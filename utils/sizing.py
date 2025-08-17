# utils/sizing.py
from __future__ import annotations
from typing import Dict, List, Optional, Tuple
from utils.data import EBOSS_LOAD_REFERENCE

# --------- 1D interpolation across load anchors (25/50/75/100%) ----------
_LOAD_X: List[float] = [0.25, 0.50, 0.75, 1.00]

def _interp1d(x: float, xp: List[float], fp: List[float]) -> float:
    """Linear interpolation with clamping to [xp[0], xp[-1]]."""
    if x <= xp[0]:
        return fp[0]
    if x >= xp[-1]:
        return fp[-1]
    for i in range(len(xp) - 1):
        if xp[i] <= x <= xp[i + 1]:
            x0, x1 = xp[i], xp[i + 1]
            y0, y1 = fp[i], fp[i + 1]
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return fp[-1]

def _gph_curve_for_size(gen_kva: int, gph_table: Dict[int, Dict[str, float]]) -> List[float]:
    """
    Return GPH at [25,50,75,100]% for the given size.
    If size isn't an exact key, interpolate ACROSS SIZE between nearest sizes.
    """
    sizes = sorted(gph_table.keys())
    if gen_kva in gph_table:
        row = gph_table[gen_kva]
        return [float(row["25%"]), float(row["50%"]), float(row["75%"]), float(row["100%"])]

    lower = max([s for s in sizes if s <= gen_kva], default=sizes[0])
    upper = min([s for s in sizes if s >= gen_kva], default=sizes[-1])
    if lower == upper:
        row = gph_table[lower]
        return [float(row["25%"]), float(row["50%"]), float(row["75%"]), float(row["100%"])]

    lr, ur = gph_table[lower], gph_table[upper]
    t = (gen_kva - lower) / (upper - lower)
    out = []
    for label in ("25%", "50%", "75%", "100%"):
        y0 = float(lr[label]); y1 = float(ur[label])
        out.append(y0 + t * (y1 - y0))
    return out

def fuel_gph_at_load(gen_kva: int | float, load: float,
                     table: Optional[Dict[int, Dict[str, float]]] = None) -> float:
    """
    Interpolate GPH from table given:
      - gen_kva: generator size in kVA
      - load: engine load as fraction (0..1) or percent (0..100)
    """
    if table is None:
        table = EBOSS_LOAD_REFERENCE["gph_interpolation"]
    load_fraction = (load / 100.0) if load > 1.0 else float(load)
    fp = _gph_curve_for_size(int(round(gen_kva)), table)
    return float(_interp1d(load_fraction, _LOAD_X, fp))

# ----------------- Helpers to fetch EBOSS charge rates / sizes -----------------

def _rec_for_model(model: str) -> Optional[Dict]:
    """Find the generator_sizes record for a given EBOSS model string."""
    for rec in EBOSS_LOAD_REFERENCE["generator_sizes"].values():
        if rec.get("eboss_model") == model:
            return rec
    return None

def eboss_defined_charge_rate_kw(model: str, eboss_type: str) -> Optional[float]:
    """
    Returns the defined charge rate (kW) for the EBOSS model/type:
      - "Full Hybrid" => fh_charge_rate
      - "Power Module" => pm_charge_rate
    """
    rec = _rec_for_model(model)
    if not rec:
        return None
    if eboss_type == "Full Hybrid":
        return float(rec.get("fh_charge_rate"))
    if eboss_type == "Power Module":
        return float(rec.get("pm_charge_rate"))
    return None

def eboss_default_gen_kva(model: str) -> Optional[int]:
    """Default hybrid gen size for EBOSS model (used for Full Hybrid)."""
    return EBOSS_LOAD_REFERENCE["generator_kva_hybrid"].get(model)

# ------------------- Public API: compute GPH by equipment type -------------------

def gph_for_eboss(model: str,
                  eboss_type: str,
                  actual_cont_kw: float,
                  pm_gen_kva: Optional[int] = None) -> Tuple[float, float, int]:
    """
    EBOSS path:
      engine_load_fraction = defined_charge_rate_kw / actual_cont_kw

    gen_kva used:
      - Full Hybrid: from EBOSS table (generator_kva_hybrid)
      - Power Module: the selected PM generator (pm_gen_kva) **must** be provided
    Returns: (gph, engine_load_percent, gen_kva_used)
    """
    charge_kw = eboss_defined_charge_rate_kw(model, eboss_type)
    if charge_kw is None or actual_cont_kw <= 0:
        return (0.0, 0.0, 0)

    # Engine load as fraction, clamp to [0, 1]
    eng_load_frac = max(0.0, min(charge_kw / float(actual_cont_kw), 1.0))
    eng_load_pct = eng_load_frac * 100.0

    # pick generator size (kVA)
    if eboss_type == "Full Hybrid":
        gen_kva = eboss_default_gen_kva(model) or 0
    else:  # Power Module
        gen_kva = int(pm_gen_kva or 0)

    if gen_kva <= 0:
        return (0.0, eng_load_pct, gen_kva)

    gph = fuel_gph_at_load(gen_kva, eng_load_frac)
    return (gph, eng_load_pct, gen_kva)

def gph_for_standard(actual_cont_kw: float,
                     gen_kw_rating: float,
                     gen_kva_size: Optional[int] = None) -> Tuple[float, float, int]:
    """
    Standard diesel generator path (NOT fh_gen / pm_gen):
      engine_load_fraction = actual_cont_kw / gen_kw_rating

    gen_kva_size:
      pass the generator's kVA (e.g., 25, 45, 70, 125, 220, 400). If only kW is known,
      convert with a PF assumption outside this function.
    Returns: (gph, engine_load_percent, gen_kva_used)
    """
    if actual_cont_kw <= 0 or gen_kw_rating <= 0:
        return (0.0, 0.0, int(gen_kva_size or 0))

    eng_load_frac = max(0.0, min(float(actual_cont_kw) / float(gen_kw_rating), 1.0))
    eng_load_pct = eng_load_frac * 100.0
    gen_kva = int(gen_kva_size or 0)
    if gen_kva <= 0:
        return (0.0, eng_load_pct, gen_kva)

    gph = fuel_gph_at_load(gen_kva, eng_load_frac)
    return (gph, eng_load_pct, gen_kva)

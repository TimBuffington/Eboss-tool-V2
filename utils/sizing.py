# utils/sizing.py
from __future__ import annotations
from typing import Dict, List, Tuple, Optional

# --- Safe imports: never crash at import time ---
try:
    from utils.data import SPECS as _SPECS  # your calc/spec table keyed by kVA
except Exception:
    _SPECS: Dict[int, Dict] = {}

# Try preferred name first, then legacy, else empty dict (functions will guard)
try:
    from utils.data import FUEL_BURN_CURVES as FUEL_CURVES
except Exception:
    try:
        from utils.data import EBOSS_LOAD_REFERENCE as FUEL_CURVES  # back-compat
    except Exception:
        FUEL_CURVES: Dict[int, List[Tuple[float, float]]] = {}

# ── Small helpers over your data ──────────────────────────────────────────────
def _spec_by_model(model_name: str) -> Dict:
    """Return the numeric spec record for a model string like 'EB125 kVA'."""
    for kva, rec in _SPECS.items():
        if rec.get("eboss_model") == model_name:
            return dict(rec)
    return {}

def _hybrid_kva_for_model(model_name: str) -> Optional[int]:
    """Which gen kVA curve to use for Full Hybrid for this model."""
    for kva, rec in _SPECS.items():
        if rec.get("eboss_model") == model_name:
            return int(kva)
    return None

def eboss_defined_charge_rate_kw(model: str, eboss_type: str) -> float:
    """
    Returns the defined charge rate (kW) for the given EBOSS model and type.
    - Full Hybrid  -> 'fh_charge_rate'
    - Power Module -> 'pm_charge_rate'
    """
    rec = _spec_by_model(model)
    if not rec:
        return 0.0
    key = "fh_charge_rate" if eboss_type == "Full Hybrid" else "pm_charge_rate"
    return float(rec.get(key, 0.0))

# ── Fuel curve interpolation ──────────────────────────────────────────────────
def _interp(x0: float, y0: float, x1: float, y1: float, x: float) -> float:
    if x1 == x0:
        return y0
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)

def _nearest_curve_size(gen_kva: int) -> int:
    """Pick nearest available kVA curve if exact size is missing."""
    if not FUEL_CURVES:
        raise RuntimeError(
            "Fuel-burn curves are missing. Define FUEL_BURN_CURVES in utils/data.py "
            "or provide EBOSS_LOAD_REFERENCE for back-compat."
        )
    sizes = sorted(FUEL_CURVES.keys())
    return min(sizes, key=lambda s: abs(s - gen_kva))

def fuel_gph_at_load(gen_kva: int, load_fraction: float) -> float:
    """
    Linear interpolation of GPH for a given generator curve (kVA) at load fraction ∈ [0, 1].
    - If the curve for gen_kva doesn't exist, we use the nearest available kVA curve.
    - load_fraction is clamped to the curve's min/max x (typically 0.25..1.00).
    """
    if not FUEL_CURVES:
        raise RuntimeError(
            "Fuel-burn curves are missing. Define FUEL_BURN_CURVES in utils/data.py "
            "or provide EBOSS_LOAD_REFERENCE for back-compat."
        )

    if gen_kva not in FUEL_CURVES:
        gen_kva = _nearest_curve_size(gen_kva)

    points: List[Tuple[float, float]] = sorted(FUEL_CURVES[gen_kva], key=lambda p: p[0])
    x_min, x_max = points[0][0], points[-1][0]
    x = max(x_min, min(x_max, float(load_fraction)))

    for i in range(1, len(points)):
        x0, y0 = points[i - 1]
        x1, y1 = points[i]
        if x0 <= x <= x1:
            return _interp(x0, y0, x1, y1, x)

    return points[-1][1]  # fallback (shouldn't hit with clamp)

# ── EBOSS & Standard GPH calculators ─────────────────────────────────────────
def gph_for_eboss(
    model: str,
    eboss_type: str,
    actual_cont_kw: float,
    pm_gen_kva: Optional[int] = None,
) -> Tuple[float, float, int]:
    """
    EBOSS rule:
      engine_load_fraction = defined_charge_rate_kw / actual_cont_kw

    gen_kVA used:
      - Full Hybrid: model's kVA (key in SPECS)
      - Power Module: the selected PM generator kVA (pm_gen_kva)
    Returns: (gph, engine_load_percent, gen_kva_used)
    """
    charge_kw = eboss_defined_charge_rate_kw(model, eboss_type)
    if charge_kw <= 0 or not actual_cont_kw or actual_cont_kw <= 0:
        return (0.0, 0.0, 0)

    if eboss_type == "Full Hybrid":
        gen_kva_used = _hybrid_kva_for_model(model) or 0
    elif eboss_type == "Power Module":
        gen_kva_used = int(pm_gen_kva or 0)
    else:
        gen_kva_used = 0

    if gen_kva_used <= 0:
        return (0.0, 0.0, 0)

    load_frac = max(0.0, min(1.0, float(charge_kw) / float(actual_cont_kw)))
    gph = fuel_gph_at_load(gen_kva_used, load_frac)
    return (float(gph), load_frac * 100.0, int(gen_kva_used))

def gph_for_standard(
    cont_kw: float,
    std_gen_kw_rating: float,
    std_gen_kva: int,
) -> Tuple[float, float, int]:
    """Standard diesel: engine_load_fraction = cont_kw / std_gen_kw_rating."""
    if not cont_kw or cont_kw <= 0 or not std_gen_kw_rating or std_gen_kw_rating <= 0:
        return (0.0, 0.0, 0)
    gen_kva_used = int(std_gen_kva or 0)
    if gen_kva_used <= 0:
        return (0.0, 0.0, 0)

    load_frac = max(0.0, min(1.0, float(cont_kw) / float(std_gen_kw_rating)))
    gph = fuel_gph_at_load(gen_kva_used, load_frac)
    return (float(gph), load_frac * 100.0, int(gen_kva_used))

def gph_for(
    *,
    model: Optional[str],
    type: str,
    cont_kw: float,
    gen_kw: Optional[float] = None,
    size_kva: Optional[int] = None,
    pm_gen: Optional[int] = None,
) -> Tuple[float, float, int]:
    """
    Unified entry used by spec_store.compute_and_store_spec(...).
    EBOSS if type in {"Full Hybrid", "Power Module"}, otherwise Standard diesel.
    """
    if type in ("Full Hybrid", "Power Module"):
        return gph_for_eboss(
            model=model or "",
            eboss_type=type,
            actual_cont_kw=cont_kw,
            pm_gen_kva=pm_gen,
        )
    if gen_kw is None or size_kva is None:
        return (0.0, 0.0, 0)
    return gph_for_standard(cont_kw=cont_kw, std_gen_kw_rating=float(gen_kw), std_gen_kva=int(size_kva))

__all__ = [
    "fuel_gph_at_load",
    "gph_for_eboss",
    "gph_for_standard",
    "gph_for",
    "eboss_defined_charge_rate_kw",
]

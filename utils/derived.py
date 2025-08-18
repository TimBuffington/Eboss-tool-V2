# utils/derived.py
from __future__ import annotations
import streamlit as st
from typing import Optional, Dict
from utils.keys import CANON as K
from utils.data import SPECS
from utils.sizing import fuel_gph_at_load  # uses (gen_kva, load_fraction)
# We'll reuse spec_store's cached spec for gen_kva_used and for defaults
# current_spec is set by compute_and_store_spec(...)

def _spec_for(model: str) -> Optional[Dict]:
    for rec in SPECS.values():
        if rec.get("eboss_model") == model:
            return rec
    return None

def _get_charge_kw(spec: Dict, eboss_type: str) -> float:
    if eboss_type == "Full Hybrid":
        return float(spec.get("fh_charge_rate", 0.0))
    else:
        return float(spec.get("pm_charge_rate", 0.0))

def _gen_kw_from_kva(gen_kva: Optional[int]) -> float:
    if not gen_kva: return 0.0
    # If you have explicit gen_kw in your data for that size, use it; else PF≈0.8
    return 0.8 * float(gen_kva)

def compute_and_store_derived() -> None:
    """Compute battery/runtimes, engine-load % (for interpolation), interpolated GPH & rollups."""
    ss = st.session_state
    spec = ss.get(K["current_spec"]) or {}
    model = ss.get(K["model"])
    eboss_type = ss.get(K["type"])
    cont_kw = float(ss.get(K["actual_cont_kw"]) or 0.0)

    if not model or not eboss_type or cont_kw <= 0:
        # not enough info yet
        return

    spec_row = _spec_for(model) or {}
    battery_kwh = float(spec_row.get("kwh", 0.0))
    charge_kw   = _get_charge_kw(spec_row, eboss_type)

    # 1) Battery/cycle model
    battery_life_hours = (battery_kwh / cont_kw) if cont_kw > 0 else 0.0
    charge_time_hours  = (battery_kwh / charge_kw) if charge_kw > 0 else 0.0
    denom = battery_life_hours + charge_time_hours
    cycles_per_day = (24.0 / denom) if denom > 0 else 0.0

    ss[K["battery_life_hours"]] = battery_life_hours
    ss[K["charge_time_hours"]]  = charge_time_hours
    ss[K["cycles_per_day"]]     = cycles_per_day

    # 2) Runtime per day
    eboss_runtime_hours = charge_time_hours * cycles_per_day
    std_runtime_hours   = 24.0
    ss[K["eboss_runtime_hours"]] = eboss_runtime_hours
    ss[K["std_runtime_hours"]]   = std_runtime_hours

    # 3) Engine-load % for interpolation (per your latest rule)
    # EBOSS: (charge_kw / gen_kw)
    gen_kva_used = int(spec.get("gen_kva_used") or 0)
    gen_kw = _gen_kw_from_kva(gen_kva_used)
    eboss_eng_load_frac = (charge_kw / gen_kw) if gen_kw > 0 else 0.0
    eboss_eng_load_frac = max(0.0, min(1.0, eboss_eng_load_frac))
    ss[K["eboss_eng_load_pct"]] = eboss_eng_load_frac * 100.0

    # Standard: (cont_kw / std_gen_kw_rating) if user provided these
    std_gen_kw = float(ss.get(K["std_gen_kw"]) or 0.0)
    std_gen_kva = int(ss.get(K["std_gen_kva"]) or 0)
    if std_gen_kw > 0 and std_gen_kva > 0:
        std_eng_load_frac = max(0.0, min(1.0, cont_kw / std_gen_kw))
        ss[K["std_eng_load_pct"]] = std_eng_load_frac * 100.0
    else:
        std_eng_load_frac = None
        ss[K["std_eng_load_pct"]] = None

    # 4) Interpolated GPH + rollups
    # EBOSS GPH at eboss_eng_load_frac and gen_kva_used
    eboss_gph = fuel_gph_at_load(gen_kva_used, eboss_eng_load_frac) if gen_kva_used > 0 else 0.0
    ss[K["eboss_gph"]] = eboss_gph

    # Standard GPH if inputs available
    if std_eng_load_frac is not None:
        std_gph = fuel_gph_at_load(std_gen_kva, std_eng_load_frac)
        ss[K["std_gph"]] = std_gph
    else:
        std_gph = None
        ss[K["std_gph"]] = None

    # EBOSS gallons per day/week/month from EBOSS runtime hours per day
    eboss_gpd = eboss_gph * eboss_runtime_hours
    ss[K["eboss_gpd"]] = eboss_gpd
    ss[K["eboss_gpw"]] = eboss_gpd * 7.0
    ss[K["eboss_gpm"]] = eboss_gpd * 30.0

    # Standard gallons (24h/day)
    if std_gph is not None:
        std_gpd = std_gph * 24.0
        ss[K["std_gpd"]] = std_gpd
        ss[K["std_gpw"]] = std_gpd * 7.0
        ss[K["std_gpm"]] = std_gpd * 30.0
    else:
        ss[K["std_gpd"]] = ss[K["std_gpw"]] = ss[K["std_gpm"]] = None

    # Also tuck these under the cached spec for one-stop reads
    cached = ss.get(K["current_spec"]) or {}
    derived = {
        K["battery_life_hours"]: battery_life_hours,
        K["charge_time_hours"]:  charge_time_hours,
        K["cycles_per_day"]:     cycles_per_day,
        K["eboss_runtime_hours"]: eboss_runtime_hours,
        K["std_runtime_hours"]:   std_runtime_hours,
        K["eboss_eng_load_pct"]: ss[K["eboss_eng_load_pct"]],
        K["std_eng_load_pct"]:   ss[K["std_eng_load_pct"]],
        K["eboss_gph"]:          ss[K["eboss_gph"]],
        K["std_gph"]:            ss[K["std_gph"]],
        K["eboss_gpd"]:          ss[K["eboss_gpd"]],
        K["std_gpd"]:            ss[K["std_gpd"]],
        K["eboss_gpw"]:          ss[K["eboss_gpw"]],
        K["std_gpw"]:            ss[K["std_gpw"]],
        K["eboss_gpm"]:          ss[K["eboss_gpm"]],
        K["std_gpm"]:            ss[K["std_gpm"]],
    }
    cached["derived"] = derived
    ss[K["current_spec"]] = cached

# utils/spec_store.py
from __future__ import annotations
from typing import Optional, Dict, Any
import streamlit as st
from utils.data import SPECS
from utils.sizing import gph_for          # returns (gph, engine_load_pct, gen_kva_used)
from utils.keys import CANON as K
from utils.derived import compute_and_store_derived  # computes battery/run/gpd/gpm, etc.

def _lookup_static_spec(model: str) -> Dict[str, Any]:
    for rec in SPECS.values():
        if rec.get("eboss_model") == model:
            return dict(rec)
    raise KeyError(f"Unknown EBOSS model: {model}")

def compute_and_store_spec(*, model: str, type: str, cont_kw: float,
                           gen_kw: Optional[float] = None,
                           size_kva: Optional[int] = None,
                           pm_gen: Optional[int] = None) -> Dict[str, Any]:
    """Build merged spec (incl. interpolated GPH), cache it in session, and compute derived metrics."""
    base = _lookup_static_spec(model)

    gph, pct, used_kva = gph_for(
        model=model, type=type, cont_kw=cont_kw,
        gen_kw=gen_kw, size_kva=size_kva, pm_gen=pm_gen
    )

    merged = {
        **base,
        "equipment_type": type,
        "actual_cont_kw": float(cont_kw),
        "gph": float(gph),
        "engine_load_percent": float(pct),
        "gen_kva_used": int(used_kva) if used_kva else 0,
        "_inputs": {
            "gen_kw": gen_kw,
            "size_kva": size_kva,
            "pm_gen": pm_gen,
        },
    }

    key = f"{model}|{type}|ckw={cont_kw:.3f}|skva={size_kva or ''}|pm={pm_gen or ''}"
    cache = st.session_state.setdefault(K["spec_cache"], {})
    cache[key] = merged
    st.session_state[K["current_spec_key"]] = key
    st.session_state[K["current_spec"]] = merged

    # populate battery/runtimes/gpd-gpm/etc.
    compute_and_store_derived()
    return merged

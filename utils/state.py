# utils/state.py
from __future__ import annotations
import streamlit as st
from typing import Any, Dict, Iterable

# All session_state defaults detected in your app
DEFAULTS: Dict[str, Any] = {
    # Router
    "page": "Home",

    # UI flags
    "show_calculator": False,
    "show_cost_analysis": False,
    "show_cost_dialog": False,
    "pm_charge_enabled": False,

    # Data buckets / computed results
    "user_inputs": {},               # you already use this as a general store
    "recommended_model": None,       # set by your recommendation logic
    "cost_standard_generator": None, # e.g., cache of cost comparison dict

    # Widget-backed inputs (these are auto-created by Streamlit, but
    # giving defaults avoids KeyErrors on first run/reset)
    "max_continuous_load_input": 0.0,
    "max_peak_load_input": 0.0,
    "units_input": "kW",             # or "Amps"
    "voltage_input": "208",          # "120" | "240" | "208" | "480"

    # Selectors (optional defaults)
    "eboss_model_input": None,       # e.g., "EB125 kVA"
    "eboss_type_input": None,        # "Full Hybrid" | "Power Module"
    "power_module_gen_size_input": None,  # "25" | "45" | "65" | "125" | "220"
    
    # Buttons (Streamlit sets these True for one run when clicked)
    "btn_manual_select": False,
    "btn_load_based": False,
    "btn_fuel_eff": False,
    "load_based_button": False,
    "fuel_efficiency_button": False,
    "launch_tool_manual": False,
    "selected_option": None,         # if you use a radio/select to drive flows
}

def ensure_state(overrides: Dict[str, Any] | None = None) -> None:
    """Call once at the top of every page to guarantee keys exist."""
    for k, v in DEFAULTS.items():
        st.session_state.setdefault(k, v)
    if overrides:
        st.session_state.update(overrides or {})

def get(key: str, default: Any = None) -> Any:
    return st.session_state.get(key, default)

def set(key: str, value: Any) -> None:
    st.session_state[key] = value

def update(values: Dict[str, Any]) -> None:
    st.session_state.update(values)

def reset(keys: Iterable[str] | None = None) -> None:
    """Reset specific keys (or all known defaults) back to defaults."""
    if keys is None:
        keys = list(DEFAULTS.keys())
    for k in keys:
        if k in st.session_state:
            del st.session_state[k]
    ensure_state()

def ns(prefix: str, name: str) -> str:
    """Create a namespaced key to avoid collisions across pages/forms."""
    return f"{prefix}:{name}"

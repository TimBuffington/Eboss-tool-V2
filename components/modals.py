# components/modals.py
from __future__ import annotations
import streamlit as st
from typing import Optional
from utils.spec_store import compute_and_store_spec  # computes + caches merged spec (incl. GPH)

EBOSS_MODELS = ["EB25 kVA", "EB70 kVA", "EB125 kVA", "EB220 kVA", "EB400 kVA"]
PM_GEN_KVA_OPTIONS = ["25 kVA", "70 kVA", "125 kVA", "220 kVA", "400 kVA"]
PLACEHOLDER = "— Select —"  # forces no default selection

# ---- Canonical keys used by ALL modals (do not rename) ----
K = {
    "model": "eboss_model",
    "type": "eboss_type",
    "pm_kva_label": "power_module_gen_size_label",
    "pm_kva": "power_module_gen_size",
    "max_cont": "max_continuous_load",
    "max_peak": "max_peak_load",
    "units": "units",
    "voltage": "voltage",
    "actual_cont_kw": "actual_continuous_load",
    "actual_peak_kw": "actual_peak_load",
}

def ensure_config_defaults() -> None:
    ss = st.session_state
    ss.setdefault(K["model"], "EB125 kVA")
    ss.setdefault(K["type"], "Full Hybrid")
    ss.setdefault(K["pm_kva_label"], None)
    ss.setdefault(K["pm_kva"], None)
    ss.setdefault(K["max_cont"], 0.0)
    ss.setdefault(K["max_peak"], 0.0)
    ss.setdefault(K["units"], PLACEHOLDER)    # start blank so user must pick
    ss.setdefault(K["voltage"], PLACEHOLDER)  # start blank so user must pick
    ss.setdefault(K["actual_cont_kw"], 0.0)
    ss.setdefault(K["actual_peak_kw"], 0.0)

def _kvlabel_to_kva(label: Optional[str]) -> Optional[int]:
    if not label:
        return None
    try:
        return int(label.split()[0])
    except Exception:
        return None

def _base_validation(model, eb_type, pm_kva) -> list[str]:
    errs = []
    if model not in EBOSS_MODELS:
        errs.append("Select a valid EBOSS® model.")
    if eb_type not in ("Power Module", "Full Hybrid"):
        errs.append("Select an EBOSS® type.")
    if eb_type == "Power Module" and not pm_kva:
        errs.append("Select a Power Module generator size.")
    return errs

def render_next_steps_nav():
    """Small navbar shown under the form once selections exist."""
    st.markdown("<div class='cta-scope' style='margin-top:.5rem;'>", unsafe_allow_html=True)
    cols = st.columns(4)
    def go(label, page, key):
        with page:
            if st.button(label, key=key):
                if hasattr(st, "switch_page"):
                    st.switch_page(f"pages/{label_map[label]}")
                else:
                    st.session_state["page"] = label  # fallback if you have manual routing
    # map labels to page files
    global label_map
    label_map = {
        "Technical Specs": "01_Tech_Specs.py",
        "Load Based Specs": "02_Load_Based_Specs.py",
        "EBOSS® to Standard Comparison": "03_Compare.py",
        "Parallel Calculator": "04_Parallel.py",
        # you can add Cost Analysis / Troubleshooting elsewhere if you want more buttons
    }
    with cols[0]:
        if st.button("Technical Specs", key="nav_specs"): 
            st.switch_page("pages/01_Tech_Specs.py")
    with cols[1]:
        if st.button("Load Based Specs", key="nav_load"):
            st.switch_page("pages/02_Load_Based_Specs.py")
    with cols[2]:
        if st.button("EBOSS® to Standard Comparison", key="nav_compare"):
            st.switch_page("pages/03_Compare.py")
    with cols[3]:
        if st.button("Parallel Calculator", key="nav_parallel"):
            st.switch_page("pages/04_Parallel.py")
    st.markdown("</div>", unsafe_allow_html=True)

def open_config_modal(mode: str) -> None:
    """
    Unified configuration modal for any mode in {"manual","load_based","fuel_eff"}.
    No Submit button: as soon as BOTH Units and Voltage are selected (not placeholders),
    we validate & compute and store results under the same canonical keys.
    """
    ensure_config_defaults()

    title = {
        "manual": "Manually Select EBOSS® Configuration",
        "load_based": "Load-Based EBOSS® Configuration",
        "fuel_eff": "Max Fuel Efficiency EBOSS® Configuration",
    }.get(mode, "EBOSS® Configuration")

    with st.modal(title, key=f"cfg_modal_{mode}"):
        # --- UI Fields (SAME KEYS ACROSS ALL MODALS) ---
        c1, c2, c3 = st.columns(3)
        with c1:
            st.selectbox("EBOSS® Model", EBOSS_MODELS, key=K["model"])
            st.selectbox("EBOSS® Type", ["Power Module", "Full Hybrid"], key=K["type"])
            if st.session_state[K["type"]] == "Power Module":
                st.selectbox("Power Module Generator Size", PM_GEN_KVA_OPTIONS, key=K["pm_kva_label"])
                st.session_state[K["pm_kva"]] = _kvlabel_to_kva(st.session_state[K["pm_kva_label"]])
            else:
                st.session_state[K["pm_kva_label"]] = None
                st.session_state[K["pm_kva"]] = None

        with c2:
            st.number_input("Max Continuous Load", min_value=0.0, step=1.0, format="%g", key=K["max_cont"])
            st.number_input("Max Peak Load",       min_value=0.0, step=1.0, format="%g", key=K["max_peak"])

        with c3:
            st.selectbox("Units",   [PLACEHOLDER, "kW", "Amps"], key=K["units"])
            st.selectbox("Voltage", [PLACEHOLDER, "120", "208", "240", "480"], key=K["voltage"])

        # --- Reactive trigger: when both Units & Voltage are selected, compute ---
        units   = st.session_state[K["units"]]
        voltage = st.session_state[K["voltage"]]
        ready = (units != PLACEHOLDER) and (voltage != PLACEHOLDER)

        model    = st.session_state[K["model"]]
        eb_type  = st.session_state[K["type"]]
        pm_kva   = st.session_state[K["pm_kva"]]
        max_cont = float(st.session_state[K["max_cont"]] or 0.0)
        max_peak = float(st.session_state[K["max_peak"]] or 0.0)

        if not ready:
            st.info("Select **Units** and **Voltage** to continue.")
            render_next_steps_nav()
            return

        # Minimal base validation (mode-independent)
        base_errs = _base_validation(model, eb_type, pm_kva)
        if base_errs:
            for e in base_errs:
                st.error(e)
            render_next_steps_nav()
            return

        # Convert Amps → kW if needed
        if units == "Amps":
            pf = 0.8
            v  = float(voltage)
            to_kw = lambda amps: (amps * v * 1.732 * pf) / 1000.0
            actual_cont_kw = to_kw(max_cont)
            actual_peak_kw = to_kw(max_peak)
        else:
            actual_cont_kw = max_cont
            actual_peak_kw = max_peak

        # Store computed values back into the SAME keys
        st.session_state[K["actual_cont_kw"]] = actual_cont_kw
        st.session_state[K["actual_peak_kw"]] = actual_peak_kw

        # Mirror into your existing bucket for backward-compat
        ui = st.session_state.setdefault("user_inputs", {})
        ui.update({
            "eboss_model": model,
            "eboss_type": eb_type,
            "power_module_gen_size": pm_kva,
            "max_continuous_load": max_cont,
            "max_peak_load": max_peak,
            "units": units,
            "voltage": voltage,
            "actual_continuous_load": actual_cont_kw,
            "actual_peak_load": actual_peak_kw,
        })

        # If we have enough to compute, do it now (GPH interpolation included)
        if actual_cont_kw > 0:
            spec = compute_and_store_spec(
                model=model,
                type=eb_type,
                cont_kw=actual_cont_kw,
                pm_gen_kva=pm_kva,                          # required for PM; ignored for FH
                size_kva=pm_kva if eb_type == "Power Module" else None,
                gen_kw=None,
            )
            st.success(
                f"Configured: **{spec['eboss_model']} • {spec['equipment_type']}** — "
                f"Engine load: **{spec['engine_load_percent']:.1f}%**, "
                f"GPH: **{spec['gph']:.2f}**"
            )
            # Let rest of app know a valid config exists
            st.session_state["show_calculator"] = True
            st.session_state["config_mode"] = mode
        else:
            st.warning("Enter a **Max Continuous Load** > 0 to run sizing/fuel calculations.")

        # --- Next steps: app navbar (uses stored data) ---
        render_next_steps_nav()

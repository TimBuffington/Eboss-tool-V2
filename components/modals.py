# components/modals.py
from __future__ import annotations
import streamlit as st
from utils.spec_store import compute_and_store_spec  # stores merged spec + gph in session

EBOSS_MODELS = ["EB25 kVA", "EB70 kVA", "EB125 kVA", "EB220 kVA", "EB400 kVA"]
PM_GEN_KVA_OPTIONS = ["25 kVA", "70 kVA", "125 kVA", "220 kVA", "400 kVA"]  # label list

def _kvlabel_to_kva(label: str | None) -> int | None:
    if not label:
        return None
    try:
        return int(label.split()[0])
    except Exception:
        return None

def _validate_manual(model, eb_type, max_cont, max_peak, pm_kva, units, voltage):
    errs = []
    if model not in EBOSS_MODELS:
        errs.append("Please select a valid EBOSS® model.")
    if eb_type not in ("Power Module", "Full Hybrid"):
        errs.append("Please select an EBOSS® type.")
    if max_cont is None or max_cont <= 0:
        errs.append("Max Continuous Load must be greater than 0.")
    if max_peak is None or max_peak <= 0:
        errs.append("Max Peak Load must be greater than 0.")
    if units not in ("kW", "Amps"):
        errs.append("Units must be either kW or Amps.")
    if units == "Amps" and voltage not in ("120", "208", "240", "480"):
        errs.append("Please pick a line voltage for Amp inputs.")
    if eb_type == "Power Module" and not pm_kva:
        errs.append("Select a Power Module generator size for PM configurations.")
    return errs

def open_manual_config_modal() -> None:
    with st.modal("Manually Select EBOSS® Configuration", key="manual_cfg_modal"):
        col1, col2, col3 = st.columns(3)

        with col1:
            model = st.selectbox("EBOSS® Model", EBOSS_MODELS, key="manual:model")
            eb_type = st.selectbox("EBOSS® Type", ["Power Module", "Full Hybrid"], key="manual:type")
            pm_kva_label = None
            if eb_type == "Power Module":
                pm_kva_label = st.selectbox("Power Module Generator Size", PM_GEN_KVA_OPTIONS, key="manual:pm_kva_label")
            pm_kva = _kvlabel_to_kva(pm_kva_label)

        with col2:
            max_cont = st.number_input("Max Continuous Load", min_value=0.0, step=1.0, format="%g", key="manual:max_cont")
            max_peak = st.number_input("Max Peak Load",       min_value=0.0, step=1.0, format="%g", key="manual:max_peak")

        with col3:
            units   = st.selectbox("Units",   ["kW", "Amps"], key="manual:units")
            voltage = st.selectbox("Voltage", ["120", "208", "240", "480"], key="manual:voltage")

        # validate
        errors = _validate_manual(model, eb_type, max_cont, max_peak, pm_kva, units, voltage)
        if errors:
            for e in errors:
                st.error(e)

        # Launch
        disabled = bool(errors)
        if st.button("Launch Tool", key="manual:launch", disabled=disabled):
            # Convert to kW if inputs are in Amps
            if units == "Amps":
                pf = 0.8
                v  = float(voltage)
                to_kw = lambda amps: (amps * v * 1.732 * pf) / 1000.0
                actual_cont_kw = to_kw(max_cont)
                actual_peak_kw = to_kw(max_peak)
            else:
                actual_cont_kw = float(max_cont)
                actual_peak_kw = float(max_peak)

            # Persist raw inputs (kept for transparency/back-compat)
            st.session_state.user_inputs = st.session_state.get("user_inputs", {})
            st.session_state.user_inputs.update({
                "eboss_model": model,
                "eboss_type": eb_type,
                "power_module_gen_size": pm_kva,    # integer kVA or None
                "max_continuous_load": max_cont,
                "max_peak_load": max_peak,
                "units": units,
                "voltage": voltage,
                "actual_continuous_load": actual_cont_kw,
                "actual_peak_load": actual_peak_kw,
            })

            # Compute & cache the merged spec (+ interpolated GPH) for reuse
            compute_and_store_spec(
                model=model,
                type=eb_type,
                cont_kw=actual_cont_kw,
                pm_gen_kva=pm_kva,                  # required for PM; ignored for FH
                size_kva=pm_kva if eb_type == "Power Module" else None,
                gen_kw=None,
            )

            # route flags (match your app’s flow)
            st.session_state["show_calculator"]  = True
            st.session_state["page"]             = "Tool Selection"
            st.session_state["launch_tool_modal"] = False
            st.rerun()

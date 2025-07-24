import streamlit as st
from config import EBOSS_LOAD_REFERENCE
from calculations import calculate_charge_rate, interpolate_gph
from components import sidebar_title, logo_header, system_config_form, load_inputs
from styling import apply_custom_css

# Apply styles
apply_custom_css()

# Sidebar + logo
sidebar_title()
logo_header()

# Constants
EBOSS_MODELS = list(EBOSS_LOAD_REFERENCE["battery_capacities"].keys())
EBOSS_TYPES = ["Full Hybrid", "Power Module"]

# Main UI
model, eboss_type, generator_kva = system_config_form(EBOSS_MODELS, EBOSS_TYPES)
continuous_kw, peak_kw = load_inputs()

if continuous_kw > peak_kw > 0:
    st.markdown('<div class="warning-box">⚠️ Continuous load cannot exceed peak load.</div>', unsafe_allow_html=True)
elif continuous_kw > 0 and peak_kw > 0:
    st.markdown('<div class="info-box">✅ Load inputs valid.</div>', unsafe_allow_html=True)

# Charge rate & fuel estimation
if continuous_kw > 0 and peak_kw > 0:
    charge_rate = calculate_charge_rate(model, eboss_type, generator_kva)
    st.markdown(f"""
    <div class="form-container">
        <h3 class="form-section-title">⚡ Charge Rate</h3>
        <p>{charge_rate} kW</p>
    </div>
    """, unsafe_allow_html=True)

    # Fuel consumption estimate
    kva = EBOSS_LOAD_REFERENCE["generator_kva_hybrid"].get(model, 25)
    gph = interpolate_gph(kva, charge_rate / (kva * 0.8))
    st.markdown(f"""
    <div class="form-container">
        <h3 class="form-section-title">⛽ Fuel Consumption Estimate</h3>
        <p>{gph:.2f} GPH at {charge_rate} kW</p>
    </div>
    """, unsafe_allow_html=True)

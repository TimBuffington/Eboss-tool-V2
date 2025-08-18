import streamlit as st
from utils.style import ensure_global_css  # <-- use the helper from utils

COLORS = {
    "Asphalt": "#000000",
    "Concrete": "#939598",
    "Energy Green": "#81BD47",
    "Alpine White": "#FFFFFF",
}

def render_global_header(mode: str = "external"):
    ensure_global_css(COLORS, extra_files=["styles/base.css"])  # base.css optional
    st.markdown("<h1 style='text-align:center;margin:.5rem 0'>EBOSS® Size & Spec Tool</h1>", unsafe_allow_html=True)

def render_config_selector() -> str | None:
    choice = None
    st.markdown("<div class='cta-scope'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Manually Select EBOSS Type and Model", key="btn_manual_select"):
            choice = "manual"
    with c2:
        if st.button("Use Load Based Suggested EBOSS", key="btn_load_based"):
            choice = "load_based"
    with c3:
        if st.button("Use EBOSS Model Based on Max Fuel Efficiency", key="btn_fuel_eff"):
            choice = "fuel_eff"
    st.markdown("</div>", unsafe_allow_html=True)
    return choice

import streamlit as st
from utils.style import ensure_global_css

COLORS = {
    "Asphalt": "#000000",
    "Concrete": "#939598",
    "Energy Green": "#81BD47",
    "Alpine White": "#FFFFFF",
}

def render_global_header(mode: str = "external"):
    ensure_global_css(COLORS, extra_files=["styles/base.css"])
    st.markdown("<h1 style='text-align:center;margin:0.5rem 0'>EBOSS® Size & Spec Tool</h1>", unsafe_allow_html=True)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

def render_config_selector() -> str | None:
    """Show config launch buttons. Returns: 'manual'|'load_based'|'fuel_eff'|None"""
    choice = None
    st.markdown("<div class='cta-scope'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Manually Select EBOSS Type and Model", key="btn_manual_select"):
            choice = "manual"
    with col2:
        if st.button("Use Load Based Suggested EBOSS", key="btn_load_based"):
            choice = "load_based"
    with col3:
        if st.button("Use EBOSS Model Based on Max Fuel Efficiency", key="btn_fuel_eff"):
            choice = "fuel_eff"

    st.markdown("</div>", unsafe_allow_html=True)
    return choice

__all__ = ["render_global_header", "render_config_selector"]

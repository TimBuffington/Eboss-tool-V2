from __future__ import annotations
import streamlit as st
from utils.style import ensure_global_css


DEMO_FORM_URL  = "https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform?usp=header"
TRAIN_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform?usp=header"
LEARN_YT_URL   = "https://youtu.be/0Om2qO-zZfM?si=XnLKJ_SfyKqqUI-g"

COLORS = {
    "Asphalt": "#000000",
    "Concrete": "#939598",
    "Energy Green": "#81BD47",
    "Alpine White": "#FFFFFF",
}
def render_global_header(mode: str = "external"):
    """Inject global CSS + show app title/logo/etc."""
    ensure_global_css(COLORS, extra_files=["styles/base.css"])  # base.css optional
    # Top title (replace with your logo if you like)
    st.markdown("<h1 style='text-align:center;margin:0.5rem 0'>EBOSS® Size & Spec Tool</h1>", unsafe_allow_html=True)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

def render_config_selector(*, include_troubleshooting: bool = True) -> str | None:
    """
    Show the three configuration launch buttons (Manual / Load-Based / Fuel-Efficient).
    Returns: "manual" | "load_based" | "fuel_eff" | "troubleshooting" | None
    """
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

    if include_troubleshooting:
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("Troubleshooting", key="btn_troubleshooting"):
            return "troubleshooting"

    return choice


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
    ensure_global_css(COLORS, extra_files=["styles/base.css"])  # optional file
    st.markdown("<h1>EBOSS® Size & Spec Tool</h1>", unsafe_allow_html=Tru
    st.markdown("<h1>EBOSS® Size & Spec Tool</h1>", unsafe_allow_html=True)
    st.markdown("<div class='cta-scope'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    if mode == "external":
        with c1:
            st.markdown(f'<a class="cta-link" href="{DEMO_FORM_URL}" target="_blank" rel="noopener">Request Demo</a>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<a class="cta-link" href="{TRAIN_FORM_URL}" target="_blank" rel="noopener">Request Training</a>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<a class="cta-link" href="{LEARN_YT_URL}" target="_blank" rel="noopener">Learn how the EBOSS® works</a>', unsafe_allow_html=True)
    else:
        with c1:
            if st.button("Request Demo", key="nav_req_demo"):
                st.session_state["page"] = "Request Demo"
        with c2:
            if st.button("Request Training", key="nav_req_train"):
                st.session_state["page"] = "Request Training"
        with c3:
            if st.button("Learn how the EBOSS® works", key="nav_learn"):
                st.session_state["page"] = "Learn How"

    st.markdown("</div>", unsafe_allow_html=True)

def render_config_selector(include_troubleshooting: bool = True) -> str | None:
    st.markdown("<div class='cta-scope'>", unsafe_allow_html=True)
    cols = st.columns(4 if include_troubleshooting else 3)
    clicked = None
    with cols[0]:
        if st.button("Manually Select EBOSS Type and Model", key="cfg_manual"): clicked = "manual"
    with cols[1]:
        if st.button("Use Load Based Suggested EBOSS", key="cfg_load"): clicked = "load_based"
    with cols[2]:
        if st.button("Use EBOSS Model Based on Max Fuel Efficiency", key="cfg_eff"): clicked = "fuel_eff"
    if include_troubleshooting:
        with cols[3]:
            if st.button("Troubleshooting", key="cfg_ts"): clicked = "troubleshooting"
    st.markdown("</div>", unsafe_allow_html=True)
    return clicked


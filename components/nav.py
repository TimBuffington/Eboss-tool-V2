# components/nav.py
from __future__ import annotations
import streamlit as st

# Real destinations
DEMO_FORM_URL  = "https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform?usp=header"
TRAIN_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform?usp=header"
LEARN_YT_URL   = "https://youtu.be/0Om2qO-zZfM?si=XnLKJ_SfyKqqUI-g"

def render_global_header(mode: str = "external"):
    """Three CTAs shown at the top of every page."""
    st.markdown("<h1>EBOSS® Size & Spec Tool</h1>", unsafe_allow_html=True)
    st.markdown("<div class='cta-scope'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    if mode == "external":
        with col1:
            st.markdown(
                f'<a class="cta-link" href="{DEMO_FORM_URL}" target="_blank" rel="noopener">Request Demo</a>',
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f'<a class="cta-link" href="{TRAIN_FORM_URL}" target="_blank" rel="noopener">Request Training</a>',
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                f'<a class="cta-link" href="{LEARN_YT_URL}" target="_blank" rel="noopener">Learn how the EBOSS® works</a>',
                unsafe_allow_html=True,
            )
    else:
        # keeps API flexible if you later add an internal page or modal mode
        with col1:
            if st.button("Request Demo", key="nav_req_demo"):
                st.session_state["page"] = "Request Demo"
        with col2:
            if st.button("Request Training", key="nav_req_train"):
                st.session_state["page"] = "Request Training"
        with col3:
            if st.button("Learn how the EBOSS® works", key="nav_learn"):
                st.session_state["page"] = "Learn How"

    st.markdown("</div>", unsafe_allow_html=True)

def render_cta_row():
    """Reusable FOUR-button row beneath the header (mobile friendly)."""
    st.markdown("<div class='cta-scope'>", unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]:
        st.button("Manually Select EBOSS Type and Model", key="btn_manual_select")
    with cols[1]:
        st.button("Use Load Based Suggested EBOSS", key="btn_load_based")
    with cols[2]:
        st.button("Use EBOSS Model Based on Max Fuel Efficiency", key="btn_fuel_eff")
    with cols[3]:
        # Troubleshooting page: switch if you have a multipage file, else placeholder
        if "st_switch_page" in dir(st):  # Streamlit >=1.48 shim
            if st.button("Troubleshooting", key="btn_troubleshooting"):
                st.switch_page("pages/05_Troubleshooting.py")
        else:
            if st.button("Troubleshooting", key="btn_troubleshooting"):
                st.session_state["page"] = "Troubleshooting"
    st.markdown("</div>", unsafe_allow_html=True)

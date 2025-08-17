# components/nav.py
from __future__ import annotations
import streamlit as st

DEMO_FORM_URL  = "https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform?usp=header"
TRAIN_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform?usp=header"
LEARN_YT_URL   = "https://youtu.be/0Om2qO-zZfM?si=XnLKJ_SfyKqqUI-g"

def render_global_header(mode: str = "external"):
    st.markdown("<h1>EBOSS® Size & Spec Tool</h1>", unsafe_allow_html=True)
    st.markdown("<div class='cta-scope'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    if mode == "external":
        with col1:
            st.markdown(f'<a class="cta-link" href="{DEMO_FORM_URL}" target="_blank" rel="noopener">Request Demo</a>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<a class="cta-link" href="{TRAIN_FORM_URL}" target="_blank" rel="noopener">Request Training</a>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<a class="cta-link" href="{LEARN_YT_URL}" target="_blank" rel="noopener">Learn how the EBOSS® works</a>', unsafe_allow_html=True)
    else:
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
    st.markdown("<div class='cta-scope'>", unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]:
        st.button("Manually Select EBOSS Type and Model", key="btn_manual_select")
    with cols[1]:
        st.button("Use Load Based Suggested EBOSS", key="btn_load_based")
    with cols[2]:
        st.button("Use EBOSS Model Based on Max Fuel Efficiency", key="btn_fuel_eff")
    with cols[3]:
        st.button("Troubleshooting", key="btn_troubleshooting")
    st.markdown("</div>", unsafe_allow_html=True)

# components/nav.py (append this)

import streamlit as st

def render_config_selector(include_troubleshooting: bool = False) -> str | None:
    """
    Show the 3 EBOSS configuration choices (CTA-styled, full-width, mobile-friendly).
    Returns one of: "manual", "load_based", "fuel_eff", "troubleshooting", or None.

    Also sets a few session flags for downstream logic:
      - st.session_state["config_mode"] = <mode>
      - st.session_state["launch_tool_modal"] = True  (single choke point to open your modal/page)
    """
    st.markdown("<div class='cta-scope'>", unsafe_allow_html=True)

    cols = st.columns(3)

    clicked_mode = None

    with cols[0]:
        if st.button("Manually Select EBOSS Type and Model", key="cfg_manual"):
            clicked_mode = "manual"
    with cols[1]:
        if st.button("Use Load Based Suggested EBOSS", key="cfg_load_based"):
            clicked_mode = "load_based"
    with cols[2]:
        if st.button("Use EBOSS Model Based on Max Fuel Efficiency", key="cfg_fuel_eff"):
            clicked_mode = "fuel_eff"

   st.markdown("</div>", unsafe_allow_html=True)

    if clicked_mode:
        # one canonical place to store the selection for the rest of the app
        st.session_state["config_mode"] = clicked_mode
        # flip a single flag your router can listen for (to open your modal / go to inputs)
        st.session_state["launch_tool_modal"] = True

        # (Optional) back-compat flags if other code expects them
        st.session_state["use_manual_select"]      = (clicked_mode == "manual")
        st.session_state["use_load_based"]         = (clicked_mode == "load_based")
        st.session_state["use_max_fuel_efficiency"]= (clicked_mode == "fuel_eff")

    return clicked_mode

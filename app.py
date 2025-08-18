import streamlit as st
from components.nav import render_global_header, render_config_selector
from components.modals import open_config_modal

st.set_page_config(page_title="EBOSS® Tool", layout="wide", initial_sidebar_state="collapsed")

render_global_header(mode="external")
st.markdown("<div class='message-text'>Please Select an EBOSS Configuration</div>", unsafe_allow_html=True)

choice = render_config_selector(include_troubleshooting=True)
if choice in ("manual", "load_based", "fuel_eff"):
    open_config_modal(choice)
elif choice == "troubleshooting":
    if hasattr(st, "switch_page"):
        st.switch_page("pages/05_Troubleshooting.py")

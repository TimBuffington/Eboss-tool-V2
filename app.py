import streamlit as st
from utils.theme import apply_theme, render_logo
from utils.state import ensure_state
from components.nav import render_global_header, render_config_selector

st.set_page_config(page_title="EBOSS® Tool", layout="wide", initial_sidebar_state="collapsed")

apply_theme()
ensure_state()
render_logo()

st.header("EBOSS® Home")
render_global_header(mode="external")



# header + external CTAs (forms/video), mobile-friendly
render_global_header(mode="external")

# EBOSS configuration chooser (this is the row you meant)
mode = render_config_selector(include_troubleshooting=True)

# Handle the selection (open your existing modal / route to inputs)
if mode:
    # Your app already had a modal/input flow — trigger it here:
    # e.g., open a modal or jump to an inputs page based on mode
    if mode == "manual":
        # show your manual selection modal/page
        st.session_state["page"] = "Tool Selection"         # or whatever your router expects
        st.session_state["show_tool_modal"] = True          # if you use a modal
        st.rerun()
    elif mode == "load_based":
        st.session_state["page"] = "Tool Selection"
        st.session_state["show_tool_modal"] = True
        st.rerun()
    elif mode == "fuel_eff":
        st.session_state["page"] = "Tool Selection"
        st.session_state["show_tool_modal"] = True
        st.rerun()
    elif mode == "troubleshooting":
        # go to your troubleshooting page if you have a multipage app
        if hasattr(st, "switch_page"):
            st.switch_page("pages/05_Troubleshooting.py")

# Reusable 4-column CTA row
render_cta_row(
    col1=("Technical Specs", "pages/01_Tech_Specs.py"),
    col2=("Load Based Specs", "pages/02_Load_Based_Specs.py"),
    col3=("EBOSS® to Standard Comparison", "pages/03_Compare.py"),
    col4=("Troubleshooting", "pages/05_Troubleshooting.py"),
)

# Optional: a second row of CTAs
render_cta_row(
    col1=("Cost Analysis", "pages/06_Cost_Analysis.py"),
    col2=("Parallel Calculator", "pages/04_Parallel.py"),
    col3=(" ", None),  # placeholder
    col4=(" ", None),  # placeholder
)


import streamlit as st
from components.nav import render_global_header, render_config_selector
from components.modals import open_config_modal
from utils.style import ensure_global_css

COLORS = {
    "Asphalt": "#000000",
    "Concrete": "#939598",
    "Energy Green": "#81BD47",
    "Alpine White": "#FFFFFF",
}

st.set_page_config(page_title="EBOSS® Tool", layout="wide", initial_sidebar_state="collapsed")

# Inject CSS once per session (feels global on every page that calls header)
ensure_global_css(COLORS, extra_files=["styles/base.css"])  # make sure styles/base.css exists

# Render the shared header + external CTA links/buttons
render_global_header(mode="external")

# Home: configuration launcher buttons
choice = render_config_selector(include_troubleshooting=True)

if choice in ("manual", "load_based", "fuel_eff"):
    open_config_modal(choice)
elif choice == "troubleshooting":
    if hasattr(st, "switch_page"):
        st.switch_page("pages/05_Troubleshooting.py")

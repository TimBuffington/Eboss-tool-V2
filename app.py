import streamlit as st
from utils.theme import apply_theme, render_logo
from utils.state import ensure_state
from components.nav import render_global_header, render_config_selector
from components.modals import open_manual_config_modal
st.set_page_config(page_title="EBOSS® Tool", layout="wide", initial_sidebar_state="collapsed")

apply_theme()
ensure_state()
render_logo()
render_global_header(mode="external")
choice = render_config_selector(include_troubleshooting=True)

# Open the right input UI
if choice == "manual":
    open_manual_config_modal()
elif choice == "load_based":
    # TODO: open your load-based modal (similar pattern)
    pass
elif choice == "fuel_eff":
    # TODO: open your max fuel efficiency modal (similar pattern)
    pass

import streamlit as st
from utils.theme import apply_theme, render_logo
from utils.state import ensure_state
from components.nav import render_cta_row

st.set_page_config(page_title="EBOSS® Tool", layout="wide", initial_sidebar_state="collapsed")

apply_theme()
ensure_state()
render_logo()

st.header("EBOSS® Home")
render_global_header(mode="external")

st.write("Choose a module to get started:")

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

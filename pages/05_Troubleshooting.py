import streamlit as st
from utils.theme import apply_theme, render_logo
from utils.state import ensure_state
from components.fault_lookup_widget import render_fault_lookup_widget

apply_theme(); ensure_state(); render_logo()
st.header("Troubleshooting")

render_fault_lookup_widget()

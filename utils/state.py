import streamlit as st

DEFAULTS = {
    "user_inputs": {},
}

def ensure_state():
    for k, v in DEFAULTS.items():
        st.session_state.setdefault(k, v)


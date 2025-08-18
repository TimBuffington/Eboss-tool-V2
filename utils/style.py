# utils/style.py
from pathlib import Path
import streamlit as st
from utils import render_global_header

def inject_css_file(path: str):
    css = Path(path).read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def inject_theme_vars(colors: dict):
    # inject color tokens as CSS variables
    st.markdown(
        f"""
        <style>
        :root {{
          --asphalt: {colors["Asphalt"]};
          --alpine: {colors["Alpine White"]};
          --concrete: {colors["Concrete"]};
          --energy: {colors["Energy Green"]};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def inject_theme_css():
    # static CSS that uses the variables above; no Python formatting here
    st.markdown(
        """
        <style>
        .cta-scope [data-testid="column"] .stButton { width: 100%; }
        .cta-scope .stButton > button{
            display:block; width:100%;
            background-color: var(--asphalt);
            color: var(--alpine);
            border: 2px solid var(--concrete);
            border-radius: 10px;
            font-weight: 700;
            padding: 12px 14px;
            text-shadow: 0 0 6px var(--energy);
            transition: box-shadow .25s ease, transform .15s ease;
        }
        .cta-scope .stButton > button:hover{
            box-shadow: 0 0 28px var(--energy);
            transform: translateY(-1px);
        }
        .cta-link{
            display:flex; align-items:center; justify-content:center;
            width:100%; min-height:56px; text-decoration:none!important;
            background-color: var(--asphalt);
            color: var(--alpine);
            border: 2px solid var(--concrete);
            border-radius: 10px;
            padding: 12px 14px;
            font-weight: 700;
            text-shadow: 0 0 6px var(--energy);
            transition: box-shadow .25s ease, transform .15s ease;
        }
        .cta-link:hover{ box-shadow: 0 0 28px var(--energy); transform: translateY(-1px); }
        </style>
        """,
        unsafe_allow_html=True,
    )

def ensure_global_css(colors: dict, extra_files: list[str] | None = None):
    """Call once per page (or from your header)."""
    if st.session_state.get("_css_injected"):
        return
    inject_theme_vars(colors)
    inject_theme_css()
    for f in (extra_files or []):
        try:
            inject_css_file(f)
        except FileNotFoundError:
            pass
    st.session_state["_css_injected"] = True

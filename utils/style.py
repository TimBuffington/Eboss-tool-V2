from pathlib import Path
import streamlit as st

def inject_css_file(path: str):
    css = Path(path).read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def inject_theme_css(colors: dict):
    pal = {
        "asphalt": colors["Asphalt"],
        "alpine": colors["Alpine White"],
        "concrete": colors["Concrete"],
        "energy": colors["Energy Green"],
    }
    css = """
    .cta-scope [data-testid="column"] .stButton{width:100%}
    .cta-scope .stButton > button{
        display:block;width:100%;
        background-color:{asphalt};color:{alpine};
        border:2px solid {concrete};border-radius:10px;
        font-weight:700;padding:12px 14px;
        text-shadow:0 0 6px {energy};
        transition: box-shadow .25s ease, transform .15s ease;
    }
    .cta-scope .stButton > button:hover{
        box-shadow:0 0 28px {energy};transform: translateY(-1px);
    }
    .cta-link{
        display:flex;align-items:center;justify-content:center;
        width:100%;min-height:56px;text-decoration:none!important;
        background-color:{asphalt};color:{alpine};
        border:2px solid {concrete};border-radius:10px;padding:12px 14px;
        font-weight:700;text-shadow:0 0 6px {energy};
        transition: box-shadow .25s ease, transform .15s ease;
    }
    .cta-link:hover{ box-shadow:0 0 28px {energy}; transform: translateY(-1px); }
    """
    st.markdown(f"<style>{css.format(**pal)}</style>", unsafe_allow_html=True)

def ensure_global_css(colors: dict, extra_files: list[str] | None = None):
    """Run once per session to make CSS feel global across pages."""
    if st.session_state.get("_css_injected"):
        return
    inject_theme_css(colors)
    for f in (extra_files or []):
        inject_css_file(f)
    st.session_state["_css_injected"] = True

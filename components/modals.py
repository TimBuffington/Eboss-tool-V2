import streamlit as st

# Placeholder for COLORS; replace with actual definitions
COLORS = {
    "primary": "#0055A4",
    "secondary": "#FF9900",
    "background": "#FFFFFF",
}

# Placeholder for ensure_global_css; replace with actual implementation
def ensure_global_css(colors, extra_files=None):
    css = """
    <style>
    h1 { color: %s; }
    .cta-scope { 
        background-color: %s; 
        padding: 1rem;
        border-radius: 8px;
    }
    .stButton>button {
        width: 100%;
        padding: 0.5rem;
        background-color: %s;
        color: white;
        border: none;
        border-radius: 4px;
    }
    .stButton>button:hover {
        background-color: %s;
    }
    </style>
    """ % (colors["primary"], colors["background"], colors["primary"], colors["secondary"])
    if extra_files:
        for file in extra_files:
            try:
                with open(file, "r") as f:
                    css += f"<style>{f.read()}</style>"
            except FileNotFoundError:
                st.error(f"CSS file {file} not found")
    st.markdown(css, unsafe_allow_html=True)

PAGE_MAP = {
    "Technical Specs": "pages/01_Tech_Specs.py",
    "Load Based Specs": "pages/02_Load_Based_Specs.py",
    "Compare": "pages/03_Compare.py",
    "Cost Analysis": "pages/05_Cost_Analysis.py",
    "Paralleling": "pages/04_Parallel.py",
}

def _nav_to(page_label: str, *, mode_key: str):
    st.session_state["launch_tool_modal"] = False
    target = PAGE_MAP.get(page_label)
    if target and hasattr(st, "switch_page"):
        st.switch_page(target)
    else:
        st.session_state["page"] = page_label
        st.rerun()

def render_modal_nav_grid(*, mode_key: str):
    """2 columns × 3 rows; last right cell now omitted."""
    st.markdown("<div class='cta-scope' style='margin-top:.75rem;'>", unsafe_allow_html=True)
    rows = [
        ("Technical Specs", "Load Based Specs"),
        ("Compare", "Cost Analysis"),
        ("Paralleling", None),
    ]
    for left, right in rows:
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            st.button(
                left,
                key=f"nav_{left.replace(' ','_').lower()}_{mode_key}",
                on_click=_nav_to,
                kwargs={"page_label": left, "mode_key": mode_key},
            )
        with c2:
            if right:
                st.button(
                    right,
                    key=f"nav_{right.replace(' ','_').lower()}_{mode_key}",
                    on_click=_nav_to,
                    kwargs={"page_label": right, "mode_key": mode_key},
                )
            else:
                st.markdown("&nbsp;", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_global_header(mode: str = "external"):
    ensure_global_css(COLORS, extra_files=["styles/base.css"])
    st.markdown("<h1 style='text-align:center;margin:0.5rem 0'>EBOSS® Size & Spec Tool</h1>", unsafe_allow_html=True)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    render_modal_nav_grid(mode_key=mode)

def render_config_selector():
    """Renders a selector for configuration modes."""
    return st.selectbox("Select configuration mode", ["manual", "load_based", "fuel_eff"], key="config_selector")

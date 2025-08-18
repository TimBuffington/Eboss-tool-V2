import streamlit as st

PAGE_MAP = {
    "Technical Specs": "pages/01_Tech_Specs.py",
    "Load Based Specs": "pages/02_Load_Based_Specs.py",
    "Compare": "pages/03_Compare.py",
    "Cost Analysis": "pages/05_Cost_Analysis.py",
    "Paralleling": "pages/04_Parallel.py",
    # "Troubleshooting": removed
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
        ("Compare",         "Cost Analysis"),
        ("Paralleling",     None),  # no Troubleshooting
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
                st.markdown("&nbsp;", unsafe_allow_html=True)  # spacer
    st.markdown("</div>", unsafe_allow_html=True)
import streamlit as st

PAGE_MAP = {
    "Technical Specs": "pages/01_Tech_Specs.py",
    "Load Based Specs": "pages/02_Load_Based_Specs.py",
    "Compare": "pages/03_Compare.py",
    "Cost Analysis": "pages/05_Cost_Analysis.py",
    "Paralleling": "pages/04_Parallel.py",
    # "Troubleshooting": removed
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
        ("Compare",         "Cost Analysis"),
        ("Paralleling",     None),  # no Troubleshooting
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
                st.markdown("&nbsp;", unsafe_allow_html=True)  # spacer
    st.markdown("</div>", unsafe_allow_html=True)
def open_config_modal(mode: str) -> None:
    """Unified configuration modal with version-safe modal/dialog fallback."""
    title = f"EBOSS Configuration — {mode.title()}"
    def _body() -> None:
        # Lazy imports to avoid import-time crashes if utils are mid-refactor.
        try:
            from utils.spec_store import compute_and_store_spec  # noqa: F401
            from utils.sizing import eboss_defined_charge_rate_kw  # noqa: F401
        except Exception:
            pass

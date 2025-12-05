import streamlit as st
from utils.style import ensure_global_css  # <-- use the helper from utils
from style import ensure_global_css   # if defined externally, optional

# ⬇️ CALL YOUR CSS LOADER HERE — immediately after imports
ensure_global_css(COLORS, extra_files=["styles/base.css"])

# -------------------------------------------------
# Now define your components
# -------------------------------------------------

def render_global_header(mode: str = "external"):
    st.markdown("<h1 style='text-align:center;margin:.5rem 0'>EBOSS® Size & Spec Tool</h1>", unsafe_allow_html=True)

def render_config_selector() -> str | None:
    choice = None
    st.markdown("<div class='cta-scope'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Manually Select EBOSS Type and Model", key="btn_manual_select"):
            choice = "manual"
    with c2:
        if st.button("Use Load Based Suggested EBOSS", key="btn_load_based"):
            choice = "load_based"
    with c3:
        if st.button("Use EBOSS Model Based on Max Fuel Efficiency", key="btn_fuel_eff"):
            choice = "fuel_eff"
    st.markdown("</div>", unsafe_allow_html=True)
    return choice


def render_modal_nav_grid(*, mode_key: str) -> None:
    st.markdown("<div class='cta-scope' style='margin-top:.75rem;'>", unsafe_allow_html=True)
    rows = [
        ("Technical Specs", "Load Based Specs"),
        ("Compare", "Cost Analysis"),
        ("Paralleling", None),
    ]
    for left, right in rows:
        c1, c2 = st.columns(2, gap="small")
        with c1:
            st.button(
                left,
                key=f"nav_{left.replace(' ', '_').lower()}_{mode_key}",
                on_click=_nav_to,
                args=(left,),
            )
        with c2:
            if right:
                st.button(
                    right,
                    key=f"nav_{right.replace(' ', '_').lower()}_{mode_key}",
                    on_click=_nav_to,
                    args=(right,),
                )
            else:
                st.markdown("&nbsp;", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def nav_to(page_label: str, *, mode_key: str) -> None:
    st.session_state["launch_tool_modal"] = False
    target = PAGE_MAP.get(page_label)
    if target and hasattr(st, "switch_page"):
        st.switch_page(target)
    else:
        st.session_state["page"] = page_label
        st.rerun()


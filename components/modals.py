# components/modals.py
from __future__ import annotations
import streamlit as st

# Keep this file import-safe. Only Streamlit at top level; lazy-import the rest inside functions.

# Pages this modal can navigate to
PAGE_MAP = {
    "Technical Specs": "pages/01_Tech_Specs.py",
    "Load Based Specs": "pages/02_Load_Based_Specs.py",
    "Compare": "pages/03_Compare.py",
    "Cost Analysis": "pages/05_Cost_Analysis.py",
    "Paralleling": "pages/04_Parallel.py",
}

def _nav_to(page_label: str, *, mode_key: str):
    """Close modal & navigate."""
    st.session_state["launch_tool_modal"] = False
    target = PAGE_MAP.get(page_label)
    if target and hasattr(st, "switch_page"):
        st.switch_page(target)
    else:
        st.session_state["page"] = page_label
        st.rerun()

def render_modal_nav_grid(*, mode_key: str):
    """2 columns × 3 rows (last right cell is blank since Troubleshooting is removed)."""
    st.markdown("<div class='cta-scope' style='margin-top:.75rem;'>", unsafe_allow_html=True)
    rows = [
        ("Technical Specs", "Load Based Specs"),
        ("Compare",         "Cost Analysis"),
        ("Paralleling",     None),
    ]
    for left, right in rows:
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            st.button(
                left,
                key=f"nav_{left.replace(' ', '_').lower()}_{mode_key}",
                on_click=_nav_to,
                kwargs={"page_label": left, "mode_key": mode_key},
            )
        with c2:
            if right:
                st.button(
                    right,
                    key=f"nav_{right.replace(' ', '_').lower()}_{mode_key}",
                    on_click=_nav_to,
                    kwargs={"page_label": right, "mode_key": mode_key},
                )
            else:
                st.markdown("&nbsp;", unsafe_allow_html=True)  # spacer
    st.markdown("</div>", unsafe_allow_html=True)

def open_config_modal(mode: str) -> None:
    """
    Unified configuration modal for {'manual','load_based','fuel_eff'}.
    NOTE: Heavy imports are done lazily inside this function to avoid ImportError on module import.
    """
    with st.modal(f"EBOSS Configuration — {mode.title()}", key=f"cfg_modal_{mode}"):
        # --- Lazy imports here (so this file can be imported even if utils are mid-refactor)
        try:
            # Only when the modal is opened do we import these:
            from utils.spec_store import compute_and_store_spec
            from utils.sizing import eboss_defined_charge_rate_kw  # optional helper
        except Exception:
            # Keep the modal usable even if utils layer is broken
            compute_and_store_spec = None
            eboss_defined_charge_rate_kw = None

        # -----------------------
        # Render your real fields here (units, voltage, type/model, etc.)
        # For smoke-test, show minimal content so import succeeds:
        st.write("Configure your EBOSS settings. (If you see this, import worked.)")

        # TODO: your real UI goes here...
        # When ready to compute, guard the call:
        # if compute_and_store_spec and ready:
        #     compute_and_store_spec(model=..., type=..., cont_kw=..., gen_kw=..., size_kva=..., pm_gen=...)

        # Shared nav buttons at bottom:
        render_modal_nav_grid(mode_key=mode)

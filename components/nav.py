import streamlit as st
from __future__ import annotations
import streamlit.components.v1 as components

def render_cta_row(col1, col2, col3, col4):
    """
    Each col is a tuple: (label, page_path or None).
    If page_path is None, shows 'Coming Soon' placeholder.
    """
    st.markdown("<div class='cta-scope'>", unsafe_allow_html=True)
    cols = st.columns(4)
    for idx, (label, page) in enumerate([col1, col2, col3, col4]):
        with cols[idx]:
            if page:
                if st.button(label, key=f"cta_{idx}"):
                    st.switch_page(page)   # Streamlit 1.48+
            else:
                if st.button(f"{label}", key=f"cta_{idx}"):
                    st.toast("Coming soon.", icon="⏳")
    st.markdown("</div>", unsafe_allow_html=True)


# === REAL destinations (from your app) ===
DEMO_FORM_URL  = "https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform?usp=header"
TRAIN_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform?usp=header"
LEARN_YT_URL   = "https://youtu.be/0Om2qO-zZfM?si=XnLKJ_SfyKqqUI-g"

def render_global_header(mode: str = "external"):
    """
    Render the site-wide header + three CTAs on every page.

    mode:
      - "external": open Google Forms / YouTube in a new tab (styled <a> links)
      - "embed": open the REAL Google Form in a modal with an embedded iframe (no fake submitters)
      - "pages": use st.switch_page(...) (only if you’ve created those internal pages)

    NOTE: Styling relies on your .cta-scope / .cta-link CSS from theme.py.
    """
    st.markdown("<h1>EBOSS® Size & Spec Tool</h1>", unsafe_allow_html=True)

    st.markdown("<div class='cta-scope'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])

    if mode == "external":
        # Real links (open in new tab), no placeholders
        with col1:
            st.markdown(
                f'<a class="cta-link" href="{DEMO_FORM_URL}" target="_blank" rel="noopener">Request Demo</a>',
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f'<a class="cta-link" href="{TRAIN_FORM_URL}" target="_blank" rel="noopener">Request Training</a>',
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                f'<a class="cta-link" href="{LEARN_YT_URL}" target="_blank" rel="noopener">Learn how the EBOSS® works</a>',
                unsafe_allow_html=True,
            )

    elif mode == "embed":
        # No fake submission—embed the REAL Google Forms in modals
        with col1:
            if st.button("Request Demo", key="btn_demo_embed"):
                _open_form_modal("Request a Demo", DEMO_FORM_URL)
        with col2:
            if st.button("Request Training", key="btn_train_embed"):
                _open_form_modal("Request On-Site Training", TRAIN_FORM_URL)
        with col3:
            # Use native Streamlit video for the real YouTube link
            if st.button("Learn how the EBOSS® works", key="btn_learn_embed"):
                with st.modal("How EBOSS® Works"):
                    st.video(LEARN_YT_URL)
                    st.button("Close")

    elif mode == "pages":
        # Only use this if you created internal pages and want to route there
        # (These pages should present/redirect to the same REAL forms/YouTube)
        with col1:
            if st.button("Request Demo", key="btn_demo_page"):
                st.switch_page("pages/90_Request_Demo.py")
        with col2:
            if st.button("Request Training", key="btn_train_page"):
                st.switch_page("pages/91_Request_Training.py")
        with col3:
            # Still best as a real external link
            st.markdown(
                f'<a class="cta-link" href="{LEARN_YT_URL}" target="_blank" rel="noopener">Learn how the EBOSS® works</a>',
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)


def _open_form_modal(title: str, form_url: str, height: int = 720):
    """Open a modal and embed the REAL Google Form (no placeholder submissions)."""
    # Use Google Forms' embeddable query for best results
    embed_url = form_url.replace("/viewform", "/viewform?embedded=true")
    with st.modal(title):
        # You can also use st.components.v1.iframe directly:
        components.iframe(embed_url, height=height, scrolling=True)
        st.caption("This is the live Google Form. Submissions go directly to your Google Form destination.")
        st.button("Close")



import streamlit as st

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



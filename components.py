# components.py

import streamlit as st

def sidebar_title():
    st.sidebar.title("⚡ EBOSS® Tool")
    st.sidebar.markdown("Built for EBOSS® vs Diesel Generator Analysis")

def logo_header():
    st.markdown('<div style="text-align:center; margin-bottom:1rem;">'
                '<img src="https://anacorp.com/wp-content/uploads/2023/10/ANA-ENERGY-LOGO-PADDED.png" width="200">'
                '</div>', unsafe_allow_html=True)

def system_config_form(eboss_models, eboss_types, default_model=None, default_type=None):
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="form-section-title">System Configuration</h3>', unsafe_allow_html=True)

    model = st.selectbox("EBOSS® Model", eboss_models, index=eboss_models.index(default_model) if default_model else 0)
    eboss_type = st.selectbox("EBOSS® Type", eboss_types, index=eboss_types.index(default_type) if default_type else 0)

    generator_kva = None
    if eboss_type == "Power Module":
        generator_options = ["25kVA", "45kVA", "65kVA", "125kVA", "220kVA", "400kVA"]
        generator_kva = st.selectbox("Generator Size", generator_options)

    st.markdown('</div>', unsafe_allow_html=True)
    return model, eboss_type, generator_kva

def load_inputs(continuous=0, peak=0):
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="form-section-title">Load Requirements</h3>', unsafe_allow_html=True)

    continuous_kw = st.number_input("Continuous Load (kW)", min_value=0.0, max_value=500.0, value=continuous, step=1.0)
    peak_kw = st.number_input("Max Peak Load (kW)", min_value=0.0, max_value=500.0, value=peak, step=1.0)

    st.markdown('</div>', unsafe_allow_html=True)
    return continuous_kw, peak_kw

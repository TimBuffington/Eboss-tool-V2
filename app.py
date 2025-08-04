
import streamlit as st
from datetime import date

# Global CSS and floating logo
def apply_custom_css():
    st.markdown("""
    <style>
    .stApp {
        background: url("https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/bg.png") no-repeat center center fixed !important;
        background-size: cover !important;
        background-color: #000000 !important;
        padding-top: 90px !important;
    }
    .logo-absolute {
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        z-index: 9999;
    }
    .logo-absolute img {
        height: 80px;
    }
    .card {
        background-color: #000000;
        border: 2px solid #D3D3D3;
        border-radius: 12px;
        padding: .5rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .card-label {
        font-size: 1rem;
        font-weight: bold;
        color: #81BD47;
        text-align: center;
    }
    .card-value {
        font-size: 0.9rem;
        font-weight: bold;
        color: #81BD47;
        text-align: center;
        margin-top: 0.2rem;
    }
    .stSelectbox > div > div,
    .stTextInput > div > div,
    .stNumberInput > div > div {
        background-color: #000000 !important;
        color: #81BD47 !important;
        border: 1px solid #D3D3D3 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 0.5rem 1rem !important;
    }
    [data-baseweb="menu"] {
        background-color: #000000 !important;
        color: #81BD47 !important;
        border: 1px solid #D3D3D3 !important;
        border-radius: 6px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="logo-absolute">
            <img src="https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/logo.png">
        </div>
    """, unsafe_allow_html=True)

# Spec layout and placeholder data
SPEC_LAYOUT = {
    "Maximum Intermittent Power Output": [
        "Three-phase", "Single-phase", "Frequency", "Simultaneous voltage",
        "Voltage regulation", "Amp-load @ 208V", "Amp-load @ 480V",
        "Motor start (3 sec @ 208V)", "Motor start (3 sec @ 480V)"
    ],
    "Maximum Continuous Power Output": [
        "Generator size", "Three-phase output", "Single-phase output",
        "Simultaneous voltage", "Amp-load @ 208V", "Amp-load @ 480V"
    ],
    "Technology": [
        "Battery chemistry", "Battery capacity", "Energy throughput",
        "Charge time (no load)", "Inverter output max", "Parallel capability"
    ],
    "Battery Life": [
        "Battery type", "Cycle life @ 77°F", "Cycle life @ 100°F", "Life @ 3kW load (100°F)"
    ],
    "Operating Temperatures": [
        "Inverter cold start (min)", "Running temp range", "Arctic package (optional)"
    ],
    "Weights & Dimensions": [
        "EBOSS only (L×W×H)", "EBOSS weight only", "With trailer & generator",
        "Total weight (no fuel / full)", "Fuel tank capacity"
    ]
}

spec_data = {}  # Inject your model data here

def show_logo_and_title(title):
    st.markdown(f"<h1 style='text-align:center; color:#81BD47;'>{title}</h1>", unsafe_allow_html=True)

def top_navbar():
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Back to Input"):
            st.session_state.section = "input"
            st.rerun()
    with col2:
        st.empty()
    with col3:
        if st.button("🛠 View Specs Again"):
            st.rerun()

def render_tech_specs_page():
    apply_custom_css()
    show_logo_and_title("Tech Specs")
    top_navbar()

    model = st.session_state.user_inputs.get("model", "EBOSS 25 kVA")
    if model not in spec_data:
        st.warning("⚠️ No model selected or data missing.")
        return

    st.markdown(f'''
        <div class="card" style="margin-top: -1rem; margin-bottom: 2rem;">
            <div class="card-label" style="font-size: 1.1rem;">
                Showing specs for: <strong style="color:#81BD47;">{model}</strong>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card"><div class="card-label">🔁 Change EBOSS Model</div>', unsafe_allow_html=True)
        st.session_state.user_inputs["model"] = st.selectbox(
            "Model", list(spec_data.keys()), index=list(spec_data.keys()).index(model)
        )
        st.markdown('</div>', unsafe_allow_html=True)

    for section, labels in SPEC_LAYOUT.items():
        values = spec_data[model].get(section, ["—"] * len(labels))
        st.markdown(f'''
            <div class="card" style="background-color: #636569; color: white; font-weight: 700;
                font-size: 1.2rem; padding: 0.8rem 1.5rem; border-radius: 12px;
                margin: 2rem 0 1rem 0; text-align: center; text-transform: uppercase;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
                {section}
            </div>
        ''', unsafe_allow_html=True)
        for label, value in zip(labels, values):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f'<div class="card"><div class="card-label">{label}</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="card"><div class="card-value">{value}</div></div>', unsafe_allow_html=True)

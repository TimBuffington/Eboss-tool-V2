
import streamlit as st
from datetime import date

# ───────────────────────────────
# ✅ GLOBAL STYLING + LOGO
# ───────────────────────────────
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
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="logo-absolute">
            <img src="https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/logo.png">
        </div>
    """, unsafe_allow_html=True)

# ───────────────────────────────
# ✅ STATIC SPECS FORMAT
# ───────────────────────────────
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

spec_data = {}  # Replace with your full dictionary from earlier

# ───────────────────────────────
# ✅ NAVBAR + LOGIC
# ───────────────────────────────
def show_logo_and_title(title):
    st.markdown(f"<h1 style='text-align:center; color:#81BD47;'>{title}</h1>", unsafe_allow_html=True)

def top_navbar():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("🧰 Input"):
            st.session_state.section = "input"
    with col2:
        if st.button("📋 Specs"):
            st.session_state.section = "tech_specs"
    with col3:
        if st.button("📊 Load"):
            st.session_state.section = "load"
    with col4:
        if st.button("⚖️ Compare"):
            st.session_state.section = "compare"
    with col5:
        if st.button("💰 Cost"):
            st.session_state.section = "cost"

# ───────────────────────────────
# ✅ USER INPUT PAGE
# ───────────────────────────────
def render_user_input_page():
    apply_custom_css()
    show_logo_and_title("EBOSS® User Input")
    top_navbar()

    st.session_state.user_inputs = st.session_state.get("user_inputs", {})
    with st.container():
        cols = st.columns(2)
        with cols[0]:
            st.session_state.user_inputs["model"] = st.selectbox(
                "Model", ["EBOSS 25 kVA", "EBOSS 70 kVA", "EBOSS 125 kVA", "EBOSS 220 kVA", "EBOSS 400 kVA"]
            )
        with cols[1]:
            st.session_state.user_inputs["gen_type"] = st.selectbox(
                "Type", ["Full Hybrid", "Power Module"]
            )

# ───────────────────────────────
# ✅ TECH SPECS PAGE
# ───────────────────────────────
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
        st.markdown(f"<h3 style='color:#81BD47;'>{section}</h3>", unsafe_allow_html=True)
        for label, value in zip(labels, values):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f'<div class="card"><div class="card-label">{label}</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="card"><div class="card-value">{value}</div></div>', unsafe_allow_html=True)

# ───────────────────────────────
# 🧼 PLACEHOLDER PAGES
# ───────────────────────────────
def render_compare_page():
    apply_custom_css()
    show_logo_and_title("Compare Page")
    top_navbar()
    st.info("⚠️ Compare logic not implemented yet.")

def render_cost_analysis_page():
    apply_custom_css()
    show_logo_and_title("Cost Analysis")
    top_navbar()
    st.info("⚠️ Cost logic not implemented yet.")

def render_load_specs_page():
    apply_custom_css()
    show_logo_and_title("Load Specs")
    top_navbar()
    st.info("⚠️ Load specs logic not implemented yet.")

# ───────────────────────────────
# 🚀 ROUTING
# ───────────────────────────────
def main():
    if "section" not in st.session_state:
        st.session_state.section = "input"
    if "user_inputs" not in st.session_state:
        st.session_state.user_inputs = {}

    if st.session_state.section == "input":
        render_user_input_page()
    elif st.session_state.section == "tech_specs":
        render_tech_specs_page()
    elif st.session_state.section == "compare":
        render_compare_page()
    elif st.session_state.section == "cost":
        render_cost_analysis_page()
    elif st.session_state.section == "load":
        render_load_specs_page()

main()

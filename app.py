import streamlit as st
import webbrowser
import math

# Color mappings based on provided hex codes
COLORS = {
    "Asphalt": "#000000",
    "Concrete": "#939598",
    "Charcoal": "#636569",
    "Energy Green": "#81BD47",
    "Alpine White": "#FFFFFF",
    "Light Grey": "#D3D3D3"  # Added for border
}

# EBOSS® model data (adapted from your repo's app.py)
spec_data = {
    "EB 25 kVA": {
        "Maximum Intermittent Output": [("Three-phase", "30 kVA / 24 kW"), ("Single-phase", "20 kVA / 16 kW"), ("Frequency", "60 Hz"), ("Simultaneous voltage", "120/240 (1Φ) • 208/480 (3Φ)"), ("Voltage regulation", "Adjustable"), ("Max. Intermittent amp-load 208V", "70 A / 13.5 kW"), ("Max. Intermittent amp-load 480V", "30 A / 19 kW"), ("Motor start rating for 3 second (208V)", "104 A / 19.5 kW"), ("Motor start rating for 3 second (480V)", "45 A / 29 kW")],
        "Maximum Continuous Output": [("Generator", "Airman SDG25"), ("Generator charge rate", "25 kVA / 20 kW"), ("Three-phase output", "23 kVA / 19 kW"), ("Single-phase output", "20 kVA / 16 kW"), ("Simultaneous voltage", "120/240 (1Φ) • 208/480 (3Φ)"), ("Max. Continuous amp-load @208V", "70 A / 13.5 kW"), ("Max. Continuous amp-load @480V", "30 A / 19 kW")],
        "Technology": [("Battery chemistry", "Lithium Titanate Oxide (LTO)"), ("Battery capacity", "15 kWh"), ("Total battery life or energy throughout", "1,200 mWh"), ("Charge time (no load)", "< 45 min"), ("Inverter output max", "24 kW"), ("Parallel capability", "Available")],
        "Battery Life": [("Battery type", "Lithium Titanate Oxide (LTO)"), ("Est. Cycle life @ 77°F enclosure temp", "90K Cycles at 90% DOD"), ("Est. Cycle life @ 100°F enclosure temp", "80K Cycles at 90% DOD"), ("Battery life (100°F @ 3 kW average load)", "41 Years")],
        "Operating temperatures": [("Inverter cold start temperature (minimum)", "14°F"), ("Running operating temperature", "-22°F to 130°F"), ("Arctic package operating temp. (optional)", "-50°F to 130°F")],
        "Weights & Dimensions": [("L x w x h x (EBOSS® only)", "40” x 48” x 46”"), ("Eboss® weight only", "2,120 lbs"), ("L x w x h (trailer and generator)", "160” x 74” x 75”"), ("Total weight (without/with fuel)", "5100 / 5500 lbs"), ("Integral fuel tank capacity", "51.5 gal")]
    }
    # Add other models as needed
}

# Apply custom CSS for branding, full-screen background, mobile-friendly, and container styles
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/bg.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: {COLORS['Alpine White']};
        font-family: Arial, sans-serif;
        font-size: 16px;
    }}
    .sidebar .sidebar-content {{
        background-color: {COLORS['Asphalt']};
        color: {COLORS['Alpine White']};
    }}
    button {{
        background-color: {COLORS['Energy Green']};
        color: {COLORS['Asphalt']};
        border: 1px solid {COLORS['Charcoal']};
        border-radius: 5px;
        padding: 10px 20px;
        transition: box-shadow 0.3s ease;
    }}
    button:hover {{
        box-shadow: 0 0 10px {COLORS['Energy Green']};
    }}
    .stTextInput > div > div > input, .stSelectbox > div > div > div, .stNumberInput > div > div > input {{
        background-color: {COLORS['Asphalt']};
        color: {COLORS['Alpine White']};
        border: 1px solid {COLORS['Light Grey']};
        border-radius: 5px;
        padding: 8px;
        transition: box-shadow 0.3s ease;
    }}
    .stTextInput > div > div > input:hover, .stSelectbox > div > div > div:hover, .stNumberInput > div > div > input:hover {{
        box-shadow: 0 0 10px {COLORS['Energy Green']};
    }}
    .logo {{
        max-width: 150px; /* Adjusted for mobile friendliness */
        display: block;
        margin: 0 auto;
    }}
    .footer {{
        text-align: center;
        color: {COLORS['Alpine White']};
        padding: 10px;
        background-color: {COLORS['Asphalt']};
        position: fixed;
        bottom: 0;
        width: 100%;
    }}
    .card-header {{
        background-color: {COLORS['Concrete']};
        color: {COLORS['Asphalt']};
        padding: 10px;
        margin-bottom: 5px;
        border-radius: 5px 5px 0 0;
        width: 100%;
        display: block;
    }}
    .card-content {{
        background-color: {COLORS['Alpine White']};
        color: {COLORS['Asphalt']};
        padding: 10px;
        border: 1px solid {COLORS['Charcoal']};
        border-top: none;
        border-radius: 0 0 5px 5px;
    }}
    .two-col-layout {{
        display: flex;
        justify-content: space-between;
        width: 100%;
    }}
    @media (max-width: 768px) {{
        .two-col-layout {{
            flex-direction: column;
        }}
        .stColumn {{
            width: 100% !important;
        }}
        .logo {{
            max-width: 120px; /* Smaller logo on mobile */
        }}
        button, .stTextInput > div > div > input, .stSelectbox > div > div > div, .stNumberInput > div > div > input {{
            width: 100%;
            box-sizing: border-box;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if "user_inputs" not in st.session_state:
    st.session_state.user_inputs = {
        "eboss_model": "",
        "eboss_type": "",
        "power_module_gen_size": "",
        "max_continuous_load": 0.0,
        "max_peak_load": 0.0,
        "units": "kW",
        "voltage": "480",
        "actual_continuous_load": 0.0,
        "actual_peak_load": 0.0,
        "job_name": ""
    }
if "show_calculator" not in st.session_state:
    st.session_state.show_calculator = False
if "selected_option" not in st.session_state:
    st.session_state.selected_option = "Select EBOSS® Model"
if "recommended_model" not in st.session_state:
    st.session_state.recommended_model = ""
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Corporate logo centered
st.image("https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/ANA-ENERGY-LOGO-HORIZONTAL-WHITE-GREEN.png", use_column_width=False, width=150, output_format="PNG", caption="ANA Logo")  # Corrected logo URL

# Page title
st.title("EBOSS® Size & Spec Tool")

# Navbar for other pages
navbar_pages = ["Home", "Technical Specs", "Load Based Specs", "EBOSS® to Standard Comparison", "Cost Analysis", "Parallel Calculator"]
if st.session_state.show_calculator:
    st.session_state.page = st.radio("", navbar_pages, horizontal=True, index=navbar_pages.index(st.session_state.page))
else:
    st.session_state.page = "Home"

if st.session_state.page == "Home":
    # Radio buttons for EBOSS® option
    st.session_state.selected_option = st.radio("Choose EBOSS® Configuration Option:", ("Select EBOSS® Model", "Get Recommended EBOSS® Model Based on Load"))

    # Text
    st.write("Provide your load details, choose a page or tool, and press Calculate to start.")

    # User input section with 3 columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("EBOSS®")
        if st.session_state.selected_option == "Select EBOSS® Model":
            st.session_state.user_inputs["eboss_model"] = st.selectbox("EBOSS® Model", options=list(spec_data.keys()))
            st.session_state.user_inputs["eboss_type"] = st.selectbox("EBOSS® Type", options=["Full Hybrid", "Power Module"])
            if st.session_state.user_inputs["eboss_type"] == "Power Module":
                st.session_state.user_inputs["power_module_gen_size"] = st.selectbox("Power Module Generator Size", options=["25 kVA", "70 kVA", "125 kVA", "220 kVA", "400 kVA"])

    with col2:
        st.header("Load")
        st.session_state.user_inputs["max_continuous_load"] = st.number_input("Max Continuous Load", min_value=0.0, step=0.1)
        st.session_state.user_inputs["max_peak_load"] = st.number_input("Max Peak Load", min_value=0.0, step=0.1)

    with col3:
        st.header("Units")
        col3a, col3b = st.columns(2)
        with col3a:
            st.session_state.user_inputs["units"] = st.selectbox("Units", options=["kW", "Amps"])
        with col3b:
            st.session_state.user_inputs["voltage"] = st.selectbox("Voltage", options=["120", "240", "208", "480"])

        # Calculated Actual Load with labels
        st.header("Actual Load")
        col3a, col3b = st.columns(2)
        with col3a:
            st.subheader("Actual Continuous Load")
            st.write(f"{st.session_state.user_inputs['actual_continuous_load']:.2f} kW")

        with col3b:
            st.subheader("Actual Peak Load")
            st.write(f"{st.session_state.user_inputs['actual_peak_load']:.2f} kW")

    # Job name input
    st.session_state.user_inputs["job_name"] = st.text_input("Job Name", value=st.session_state.user_inputs["job_name"])

    # Calculate button with modal logic
    if st.button("Calculate"):
        if st.session_state.selected_option == "Get Recommended EBOSS® Model Based on Load":
            # Placeholder for recommended model logic (to be added later)
            st.session_state.recommended_model = "EB 70 kVA"  # Example
            st.session_state.user_inputs["eboss_model"] = st.session_state.recommended_model
            with st.dialog("Recommended EBOSS® Configuration"):
                st.write(f"Recommended EBOSS® Model: {st.session_state.user_inputs['eboss_model']}")
                st.session_state.user_inputs["eboss_type"] = st.selectbox("Select Type of EBOSS®", options=["Full Hybrid", "Power Module"])
                if st.session_state.user_inputs["eboss_type"] == "Power Module":
                    st.session_state.user_inputs["power_module_gen_size"] = st.selectbox("Power Module Generator Size", options=["25 kVA", "70 kVA", "125 kVA", "220 kVA", "400 kVA"])
                if st.button("Go"):
                    st.session_state.show_calculator = True
                    st.rerun()
        else:  # Select EBOSS® Model
            with st.dialog("EBOSS® Configuration"):
                st.write("Confirm your selected EBOSS® configuration:")
                st.write(f"EBOSS® Model: {st.session_state.user_inputs['eboss_model']}")
                st.write(f"EBOSS® Type: {st.session_state.user_inputs['eboss_type']}")
                if st.session_state.user_inputs["eboss_type"] == "Power Module":
                    st.write(f"Power Module Generator Size: {st.session_state.user_inputs['power_module_gen_size']}")
                st.write(f"Max Continuous Load: {st.session_state.user_inputs['max_continuous_load']} {st.session_state.user_inputs['units']}")
                st.write(f"Max Peak Load: {st.session_state.user_inputs['max_peak_load']} {st.session_state.user_inputs['units']}")
                st.write(f"Actual Continuous Load: {st.session_state.user_inputs['actual_continuous_load']:.2f} kW")
                st.write(f"Actual Peak Load: {st.session_state.user_inputs['actual_peak_load']:.2f} kW")
                st.write(f"Job Name: {st.session_state.user_inputs['job_name']}")
                if st.button("Go"):
                    st.session_state.show_calculator = True
                    st.rerun()

if st.session_state.show_calculator:
    st.write("Select a page to view calculations")
    st.session_state.page = st.radio("", navbar_pages, horizontal=True, index=navbar_pages.index(st.session_state.page))

# Display selected page content
if st.session_state.page == "Technical Specs":
    st.header("Technical Specifications for the " + st.session_state.user_inputs["eboss_model"] + " " + st.session_state.user_inputs["eboss_type"] + (" using a " + st.session_state.user_inputs["power_module_gen_size"] + " generator" if st.session_state.user_inputs["eboss_type"] == "Power Module" else ""))
    if st.button("Change EBOSS®"):
        st.session_state.show_calculator = False
        st.rerun()

    # Two-column card layout with section headers
    col1, col2 = st.columns(2)
    section_headers = ["Maximum Intermittent Output", "Maximum Continuous Output", "Technology", "Battery Life", "Operating temperatures", "Weights & Dimensions"]
    spec_names = [
        "Three-phase", "Single-phase", "Frequency", "Simultaneous voltage", "Voltage regulation",
        "Max. Intermittent amp-load 208V", "Max. Intermittent amp-load 480V", "Motor start rating for 3 second (208V)",
        "Motor start rating for 3 second (480V)", "Generator", "Generator charge rate", "Three-phase output",
        "Single-phase output", "Simultaneous voltage", "Max. Continuous amp-load @208V", "Max. Continuous amp-load @480V",
        "Battery chemistry", "Battery capacity", "Total battery life or energy throughout", "Charge time (no load)",
        "Inverter output max", "Parallel capability", "Battery type", "Est. Cycle life @ 77°F enclosure temp",
        "Est. Cycle life @ 100°F enclosure temp", "Battery life (100°F @ 3 kW average load)", "Inverter cold start temperature (minimum)",
        "Running operating temperature", "Arctic package operating temp. (optional)", "L x w x h x (EBOSS® only)",
        "Eboss® weight only", "L x w x h (trailer and generator)", "Total weight (without/with fuel)", "Integral fuel tank capacity"
    ]

    model = st.session_state.user_inputs["eboss_model"]
    if model in spec_data:
        specs = []
        for section in spec_data[model].values():
            specs.extend(section)
        header_index = 0
        for i in range(len(spec_names)):
            if header_index < len(section_headers) and i % (len(spec_names) // len(section_headers)) == 0:
                with col1:
                    st.markdown(f'<div class="card-header" style="grid-column: span 2;">{section_headers[header_index]}</div>', unsafe_allow_html=True)
                header_index += 1
            with col1:
                st.markdown(f'<div class="card-content">{spec_names[i]}</div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="card-content">{specs[i][1]}</div>', unsafe_allow_html=True)
    else:
        st.write("No specs available for selected model.")

elif st.session_state.page == "Load Based Specs":
    st.header("Load Based Specs")
    # Placeholder for load based specs

elif st.session_state.page == "EBOSS® to Standard Comparison":
    st.header("EBOSS® to Standard Comparison")
    # Placeholder for comparison

elif st.session_state.page == "Cost Analysis":
    st.header("Cost Analysis")
    # Placeholder for cost analysis

elif st.session_state.page == "Parallel Calculator":
    st.header("Parallel Calculator")
    # Placeholder for parallel calculator

# Footer with links
st.markdown(f"""
<div class="footer">
EBOSS® Size & Spec Tool | 
<a href="#" onclick="window.open('https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform?usp=header', '_blank')">Request Demo</a> |
<a href="#" onclick="window.open('https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform?usp=header', '_blank')">Request Training</a> |
<a href="#" onclick="window.open('https://youtu.be/0Om2qO-zZfM?si=XnLKJ_SfyKqqUI-g', '_blank')">Learn how the EBOSS® works</a>
</div>
""", unsafe_allow_html=True)

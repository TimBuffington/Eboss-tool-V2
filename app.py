import streamlit as st
import webbrowser
import math

# Color mappings based on provided hex codes
COLORS = {
    "Asphalt": "#000000",
    "Concrete": "#939598",
    "Charcoal": "#636569",
    "Energy Green": "#81BD47",
    "Alpine White": "#FFFFFF"
}

# EBOSS® model data (adapted from your repo's app.py)
spec_data = {
    "EB 25 kVA": {
        "Maximum Intermittent Load": [("Three-phase", "30 kVA / 24 kW"), ("Single-phase", "20 kVA / 16 kW"), ("Frequency", "60 Hz"), ("Simultaneous voltage", "Yes 120V / 240V / 208V / 480V"), ("Voltage regulation", "Adjustable"), ("Max. Intermittent 208V", "70 A / 20 kW"), ("Max. Intermittent amp-load 480V", "30 A / 25 kW"), ("Motor start rating - 3 second 208V", "104 A / 30 kW"), ("Motor start rating - 3 second 480V", "45 A / 37 kW")],
        "Maximum Continuous Load": [("Generator Size", "25 kVA / 20 kW"), ("Three-phase output", "23 kVA / 19 kW"), ("Single-phase output", "20 kVA / 16 kW"), ("Max. Continuous 208V", "64 A / 18.5 kW"), ("Max. Continuous amp-load 480V", "28 A / 23 kW")],
        "Battery Specs": [("Battery Capacity", "15 kWh"), ("Battery Chemistry", "Lithium Iron Phosphate"), ("Battery Life Cycles", "> 6,000"), ("Battery Warranty", "10 years")],
        "Engine Specs & Fuel Use": [("Engine Model", "Yanmar 3TNV88C"), ("Fuel Type", "Diesel"), ("Fuel Tank Capacity", "40 gal"), ("Runtime at 100% Load", "30 hrs"), ("Runtime at 50% Load", "50 hrs"), ("Fuel Consumption", "0.5 gal/hr at 50% load")],
        "System Specs": [("Weight", "4,500 lbs"), ("Dimensions", "120\" L x 48\" W x 72\" H"), ("Noise Level", "62 dBA at 23 ft"), ("Enclosure", "Aluminum, powder coated")],
        "Savings": [("Fuel Savings vs Diesel", "83%"), ("CO2 Reduction", "314.73 metric tons/year")]
    },
    "EB 70 kVA": {
        "Maximum Intermittent Load": [("Three-phase", "70 kVA / 56 kW"), ("Single-phase", "46 kVA / 37 kW"), ("Frequency", "60 Hz"), ("Simultaneous voltage", "Yes 120V / 240V / 208V / 480V"), ("Voltage regulation", "Adjustable"), ("Max. Intermittent 208V", "194 A / 56 kW"), ("Max. Intermittent amp-load 480V", "84 A / 70 kW"), ("Motor start rating - 3 second 208V", "291 A / 84 kW"), ("Motor start rating - 3 second 480V", "126 A / 105 kW")],
        "Maximum Continuous Load": [("Generator Size", "45 kVA / 36 kW"), ("Three-phase output", "41 kVA / 33 kW"), ("Single-phase output", "38 kVA / 30 kW"), ("Max. Continuous 208V", "114 A / 33 kW"), ("Max. Continuous amp-load 480V", "49 A / 41 kW")],
        "Battery Specs": [("Battery Capacity", "45 kWh"), ("Battery Chemistry", "Lithium Iron Phosphate"), ("Battery Life Cycles", "> 6,000"), ("Battery Warranty", "10 years")],
        "Engine Specs & Fuel Use": [("Engine Model", "Yanmar 4TNV98C"), ("Fuel Type", "Diesel"), ("Fuel Tank Capacity", "100 gal"), ("Runtime at 100% Load", "35 hrs"), ("Runtime at 50% Load", "70 hrs"), ("Fuel Consumption", "1.0 gal/hr at 50% load")],
        "System Specs": [("Weight", "6,000 lbs"), ("Dimensions", "144\" L x 60\" W x 80\" H"), ("Noise Level", "65 dBA at 23 ft"), ("Enclosure", "Aluminum, powder coated")],
        "Savings": [("Fuel Savings vs Diesel", "75%"), ("CO2 Reduction", "250 metric tons/year")]
    }
    # Add other models as needed
}

# Apply custom CSS for branding and full-screen background
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://raw.githubusercontent.com/timbuffington/Eboss-tool-V2/main/images/APP_BACKGROUND.jpeg");
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
    .stTextInput > div > div > input {{
        background-color: {COLORS['Concrete']};
        color: {COLORS['Asphalt']};
        border: 1px solid {COLORS['Charcoal']};
        border-radius: 5px;
        padding: 8px;
        transition: box-shadow 0.3s ease;
    }}
    .stTextInput > div > div > input:hover {{
        box-shadow: 0 0 10px {COLORS['Energy Green']};
    }}
    .stSelectbox > div > div > div {{
        background-color: {COLORS['Concrete']};
        color: {COLORS['Asphalt']};
        border: 1px solid {COLORS['Charcoal']};
        border-radius: 5px;
        padding: 8px;
        transition: box-shadow 0.3s ease;
    }}
    .stSelectbox > div > div > div:hover {{
        box-shadow: 0 0 10px {COLORS['Energy Green']};
    }}
    .stNumberInput > div > div > input {{
        background-color: {COLORS['Concrete']};
        color: {COLORS['Asphalt']};
        border: 1px solid {COLORS['Charcoal']};
        border-radius: 5px;
        padding: 8px;
        transition: box-shadow 0.3s ease;
    }}
    .stNumberInput > div > div > input:hover {{
        box-shadow: 0 0 10px {COLORS['Energy Green']};
    }}
    .logo {{
        max-width: 200px;
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
st.image("https://raw.githubusercontent.com/timbuffington/Eboss-tool-V2/main/images/ANA-ENERGY-LOGO-HORIZONTAL-WHITE-GREEN.png", use_column_width=False, width=200, output_format="PNG")

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
            st.session_state.user_inputs["eboss_type"] = st.radio("EBOSS® Type", options=["Full Hybrid", "Power Module"])
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

        # Calculated Actual Load
        def calculate_actual_load(load, units, voltage):
            if units == "kW":
                return load
            elif units == "Amps":
                pf = 0.8  # Power Factor
                return (load * float(voltage) * 1.732 * pf) / 1000  # sqrt(3) = 1.732
            return 0.0

        st.session_state.user_inputs["actual_continuous_load"] = calculate_actual_load(
            st.session_state.user_inputs["max_continuous_load"],
            st.session_state.user_inputs["units"],
            st.session_state.user_inputs["voltage"]
        )
        st.write(f"Actual Continuous Load: {st.session_state.user_inputs['actual_continuous_load']:.2f} kW")

        st.session_state.user_inputs["actual_peak_load"] = calculate_actual_load(
            st.session_state.user_inputs["max_peak_load"],
            st.session_state.user_inputs["units"],
            st.session_state.user_inputs["voltage"]
        )
        st.write(f"Actual Peak Load: {st.session_state.user_inputs['actual_peak_load']:.2f} kW")

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
                st.session_state.user_inputs["eboss_type"] = st.radio("Select Type of EBOSS®", options=["Full Hybrid", "Power Module"])
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
    st.header("Technical Specs")
    if st.session_state.user_inputs["eboss_model"]:
        model = st.session_state.user_inputs["eboss_model"]
        if model in spec_data:
            for section, specs in spec_data[model].items():
                st.subheader(section)
                for label, value in specs:
                    st.write(f"{label}: {value}")
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

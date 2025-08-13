import streamlit as st
import webbrowser
import math
import logging
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Starting EBOSS® Streamlit app...")

# Color mappings based on provided hex codes
COLORS = {
    "Asphalt": "#000000",
    "Concrete": "#939598",
    "Charcoal": "#636569",
    "Energy Green": "#81BD47",
    "Alpine White": "#FFFFFF",
    "Light Grey": "#D3D3D3"
}

st.markdown(
    f"""
    <style>
    /* ===== App Background ===== */
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
    /* ===== Buttons (Streamlit + Link Buttons) ===== */
    button, .stButton button, .stLinkButton > a {{
        background-color: {COLORS['Asphalt']} !important;
        color: {COLORS['Energy Green']} !important;
        border: 2px solid {COLORS['Alpine White']} !important;
        font-family: Arial, sans-serif;
        font-size: 16px;
        font-weight: bold !important;
        text-shadow: 0 0 6px {COLORS['Energy Green']};
        border-radius: 6px;
        padding: 6px 10px;
        transition: box-shadow 0.3s ease, transform 0.2s ease;
        width: 100%;
        margin: 0px 0;
    }}
    button:hover, .stButton button:hover, .stLinkButton > a:hover {{
        box-shadow: 0 0 30px {COLORS['Energy Green']};
        transform: translateY(-1px);
    }}

    /* ===== Button Layout Containers ===== */
    .button-container {{
        display: flex;
        justify-content: center;
        gap: 0px;
        width: 100%;
    }}
    .button-block {{
        flex: 1;
        max-width: 300px;
    }}

    /* ===== Inputs ===== */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input {{
        background-color: {COLORS['Asphalt']};
        color: {COLORS['Alpine White']};
        border: 1px solid {COLORS['Light Grey']};
        border-radius: 5px;
        padding: 8px;
        transition: box-shadow 0.3s ease;
    }}
    .stTextInput > div > div > input:hover,
    .stSelectbox > div > div > div:hover,
    .stNumberInput > div > div > input:hover {{
        box-shadow: 0 0 10px {COLORS['Energy Green']};
    }}

    /* ===== Logo ===== */
    .logo-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0x 0;
        height: 0px;
    }}
    .logo {{
        max-width: autopx;
        display: block;
    }}

    /* ===== Footer ===== */
    .footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: black;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px;
    }}

    /* ===== Message & Centered Elements ===== */
    .message-text {{
        font-size: 1.5em;
        text-align: center;
        transition: box-shadow 0.3s ease;
        padding: 10px;
    }}
    .message-text:hover {{
        box-shadow: 0 0 10px {COLORS['Energy Green']};
    }}
    .centered-radio {{
        display: flex;
        justify-content: center;
        width: 100%;
    }}
    .centered-button {{
        display: flex;
        justify-content: center;
        width: 100%;
    }}

    /* ===== Mobile Tweaks ===== */
    @media (max-width: 768px) {{
        .logo {{ max-width: 480px; }}
        .logo-container {{ height: 120px; }}
        .button-container {{
            flex-direction: column;
            gap: 5px;
        }}
        .button-block {{ max-width: 100%; }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# EBOSS Load Calculation Reference Data from file 2
EBOSS_LOAD_REFERENCE = {
    "battery_capacities": {
        "EB25 kVA": 15,
        "EB70 kVA": 25,
        "EB125 kVA": 50,
        "EB220 kVA": 75,
        "EB400 kVA": 125
    },
    "generator_kva_hybrid": {
        "EB25 kVA": 25,
        "EB70 kVA": 45,
        "EB125 kVA": 65,
        "EB220 kVA": 125,
        "EB400 kVA": 220
    },
    "generator_sizes": {
        25: {"eboss_model": "EB25 kVA", "pm_charge_rate": 18.5, "fh_charge_rate": 19.5, "max_charge_rate": 20, "kwh": 15, "gen_kw": 20},
        45: {"eboss_model": "EB70 kVA", "pm_charge_rate": 33, "fh_charge_rate": 36, "max_charge_rate": 45, "kwh": 25, "gen_kw": 36},
        65: {"eboss_model": "EB125 kVA", "pm_charge_rate": 48, "fh_charge_rate": 52, "max_charge_rate": 65, "kwh": 50, "gen_kw": 52},
        125: {"eboss_model": "EB220 kVA", "pm_charge_rate": 96, "fh_charge_rate": 100, "max_charge_rate": 125, "kwh": 75, "gen_kw": 100},
        220: {"eboss_model": "EB400 kVA", "pm_charge_rate": 166, "fh_charge_rate": 176, "max_charge_rate": 220, "kwh": 125, "gen_kw": 176}
    },
    "gph_interpolation": {
        25: {"25%": 0.67, "50%": 0.94, "75%": 1.26, "100%": 1.62},
        45: {"25%": 1.04, "50%": 1.60, "75%": 2.20, "100%": 2.03},
        70: {"25%": 1.70, "50%": 2.60, "75%": 3.50, "100%": 4.40},
        125: {"25%": 2.60, "50%": 4.10, "75%": 5.60, "100%": 7.10},
        220: {"25%": 4.60, "50%": 6.90, "75%": 9.40, "100%": 12.00},
        400: {"25%": 7.70, "50%": 12.20, "75%": 17.30, "100%": 22.50}
    }
}

# Standard Generator Data from file 2
STANDARD_GENERATOR_DATA = {
    "25 kVA / 20 kW": {
        "kva": 25, "kw": 20,
        "fuel_consumption_gph": {"50%": 0.90, "75%": 1.30, "100%": 1.60},
        "noise_level_db": 68, "dimensions": "L:48\" W:24\" H:30\"", "weight_lbs": 650,
        "fuel_tank_gal": 12, "runtime_at_50_load": 13.3, "co2_per_gal": 22.4
    },
    "45 kVA / 36 kW": {
        "kva": 45, "kw": 36,
        "fuel_consumption_gph": {"50%": 2.30, "75%": 3.20, "100%": 4.00},
        "noise_level_db": 72, "dimensions": "L:60\" W:28\" H:36\"", "weight_lbs": 1200,
        "fuel_tank_gal": 25, "runtime_at_50_load": 10.9, "co2_per_gal": 22.4
    },
    "65 kVA / 52 kW": {
        "kva": 65, "kw": 52,
        "fuel_consumption_gph": {"50%": 2.90, "75%": 3.80, "100%": 4.80},
        "noise_level_db": 75, "dimensions": "L:72\" W:32\" H:42\"", "weight_lbs": 1800,
        "fuel_tank_gal": 40, "runtime_at_50_load": 13.8, "co2_per_gal": 22.4
    },
    "125 kVA / 100 kW": {
        "kva": 125, "kw": 100,
        "fuel_consumption_gph": {"50%": 5.00, "75%": 7.10, "100%": 9.10},
        "noise_level_db": 78, "dimensions": "L:96\" W:36\" H:48\"", "weight_lbs": 3200,
        "fuel_tank_gal": 75, "runtime_at_50_load": 15.0, "co2_per_gal": 22.4
    },
    "220 kVA / 176 kW": {
        "kva": 220, "kw": 176,
        "fuel_consumption_gph": {"50%": 8.80, "75%": 12.50, "100%": 16.60},
        "noise_level_db": 82, "dimensions": "L:120\" W:48\" H:60\"", "weight_lbs": 5500,
        "fuel_tank_gal": 125, "runtime_at_50_load": 14.2, "co2_per_gal": 22.4
    },
    "400 kVA / 320 kW": {
        "kva": 400, "kw": 320,
        "fuel_consumption_gph": {"50%": 14.90, "75%": 21.30, "100%": 28.60},
        "noise_level_db": 85, "dimensions": "L:144\" W:60\" H:72\"", "weight_lbs": 8800,
        "fuel_tank_gal": 200, "runtime_at_50_load": 13.4, "co2_per_gal": 22.4
    }
}

# Additional STANDARD_GENERATOR_DATA from file 2 (merged)
STANDARD_GENERATOR_DATA.update({
    "25 kVA / 20 kW": {
        "kw": 20,
        "fuel_consumption_gph": {"50%": 1.2, "75%": 1.7, "100%": 2.3},
        "fuel_tank_gal": 38,
        "co2_per_gal": 22.4,
        "noise_level_db": 75,
        "dimensions": "60\" x 24\" x 36\"",
        "weight_lbs": 1850
    },
    # ... (similar for other sizes, assuming merge by overwriting if needed)
})

# Functions from file 2
def interpolate_gph(generator_kva, load_percent):
    if load_percent > 1:
        load_percent = load_percent / 100
    gph_data_map = EBOSS_LOAD_REFERENCE["gph_interpolation"]
    if generator_kva not in gph_data_map:
        available_sizes = list(gph_data_map.keys())
        closest_size = min(available_sizes, key=lambda x: abs(x - generator_kva))
        gph_data = gph_data_map[closest_size]
    else:
        gph_data = gph_data_map[generator_kva]
    load_points = [0.25, 0.50, 0.75, 1.00]
    gph_values = [gph_data["25%"], gph_data["50%"], gph_data["75%"], gph_data["100%"]]
    load_percent = max(0.25, min(1.00, load_percent))
    if load_percent <= 0.25:
        return gph_values[0]
    elif load_percent >= 1.00:
        return gph_values[3]
    for i in range(len(load_points) - 1):
        if load_points[i] <= load_percent <= load_points[i + 1]:
            x1, x2 = load_points[i], load_points[i + 1]
            y1, y2 = gph_values[i], gph_values[i + 1]
            interpolated_gph = y1 + (load_percent - x1) * (y2 - y1) / (x2 - x1)
            return round(interpolated_gph, 4)
    return 0

def calculate_charge_rate(eboss_model, eboss_type, generator_kva=None, custom_rate=None):
    if custom_rate:
        return custom_rate
    generator_kw = 0
    if eboss_type == "Full Hybrid":
        hybrid_kva = EBOSS_LOAD_REFERENCE["generator_kva_hybrid"].get(eboss_model, 0)
        generator_kw = hybrid_kva * 0.8
    elif eboss_type == "Power Module" and generator_kva:
        gen_kva = float(generator_kva.replace("kVA", ""))
        generator_kw = gen_kva * 0.8
    if eboss_type == "Full Hybrid":
        charge_rate = generator_kw * 0.98
    elif eboss_type == "Power Module":
        charge_rate = generator_kw * 0.90 * 0.98
    else:
        charge_rate = 0
    return round(charge_rate, 1)

def get_max_charge_rate(eboss_model, eboss_type, generator_kva=None):
    model_max_charge_rates = {
        "EB25 kVA": 20,
        "EB70 kVA": 45,
        "EB125 kVA": 65,
        "EB220 kVA": 125,
        "EB400 kVA": 220
    }
    model_max = model_max_charge_rates.get(eboss_model, 0)
    generator_kw = 0
    if eboss_type == "Full Hybrid":
        hybrid_kva = EBOSS_LOAD_REFERENCE["generator_kva_hybrid"].get(eboss_model, 0)
        generator_kw = hybrid_kva * 0.8
    elif eboss_type == "Power Module" and generator_kva:
        gen_kva = float(generator_kva.replace("kVA", ""))
        generator_kw = gen_kva * 0.8
    generator_98_percent = generator_kw * 0.98
    if model_max > 0 and generator_98_percent > 0:
        max_charge_rate = min(model_max, generator_98_percent)
    elif model_max > 0:
        max_charge_rate = model_max
    elif generator_98_percent > 0:
        max_charge_rate = generator_98_percent
    else:
        max_charge_rate = 0
    return round(max_charge_rate, 1)

def calculate_standard_generator_specs(standard_generator_size, continuous_load, max_peak_load):
    if not standard_generator_size or standard_generator_size not in STANDARD_GENERATOR_DATA:
        return {}
    gen_data = STANDARD_GENERATOR_DATA[standard_generator_size]
    gen_kw = gen_data["kw"]
    engine_load_percent = (continuous_load / gen_kw * 100) if gen_kw > 0 else 0
    load_percentage = continuous_load / gen_kw if gen_kw > 0 else 0
    fuel_gph_data = gen_data["fuel_consumption_gph"]
    if load_percentage <= 0.5:
        fuel_per_hour = fuel_gph_data["50%"]
    elif load_percentage <= 0.75:
        fuel_per_hour = fuel_gph_data["75%"]
    else:
        fuel_per_hour = fuel_gph_data["100%"]
    fuel_per_day = fuel_per_hour * 24
    fuel_per_week = fuel_per_day * 7
    fuel_per_month = fuel_per_day * 30
    co2_per_day = fuel_per_day * gen_data["co2_per_gal"]
    runtime_per_day = 24.0
    tank_runtime = gen_data["fuel_tank_gal"] / fuel_per_hour if fuel_per_hour > 0 else 0
    return {
        "generator_type": "Standard Diesel Generator",
        "generator_size": standard_generator_size,
        "engine_load_percent": engine_load_percent,
        "continuous_load_percent": load_percentage * 100,
        "fuel_consumption_gph": fuel_per_hour,
        "fuel_per_hour": fuel_per_hour,
        "fuel_per_day": fuel_per_day,
        "fuel_per_week": fuel_per_week,
        "fuel_per_month": fuel_per_month,
        "co2_per_day": co2_per_day,
        "runtime_per_day": runtime_per_day,
        "tank_runtime_hours": tank_runtime,
        "noise_level": gen_data["noise_level_db"],
        "dimensions": gen_data["dimensions"],
        "weight_lbs": gen_data["weight_lbs"],
        "fuel_tank_capacity": gen_data["fuel_tank_gal"]
    }

# Additional functions from file 2 (calculate_load_specs, etc.) - adding placeholder for truncated ones
def calculate_load_specs(eboss_model, eboss_type, continuous_load, max_peak_load, generator_kva=None, custom_charge_rate=None):
    # Implementation from file 2 (using provided code)
    generator_kw_mapping = {
        "EB25 kVA": 14.5,
        "EB70 kVA": 24.5,
        "EB125 kVA": 49,
        "EB220 kVA": 74,
        "EB400 kVA": 125
    }
    model_capacity = generator_kw_mapping.get(eboss_model, 0)
    generator_data = None
    if generator_kva:
        gen_size = int(generator_kva.replace("kVA", ""))
        generator_data = EBOSS_LOAD_REFERENCE["generator_sizes"].get(gen_size)
    peak_utilization = (max_peak_load / model_capacity * 100) if model_capacity > 0 else 0
    continuous_utilization = (continuous_load / model_capacity * 100) if model_capacity > 0 else 0
    charge_rate = calculate_charge_rate(eboss_model, eboss_type, generator_kva, custom_charge_rate)
    fuel_consumption = None
    engine_load_percent = 0
    # ... (complete based on truncated code, assuming logic for fuel and load)
    return {"peak_utilization": peak_utilization, "continuous_utilization": continuous_utilization, "charge_rate": charge_rate, "engine_load_percent": engine_load_percent}  # Placeholder

# Initialize session state from file 1, adding from file 2 where it makes sense
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
    st.session_state.selected_option = None
if "recommended_model" not in st.session_state:
    st.session_state.recommended_model = ""
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Add session states from file 2
if 'show_cost_analysis' not in st.session_state:
    st.session_state.show_cost_analysis = False
if 'show_cost_dialog' not in st.session_state:
    st.session_state.show_cost_dialog = False
if 'cost_standard_generator' not in st.session_state:
    st.session_state.cost_standard_generator = None
if 'pm_charge_enabled' not in st.session_state:
    st.session_state.pm_charge_enabled = False

# Homepage from file 1 (untouched)
# Corporate logo top center with container
st.markdown("<div class='logo-container'>", unsafe_allow_html=True)
try:
    st.image("https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/logo.png", use_container_width=False, width=600, output_format="PNG")
except Exception as e:
    st.error(f"Logo failed to load: {e}. Please verify the file at https://github.com/TimBuffington/Eboss-tool-V2/tree/main/assets/logo.png.")
st.markdown("</div>", unsafe_allow_html=True)

# Page title centered under logo
st.markdown("<h1 style='text-align: center;'>EBOSS® Size & Spec Tool</h1>", unsafe_allow_html=True)

# Buttons for Google Docs and YouTube, centered horizontally with minimal gap
with st.container():
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    col_buttons = st.columns(3)
    with col_buttons[0]:
        st.markdown("<div class='button-block'>", unsafe_allow_html=True)
        st.link_button("Request Demo", url="https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform?usp=header")
        st.markdown("</div>", unsafe_allow_html=True)
    with col_buttons[1]:
        st.markdown("<div class='button-block'>", unsafe_allow_html=True)
        st.link_button("Request Training", url="https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform?usp=header")
        st.markdown("</div>", unsafe_allow_html=True)
    with col_buttons[2]:
        st.markdown("<div class='button-block'>", unsafe_allow_html=True)
        st.link_button("Learn how the EBOSS® works", url="https://youtu.be/0Om2qO-zZfM?si=XnLKJ_SfyKqqUI-g")
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

col_buttons = st.columns(3, gap="small")
st.markdown(f"<div class='message-text'>Please Select a Configuration</div>", unsafe_allow_html=True)

st.markdown("<div class='centered-radio'>", unsafe_allow_html=True)
selected_option = st.radio(" ", ("Select a EBOSS® Model", "Use Load Based Suggested EBOSS® Model"), horizontal=True)
st.session_state.selected_option = selected_option
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='centered-button'>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3, gap="small")
with c2:
    enter_clicked = st.button("Enter Data", key="enter_data_button")
st.markdown("</div>", unsafe_allow_html=True)

if enter_clicked:
    try:
        print("Entering dialog...")

        if st.session_state.selected_option == "Use Load Based Suggested EBOSS® Model":
            st.session_state.recommended_model = "EB 70 kVA"  # Placeholder

            @st.dialog("Recommended EBOSS® Configuration")
            def show_recommended_dialog():
                st.markdown(f"**Recommended EBOSS® Model:** {st.session_state.recommended_model}")
                col1, col2, col3 = st.columns(3)
                with col2:
                    st.number_input("Max Continuous Load", min_value=0.0, step=0.1, key="max_continuous_load_input")
                    st.number_input("Max Peak Load", min_value=0.0, step=0.1, key="max_peak_load_input")
                    st.selectbox("Units", options=["kW", "Amps"], key="units_input")
                    st.selectbox("Voltage", options=["120", "240", "208", "480"], key="voltage_input")

                if st.button("Launch Tool", key="launch_tool_recommended"):
                    max_continuous_load = float(st.session_state.get("max_continuous_load_input", 0.0))
                    max_peak_load = float(st.session_state.get("max_peak_load_input", 0.0))
                    units = st.session_state.get("units_input", "kW")
                    voltage = st.session_state.get("voltage_input", "480")

                    if units == "Amps":
                        pf = 0.8
                        st.session_state.user_inputs["actual_continuous_load"] = (max_continuous_load * float(voltage) * 1.732 * pf) / 1000
                        st.session_state.user_inputs["actual_peak_load"] = (max_peak_load * float(voltage) * 1.732 * pf) / 1000
                    else:
                        st.session_state.user_inputs["actual_continuous_load"] = max_continuous_load
                        st.session_state.user_inputs["actual_peak_load"] = max_peak_load

                    st.session_state.user_inputs["max_continuous_load"] = max_continuous_load
                    st.session_state.user_inputs["max_peak_load"] = max_peak_load
                    st.session_state.user_inputs["units"] = units
                    st.session_state.user_inputs["voltage"] = voltage
                    st.session_state.show_calculator = True
                    st.session_state.page = "Tool Selection"
                    st.rerun()

            show_recommended_dialog()

        else:
            @st.dialog("EBOSS® Configuration")
            def show_config_dialog():
                st.markdown("Enter your EBOSS® configuration:")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.selectbox("EBOSS® Model", options=["EB 25 kVA", "EB 70 kVA", "EB 125 kVA", "EB 220 kVA", "EB 400 kVA"], key="eboss_model_input")
                    st.selectbox("EBOSS® Type", options=["Full Hybrid", "Power Module"], key="eboss_type_input")
                    if st.session_state.get("eboss_type_input", "") == "Power Module":
                        st.selectbox("Power Module Generator Size", options=["25 kVA", "70 kVA", "125 kVA", "220 kVA", "400 kVA"], key="power_module_gen_size_input")
                with col2:
                    st.number_input("Max Continuous Load", min_value=0.0, step=0.1, key="max_continuous_load_input")
                    st.number_input("Max Peak Load", min_value=0.0, step=0.1, key="max_peak_load_input")
                with col3:
                    st.selectbox("Units", options=["kW", "Amps"], key="units_input")
                    st.selectbox("Voltage", options=["120", "240", "208", "480"], key="voltage_input")

                if st.button("Launch Tool", key="launch_tool_select"):
                    st.session_state.user_inputs["eboss_model"] = st.session_state.get("eboss_model_input", "")
                    st.session_state.user_inputs["eboss_type"] = st.session_state.get("eboss_type_input", "")
                    st.session_state.user_inputs["power_module_gen_size"] = st.session_state.get("power_module_gen_size_input", "")
                    st.session_state.user_inputs["max_continuous_load"] = st.session_state.get("max_continuous_load_input", 0.0)
                    st.session_state.user_inputs["max_peak_load"] = st.session_state.get("max_peak_load_input", 0.0)
                    st.session_state.user_inputs["units"] = st.session_state.get("units_input", "kW")
                    st.session_state.user_inputs["voltage"] = st.session_state.get("voltage_input", "480")

                    if st.session_state.user_inputs["units"] == "Amps":
                        pf = 0.8
                        st.session_state.user_inputs["actual_continuous_load"] = (st.session_state.user_inputs["max_continuous_load"] * float(st.session_state.user_inputs["voltage"]) * 1.732 * pf) / 1000
                        st.session_state.user_inputs["actual_peak_load"] = (st.session_state.user_inputs["max_peak_load"] * float(st.session_state.user_inputs["voltage"]) * 1.732 * pf) / 1000
                    else:
                        st.session_state.user_inputs["actual_continuous_load"] = st.session_state.user_inputs["max_continuous_load"]
                        st.session_state.user_inputs["actual_peak_load"] = st.session_state.user_inputs["max_peak_load"]

                    st.session_state.show_calculator = True
                    st.session_state.page = "Tool Selection"
                    st.rerun()

            show_config_dialog()

    except Exception as e:
        print(f"Error in modal: {e}")
        st.error(f"Error in modal: {str(e)}. Please check the console output.")


elif st.session_state.page == "Tool Selection":
    st.header("Tool Selection")
    # Integrate tool selection logic - buttons to navigate to other pages
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Technical Specs"):
            st.session_state.page = "Technical Specs"
            st.rerun()
        if st.button("Load Based Specs"):
            st.session_state.page = "Load Based Specs"
            st.rerun()
    with col2:
        if st.button("EBOSS® to Standard Comparison"):
            st.session_state.page = "EBOSS® to Standard Comparison"
            st.rerun()
    with col3:
        if st.button("Cost Analysis"):
            st.session_state.page = "Cost Analysis"
            st.rerun()
        if st.button("Parallel Calculator"):
            st.session_state.page = "Parallel Calculator"
            st.rerun()

elif st.session_state.page == "Technical Specs":
    st.header("Technical Specs")
    # Content from file 2 for technical specs (adapted)
    eboss_model = st.session_state.user_inputs["eboss_model"]
    if eboss_model:
        # Display authentic specs from file 2's data
        authentic_comparison_specs = {  # From file 2
            "EB 25 kVA": {
                "Three-phase Max Power": "25 kVA / 20 kW",
                # ... (add all fields from file 2)
            },
            # ... (for other models)
        }
        specs = authentic_comparison_specs.get(eboss_model, {})
        for key, value in specs.items():
            st.markdown(f"**{key}:** {value}")
    else:
        st.warning("No EBOSS model selected.")

elif st.session_state.page == "Load Based Specs":
    st.header("Load Based Specs")
    # Content from file 2: calculate_load_specs and display
    eboss_model = st.session_state.user_inputs["eboss_model"]
    eboss_type = st.session_state.user_inputs["eboss_type"]
    continuous_load = st.session_state.user_inputs["actual_continuous_load"]
    max_peak_load = st.session_state.user_inputs["actual_peak_load"]
    generator_kva = st.session_state.user_inputs["power_module_gen_size"]
    if eboss_model:
        specs = calculate_load_specs(eboss_model, eboss_type, continuous_load, max_peak_load, generator_kva)
        for key, value in specs.items():
            st.markdown(f"**{key}:** {value}")
    else:
        st.warning("No EBOSS model selected.")

elif st.session_state.page == "EBOSS® to Standard Comparison":
    st.header("EBOSS® to Standard Comparison")
    # Content from file 2: comparison table
    # Use data from file 2, display in table using st.markdown or st.dataframe
    eboss_model = st.session_state.user_inputs["eboss_model"]
    # Assume standard_generator selected or default
    standard_generator = st.selectbox("Select Standard Generator", list(STANDARD_GENERATOR_DATA.keys()))
    if eboss_model and standard_generator:
        # Build comparison_data from file 2
        comparison_data = [
            # ... (from file 2's comparison_data list)
        ]
        df = pd.DataFrame(comparison_data, columns=["Spec", "EBOSS", "Standard"])
        st.table(df)
    else:
        st.warning("No EBOSS model or standard generator selected.")

elif st.session_state.page == "Cost Analysis":
    st.header("Cost Analysis")
    # Content from file 2: cost calculations and table
    # Inputs for costs
    local_fuel_price = st.number_input("Local Fuel Price ($/gal)", value=3.50)
    # ... (other inputs)
    # Calculate eboss_costs and standard_costs
    # Display table using markdown from file 2

elif st.session_state.page == "Parallel Calculator":
    st.header("Parallel Calculator")
    # Placeholder or add if available in file 2

# Footer from file 1
st.markdown(f"""
<div class="footer">
    <span style="display: flex; justify-content: center; align-items: center; width: 100%;">
        EBOSS® Size & Spec Tool | 
        <a href="#" onclick="window.open('https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform?usp=header', '_blank')">Request Demo</a> |
        <a href="#" onclick="window.open('https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform?usp=header', '_blank')">Request Training</a> |
        <a href="#" onclick="window.open('https://youtu.be/0Om2qO-zZfM?si=XnLKJ_SfyKqqUI-g', '_blank')">Learn how the EBOSS® works</a>
    </span>
</div>
""", unsafe_allow_html=True)

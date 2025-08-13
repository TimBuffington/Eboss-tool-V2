import streamlit as st
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
    /* ===== Buttons ===== */
    button, .stButton button {{
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
    button:hover, .stButton button:hover {{
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
        margin: 0px 0;
        height: 0px;
    }}
    .logo {{
        max-width: auto;
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

# EBOSS Load Calculation Reference Data
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

# Standard Generator Data
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

# Functions
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
        model_max_charge_rates = {
            "EB25 kVA": 20,
            "EB70 kVA": 45,
            "EB125 kVA": 65,
            "EB220 kVA": 125,
            "EB400 kVA": 220
        }
        max_rate = model_max_charge_rates.get(eboss_model, float('inf'))
        if custom_rate > max_rate:
            return None
        return round(custom_rate, 1)
    
    if eboss_model not in EBOSS_LOAD_REFERENCE["battery_capacities"]:
        return None
    
    generator_kw = 0
    if eboss_type == "Full Hybrid":
        hybrid_kva = EBOSS_LOAD_REFERENCE["generator_kva_hybrid"].get(eboss_model, 0)
        generator_kw = hybrid_kva * 0.8
        charge_rate = EBOSS_LOAD_REFERENCE["generator_sizes"].get(hybrid_kva, {}).get("fh_charge_rate", 0)
    elif eboss_type == "Power Module" and generator_kva:
        gen_kva = float(generator_kva.replace("kVA", ""))
        generator_kw = gen_kva * 0.8
        charge_rate = EBOSS_LOAD_REFERENCE["generator_sizes"].get(int(gen_kva), {}).get("pm_charge_rate", 0)
    else:
        return None
    
    if charge_rate == 0:
        return None
    
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
    load_percentage = (continuous_load / gen_kw) if gen_kw > 0 else 0
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
    runtime_per_day = 24.0  # Standard generator runs 24 hours/day
    tank_runtime = gen_data["fuel_tank_gal"] / fuel_per_hour if fuel_per_hour > 0 else 0
    return {
        "generator_type": "Standard Diesel Generator",
        "generator_size": standard_generator_size,
        "engine_load_percent": round(load_percentage * 100, 1),
        "continuous_load_percent": round(load_percentage * 100, 1),
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

def calculate_load_specs(eboss_model, eboss_type, continuous_load, max_peak_load, generator_kva=None, custom_charge_rate=None):
    generator_kw_mapping = {
        "EB25 kVA": 14.5,
        "EB70 kVA": 24.5,
        "EB125 kVA": 49,
        "EB220 kVA": 74,
        "EB400 kVA": 125
    }
    model_capacity = generator_kw_mapping.get(eboss_model, 0)
    if not model_capacity:
        return {"error": "Invalid EBOSS model"}
    
    peak_utilization = (max_peak_load / model_capacity * 100) if model_capacity > 0 else 0
    continuous_utilization = (continuous_load / model_capacity * 100) if model_capacity > 0 else 0
    charge_rate = calculate_charge_rate(eboss_model, eboss_type, generator_kva, custom_charge_rate)
    
    if charge_rate is None:
        return {"error": "Invalid charge rate or missing generator size for Power Module"}
    
    # GPH Calculations
    fuel_consumption_gph = 0
    engine_load_percent = 0
    if eboss_type == "Full Hybrid":
        generator_kva = EBOSS_LOAD_REFERENCE["generator_kva_hybrid"].get(eboss_model, 0)
        generator_kw = generator_kva * 0.8
        charge_rate = EBOSS_LOAD_REFERENCE["generator_sizes"].get(generator_kva, {}).get("fh_charge_rate", 0)
        engine_load_percent = (continuous_load / charge_rate * 100) if charge_rate > 0 else 0
        fuel_consumption_gph = interpolate_gph(generator_kva, engine_load_percent)
    elif eboss_type == "Power Module" and generator_kva:
        gen_size = int(generator_kva.replace("kVA", ""))
        generator_kw = gen_size * 0.8
        charge_rate = EBOSS_LOAD_REFERENCE["generator_sizes"].get(gen_size, {}).get("pm_charge_rate", 0)
        engine_load_percent = (charge_rate / generator_kw * 100) if generator_kw > 0 else 0
        fuel_consumption_gph = interpolate_gph(gen_size, engine_load_percent)
    
    # Battery Longevity, Charge Time, and Engine Run per Day
    kwh = EBOSS_LOAD_REFERENCE["battery_capacities"].get(eboss_model, 0)
    battery_longevity = round(kwh / continuous_load, 2) if continuous_load > 0 else "N/A"
    charge_time = round((charge_rate - continuous_load) / kwh, 2) if kwh > 0 and charge_rate > continuous_load else "N/A"
    engine_run_per_day = round(24 / charge_time, 2) if isinstance(charge_time, (int, float)) and charge_time > 0 else "N/A"
    
    return {
        "peak_utilization": round(peak_utilization, 1),
        "continuous_utilization": round(continuous_utilization, 1),
        "charge_rate": charge_rate,
        "engine_load_percent": round(engine_load_percent, 1),
        "fuel_consumption_gph": round(fuel_consumption_gph, 2),
        "battery_longevity": battery_longevity,
        "charge_time": charge_time,
        "engine_run_per_day": engine_run_per_day
    }

def calculate_max_fuel_efficiency_model(continuous_load, max_peak_load, voltage, units):
    if units == "Amps":
        pf = 0.8
        continuous_load = (continuous_load * float(voltage) * 1.732 * pf) / 1000
        max_peak_load = (max_peak_load * float(voltage) * 1.732 * pf) / 1000
    min_gph = float('inf')
    selected_model = "EB25 kVA"
    for model, capacity in EBOSS_LOAD_REFERENCE["battery_capacities"].items():
        gen_kva = EBOSS_LOAD_REFERENCE["generator_kva_hybrid"].get(model, 0)
        if gen_kva:
            charge_rate = EBOSS_LOAD_REFERENCE["generator_sizes"].get(gen_kva, {}).get("fh_charge_rate", 0)
            engine_load_percent = (continuous_load / charge_rate * 100) if charge_rate > 0 else 0
            gph = interpolate_gph(gen_kva, engine_load_percent)
            if gph < min_gph and continuous_load <= capacity:
                min_gph = gph
                selected_model = model
    return selected_model

def validate_inputs(eboss_model, eboss_type, continuous_load, max_peak_load, generator_kva=None, units="kW", voltage="480"):
    generator_kw_mapping = {
        "EB25 kVA": 14.5,
        "EB70 kVA": 24.5,
        "EB125 kVA": 49,
        "EB220 kVA": 74,
        "EB400 kVA": 125
    }
    errors = []
    
    # Convert loads to kW if in Amps
    actual_continuous_load = continuous_load
    actual_peak_load = max_peak_load
    if units == "Amps":
        pf = 0.8
        actual_continuous_load = (continuous_load * float(voltage) * 1.732 * pf) / 1000
        actual_peak_load = (max_peak_load * float(voltage) * 1.732 * pf) / 1000
    
    # Validate EBOSS model
    if eboss_model not in generator_kw_mapping:
        errors.append("Invalid EBOSS model selected.")
    
    # Validate loads
    if actual_continuous_load <= 0 or actual_peak_load <= 0:
        errors.append("Continuous and peak loads must be greater than 0.")
    
    # Validate model capacity
    model_capacity = generator_kw_mapping.get(eboss_model, 0)
    if model_capacity and actual_continuous_load > model_capacity:
        errors.append(f"Continuous load ({actual_continuous_load:.1f} kW) exceeds model capacity ({model_capacity:.1f} kW). Please select a larger EBOSS model.")
    
    # Warn if peak load significantly exceeds capacity
    if model_capacity and actual_peak_load > model_capacity * 1.2:
        errors.append(f"Peak load ({actual_peak_load:.1f} kW) significantly exceeds model capacity ({model_capacity:.1f} kW). Risk of overload.")
    
    # Validate charge rate
    charge_rate = calculate_charge_rate(eboss_model, eboss_type, generator_kva)
    if charge_rate is None:
        if eboss_type == "Power Module" and not generator_kva:
            errors.append("Please select a valid generator size for Power Module.")
        else:
            errors.append("Unable to calculate charge rate. Check model and type.")
    elif charge_rate <= actual_continuous_load:
        errors.append(f"Charge rate ({charge_rate:.1f} kW) is insufficient for continuous load ({actual_continuous_load:.1f} kW). Select a larger model or generator.")
    
    return errors

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
    st.session_state.selected_option = None
if "recommended_model" not in st.session_state:
    st.session_state.recommended_model = ""
if "page" not in st.session_state:
    st.session_state.page = "Home"
if 'show_cost_analysis' not in st.session_state:
    st.session_state.show_cost_analysis = False
if 'show_cost_dialog' not in st.session_state:
    st.session_state.show_cost_dialog = False
if 'cost_standard_generator' not in st.session_state:
    st.session_state.cost_standard_generator = None
if 'pm_charge_enabled' not in st.session_state:
    st.session_state.pm_charge_enabled = False

# Homepage
st.markdown("<div class='logo-container'>", unsafe_allow_html=True)
try:
    st.image("https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/logo.png", use_container_width=False, width=600, output_format="PNG")
except Exception as e:
    st.error(f"Logo failed to load: {e}. Please verify the file at https://github.com/TimBuffington/Eboss-tool-V2/tree/main/assets/logo.png.")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>EBOSS® Size & Spec Tool</h1>", unsafe_allow_html=True)

# --- Centered & aligned 2-row button layout ---
# --- Centered & aligned 3×2 button grid (works on all Streamlit versions) ---
with st.container():
    st.markdown("<div style='display:flex;flex-direction:column;align-items:center;width:100%'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    # Row 1 — external links (open in new tab)
    with col1:
        if st.button("Request Demo", key="btn_link_request_demo"):
            st.markdown('<script>window.open("https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform?usp=header","_blank");</script>', unsafe_allow_html=True)
    with col2:
        if st.button("Request Training", key="btn_link_request_training"):
            st.markdown('<script>window.open("https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform?usp=header","_blank");</script>', unsafe_allow_html=True)
    with col3:
        if st.button("Learn how the EBOSS® works", key="btn_link_learn_eboss"):
            st.markdown('<script>window.open("https://youtu.be/0Om2qO-zZfM?si=XnLKJ_SfyKqqUI-g","_blank");</script>', unsafe_allow_html=True)

    # small spacer
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # Row 2 — in‑app actions (unique keys)
    with col1:
        manual_select_clicked = st.button("Manually Select EBOSS Type and Model", key="btn_manual_select")
    with col2:
        load_based_clicked = st.button("Use Load Based Suggested EBOSS", key="btn_load_based")
    with col3:
        fuel_efficiency_clicked = st.button("Use EBOSS Model Based on Max Fuel Efficiency", key="btn_fuel_eff")

    st.markdown("</div>", unsafe_allow_html=True)


# Dialog logic
if manual_select_clicked:
    try:
        @st.dialog("EBOSS® Configuration")
        def show_manual_config_dialog():
            st.markdown("Enter your EBOSS® configuration:")
            col1, col2, col3 = st.columns(3)
            with col1:
                eboss_model = st.selectbox("EBOSS® Model", options=["EB25 kVA", "EB70 kVA", "EB125 kVA", "EB220 kVA", "EB400 kVA"], key="eboss_model_input")
                eboss_type = st.selectbox("EBOSS® Type", options=["Full Hybrid", "Power Module"], key="eboss_type_input")
                generator_kva = None
                if eboss_type == "Power Module":
                    generator_kva = st.selectbox("Power Module Generator Size", options=["25 kVA", "70 kVA", "125 kVA", "220 kVA", "400 kVA"], key="power_module_gen_size_input")
            with col2:
                max_continuous_load = st.number_input("Max Continuous Load", min_value=0.0, step=0.1, key="max_continuous_load_input")
                max_peak_load = st.number_input("Max Peak Load", min_value=0.0, step=0.1, key="max_peak_load_input")
            with col3:
                units = st.selectbox("Units", options=["kW", "Amps"], key="units_input")
                voltage = st.selectbox("Voltage", options=["120", "240", "208", "480"], key="voltage_input")

            # Validate inputs
            errors = validate_inputs(eboss_model, eboss_type, max_continuous_load, max_peak_load, generator_kva, units, voltage)
            if errors:
                for error in errors:
                    st.error(error)
                launch_enabled = False
            else:
                launch_enabled = True

            if st.button("Launch Tool", key="launch_tool_manual", disabled=not launch_enabled):
                st.session_state.user_inputs["eboss_model"] = eboss_model
                st.session_state.user_inputs["eboss_type"] = eboss_type
                st.session_state.user_inputs["power_module_gen_size"] = generator_kva
                st.session_state.user_inputs["max_continuous_load"] = max_continuous_load
                st.session_state.user_inputs["max_peak_load"] = max_peak_load
                st.session_state.user_inputs["units"] = units
                st.session_state.user_inputs["voltage"] = voltage

                if units == "Amps":
                    pf = 0.8
                    st.session_state.user_inputs["actual_continuous_load"] = (max_continuous_load * float(voltage) * 1.732 * pf) / 1000
                    st.session_state.user_inputs["actual_peak_load"] = (max_peak_load * float(voltage) * 1.732 * pf) / 1000
                else:
                    st.session_state.user_inputs["actual_continuous_load"] = max_continuous_load
                    st.session_state.user_inputs["actual_peak_load"] = max_peak_load

                st.session_state.show_calculator = True
                st.session_state.page = "Tool Selection"
                st.rerun()

        show_manual_config_dialog()

    except Exception as e:
        print(f"Error in modal: {e}")
        st.error(f"Error in modal: {str(e)}. Please check the console output.")

if load_based_clicked:
    try:
        @st.dialog("Load Based Suggested EBOSS® Configuration")
        def show_load_based_dialog():
            st.session_state.recommended_model = "EB70 kVA"
            st.markdown(f"**Recommended EBOSS® Model:** {st.session_state.recommended_model}")
            col1, col2, col3 = st.columns(3)
            with col1:
                eboss_type = st.selectbox("EBOSS® Type", options=["Full Hybrid"], key="eboss_type_input", disabled=True)
            with col2:
                max_continuous_load = st.number_input("Max Continuous Load", min_value=0.0, step=0.1, key="max_continuous_load_input")
                max_peak_load = st.number_input("Max Peak Load", min_value=0.0, step=0.1, key="max_peak_load_input")
            with col3:
                units = st.selectbox("Units", options=["kW", "Amps"], key="units_input")
                voltage = st.selectbox("Voltage", options=["120", "240", "208", "480"], key="voltage_input")

            # Validate inputs
            errors = validate_inputs(st.session_state.recommended_model, eboss_type, max_continuous_load, max_peak_load, None, units, voltage)
            if errors:
                for error in errors:
                    st.error(error)
                launch_enabled = False
            else:
                launch_enabled = True

            if st.button("Launch Tool", key="load_based_button", disabled=not launch_enabled):
                if units == "Amps":
                    pf = 0.8
                    st.session_state.user_inputs["actual_continuous_load"] = (max_continuous_load * float(voltage) * 1.732 * pf) / 1000
                    st.session_state.user_inputs["actual_peak_load"] = (max_peak_load * float(voltage) * 1.732 * pf) / 1000
                else:
                    st.session_state.user_inputs["actual_continuous_load"] = max_continuous_load
                    st.session_state.user_inputs["actual_peak_load"] = max_peak_load

                st.session_state.user_inputs["eboss_model"] = st.session_state.recommended_model
                st.session_state.user_inputs["eboss_type"] = "Full Hybrid"
                st.session_state.user_inputs["power_module_gen_size"] = ""
                st.session_state.user_inputs["max_continuous_load"] = max_continuous_load
                st.session_state.user_inputs["max_peak_load"] = max_peak_load
                st.session_state.user_inputs["units"] = units
                st.session_state.user_inputs["voltage"] = voltage
                st.session_state.show_calculator = True
                st.session_state.page = "Tool Selection"
                st.rerun()

        show_load_based_dialog()

    except Exception as e:
        print(f"Error in modal: {e}")
        st.error(f"Error in modal: {str(e)}. Please check the console output.")

if fuel_efficiency_clicked:
    try:
        @st.dialog("Max Fuel Efficiency EBOSS® Configuration")
        def show_fuel_efficiency_dialog():
            max_continuous_load = st.session_state.get("max_continuous_load_input", 0.0)
            max_peak_load = st.session_state.get("max_peak_load_input", 0.0)
            units = st.session_state.get("units_input", "kW")
            voltage = st.session_state.get("voltage_input", "480")
            recommended_model = calculate_max_fuel_efficiency_model(max_continuous_load, max_peak_load, voltage, units)
            st.session_state.recommended_model = recommended_model
            st.markdown(f"**Recommended EBOSS® Model for Max Fuel Efficiency:** {recommended_model}")
            col1, col2, col3 = st.columns(3)
            with col1:
                eboss_type = st.selectbox("EBOSS® Type", options=["Full Hybrid"], key="eboss_type_input", disabled=True)
            with col2:
                max_continuous_load = st.number_input("Max Continuous Load", min_value=0.0, step=0.1, key="max_continuous_load_input")
                max_peak_load = st.number_input("Max Peak Load", min_value=0.0, step=0.1, key="max_peak_load_input")
            with col3:
                units = st.selectbox("Units", options=["kW", "Amps"], key="units_input")
                voltage = st.selectbox("Voltage", options=["120", "240", "208", "480"], key="voltage_input")

            # Validate inputs
            errors = validate_inputs(recommended_model, eboss_type, max_continuous_load, max_peak_load, None, units, voltage)
            if errors:
                for error in errors:
                    st.error(error)
                launch_enabled = False
            else:
                launch_enabled = True

            if st.button("Launch Tool", key="fuel_efficiency_button", disabled=not launch_enabled):
                if units == "Amps":
                    pf = 0.8
                    st.session_state.user_inputs["actual_continuous_load"] = (max_continuous_load * float(voltage) * 1.732 * pf) / 1000
                    st.session_state.user_inputs["actual_peak_load"] = (max_peak_load * float(voltage) * 1.732 * pf) / 1000
                else:
                    st.session_state.user_inputs["actual_continuous_load"] = max_continuous_load
                    st.session_state.user_inputs["actual_peak_load"] = max_peak_load

                st.session_state.user_inputs["eboss_model"] = recommended_model
                st.session_state.user_inputs["eboss_type"] = "Full Hybrid"
                st.session_state.user_inputs["power_module_gen_size"] = ""
                st.session_state.user_inputs["max_continuous_load"] = max_continuous_load
                st.session_state.user_inputs["max_peak_load"] = max_peak_load
                st.session_state.user_inputs["units"] = units
                st.session_state.user_inputs["voltage"] = voltage
                st.session_state.show_calculator = True
                st.session_state.page = "Tool Selection"
                st.rerun()

        show_fuel_efficiency_dialog()

    except Exception as e:
        print(f"Error in modal: {e}")
        st.error(f"Error in modal: {str(e)}. Please check the console output.")

# Navigation to other pages
elif st.session_state.page == "Tool Selection":
    st.header("Tool Selection")
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
    eboss_model = st.session_state.user_inputs["eboss_model"]
    if eboss_model:
        st.markdown(f"**Selected EBOSS Model:** {eboss_model}")
        # Placeholder for detailed specs
    else:
        st.warning("No EBOSS model selected.")

elif st.session_state.page == "Load Based Specs":
    st.header("Load Based Specs")
    eboss_model = st.session_state.user_inputs["eboss_model"]
    eboss_type = st.session_state.user_inputs["eboss_type"]
    continuous_load = st.session_state.user_inputs["actual_continuous_load"]
    max_peak_load = st.session_state.user_inputs["actual_peak_load"]
    generator_kva = st.session_state.user_inputs["power_module_gen_size"]
    if eboss_model:
        specs = calculate_load_specs(eboss_model, eboss_type, continuous_load, max_peak_load, generator_kva)
        if "error" in specs:
            st.error(specs["error"])
        else:
            for key, value in specs.items():
                st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
    else:
        st.warning("No EBOSS model selected.")

elif st.session_state.page == "EBOSS® to Standard Comparison":
    st.header("EBOSS® to Standard Comparison")
    eboss_model = st.session_state.user_inputs["eboss_model"]
    eboss_type = st.session_state.user_inputs["eboss_type"]
    continuous_load = st.session_state.user_inputs["actual_continuous_load"]
    max_peak_load = st.session_state.user_inputs["actual_peak_load"]
    generator_kva = st.session_state.user_inputs["power_module_gen_size"]
    standard_generator = st.selectbox("Select Standard Generator", list(STANDARD_GENERATOR_DATA.keys()))
    if eboss_model and standard_generator:
        eboss_specs = calculate_load_specs(eboss_model, eboss_type, continuous_load, max_peak_load, generator_kva)
        standard_specs = calculate_standard_generator_specs(standard_generator, continuous_load, max_peak_load)
        if "error" in eboss_specs:
            st.error(eboss_specs["error"])
        else:
            df = pd.DataFrame([
                ("Generator Size", eboss_model, standard_generator),
                ("Continuous Load %", f"{eboss_specs.get('continuous_utilization', 0):.1f}%", f"{standard_specs.get('continuous_load_percent', 0):.1f}%"),
                ("Engine Load %", f"{eboss_specs.get('engine_load_percent', 0):.1f}%", f"{standard_specs.get('engine_load_percent', 0):.1f}%"),
                ("Fuel Consumption (GPH)", f"{eboss_specs.get('fuel_consumption_gph', 0):.2f}", f"{standard_specs.get('fuel_consumption_gph', 0):.2f}"),
                ("Runtime per Day (hours)", f"{eboss_specs.get('engine_run_per_day', 'N/A')}", f"{standard_specs.get('runtime_per_day', 0):.1f}")
            ], columns=["Spec", "EBOSS", "Standard"])
            st.table(df)
    else:
        st.warning("No EBOSS model or standard generator selected.")

elif st.session_state.page == "Cost Analysis":
    st.header("Cost Analysis")
    local_fuel_price = st.number_input("Local Fuel Price ($/gal)", value=3.50, min_value=0.0, step=0.1)
    st.session_state.user_inputs["local_fuel_price"] = local_fuel_price
    st.warning("Cost analysis functionality is under development.")

elif st.session_state.page == "Parallel Calculator":
    st.header("Parallel Calculator")
    st.warning("Parallel calculator functionality is under development.")

# Footer
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

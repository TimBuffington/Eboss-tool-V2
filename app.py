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
    "Light Grey": "#D3D3D3",
    }

LOGO_URL = "https://raw.githubusercontent.com/TimBuffington/troubleshooting/refs/heads/main/assets/ANA-ENERGY-LOGO-HORIZONTAL-WHITE-GREEN.png"

# Centered, responsive logo
st.markdown("""
<style>
.logo-wrap{
  display:flex;
  justify-content:center;
  align-items:center;
  margin: 8px 0 16px;
}
.logo-wrap img{
  width: clamp(220px, 55vw, 560px);  /* responsive: min 220px, max 560px */
  height: auto;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    f"<div class='logo-wrap'><img src='{LOGO_URL}' alt='ANA Energy Logo' /></div>",
    unsafe_allow_html=True
)

# --- Add once near the top (after your COLORS dict / styles) ---
st.markdown(f"""
<style>
/* === Anchor links styled as CTA buttons === */
.cta-link {{
  display: inline-block;
  width: 100%;
  text-align: center;
  text-decoration: none !important;
  background-color: {COLORS['Asphalt']};
  color: {COLORS['Alpine White']};
  border: 2px solid {COLORS['Concrete']};
  font-family: Arial, sans-serif;
  font-size: 16px;
  font-weight: 700;
  text-shadow: 0 0 6px {COLORS['Energy Green']};
  border-radius: 10px;
  padding: 12px 14px;
  transition: box-shadow .25s ease, transform .15s ease;
  box-sizing: border-box;
}}
.cta-link:hover {{
  box-shadow: 0 0 28px {COLORS['Energy Green']};
  transform: translateY(-1px);
}}

/* === Streamlit buttons inside .cta-scope should look like .cta-link and fill columns === */
.cta-scope [data-testid="column"] .stButton {{
  width: 100% !important;
}}
.cta-scope .stButton > button {{
  display: block;
  width: 100% !important;
  text-align: center;
  background-color: {COLORS['Asphalt']};
  color: {COLORS['Alpine White']};
  border: 2px solid {COLORS['Concrete']};
  font-family: Arial, sans-serif;
  font-size: 16px;
  font-weight: 700;
  text-shadow: 0 0 6px {COLORS['Energy Green']};
  border-radius: 10px;
  padding: 12px 14px;
  box-sizing: border-box;
  transition: box-shadow .25s ease, transform .15s ease;
}}
.cta-scope .stButton > button:hover {{
  box-shadow: 0 0 28px {COLORS['Energy Green']};
  transform: translateY(-1px);
}}
</style>
""", unsafe_allow_html=True)

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
        border: 2px solid {COLORS['Light Grey']} !important;
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
        width: 100%;
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

st.set_page_config(layout="wide")  # important!

def _to_normalized_kw(value: float, units: str, voltage: str, pf: float = 0.8) -> float:
    """
    Convert a single input (continuous or peak) to normalized kW (baseline 3φ 480V).
    - If units == 'kW': return as-is (kW is voltage-agnostic).
    - If units == 'Amps':
        * 3φ (208, 480): kW = √3 * V * I * PF / 1000
        * 1φ (120, 240): kW = V * I * PF / 1000
    """
    if units == "kW":
        return float(value or 0.0)
    v = float(voltage); i = float(value or 0.0)
    if str(voltage) in {"208", "480"}:
        return (1.732 * v * i * pf) / 1000.0
    return (v * i * pf) / 1000.0



def render_adjusted_load_panel(cont_kw: float, peak_kw: float):
    """
    Compact “Adjusted Load” panel for the modal.
    Shows normalized kW prominently; raw info is available in session if needed.
    """
    st.markdown(
        f"""
        <div style="
            border:1px solid #939598; border-radius:10px; padding:12px 14px;
            background: rgba(0,0,0,.55); box-shadow: 0 0 12px rgba(129,189,71,.35);
            ">
          <div style="font-weight:800; letter-spacing:.4px; margin-bottom:6px;">
            Adjusted Load (kW @ 3φ 480V)
          </div>
          <div>Continuous: <b>{cont_kw:.2f} kW</b></div>
          <div>Peak: <b>{peak_kw:.2f} kW</b></div>
        </div>
        """,
        unsafe_allow_html=True
    )

import math
import streamlit as st

def _set_if_missing(S: dict, key: str, value):
    """Set only if missing/None; return final value."""
    if key not in S or S.get(key) is None:
        S[key] = value
    return S[key]

def store_derived_metrics(
    *,
    eboss_model: str,
    eboss_type: str,
    cont_kw: float,
    peak_kw: float,
    charge_rate_kw: float,
    generator_kva=None,
    usable_soc_frac: float = 0.80,
    charge_efficiency: float = 0.90,
):
    """
    Persist a rich set of derived values so other pages can just read keys.
    Uses ONLY interpolation for fuel (no BSFC). Does not overwrite existing keys.
    """
    st.session_state.setdefault("user_inputs", {})
    S = st.session_state.user_inputs

    spec = EBOSS_UNITS.get(eboss_model, {})
    battery_kwh = float(spec.get("battery_kwh", 0) or 0)

    # ----- Determine generator sizing (kVA/kW) -----
    if eboss_type == "Full Hybrid":
        gen_kva_for_interp = spec.get("fh_gen_size_kva")
        if not gen_kva_for_interp:
            st.warning("FH generator size (kVA) missing from specs; cannot interpolate fuel.")
            st.stop()
        gen_kva_for_interp = int(gen_kva_for_interp)
        gen_kw = _gen_kw_from_kva(gen_kva_for_interp)
    else:
        gkva = _parse_kva(generator_kva)
        if not gkva:
            st.warning("Power Module generator size required to interpolate fuel.")
            st.stop()
        gen_kva_for_interp = int(gkva)
        gen_kw = _gen_kw_from_kva(gkva)

    # ----- Engine load & fuel (INTERPOLATION ONLY) -----
    load_frac = (charge_rate_kw / gen_kw) if gen_kw > 0 else 0.0
    load_frac = max(0.0, min(1.0, load_frac))
    fuel_gph = interpolate_gph(gen_kva_for_interp, load_frac)
    if fuel_gph == 0.0:
        st.warning("No interpolation row for this generator size; use one of: 25, 45, 65, 125, 220, 400 kVA.")
        st.stop()

    # ----- Battery/charge math -----
    usable_kwh   = battery_kwh * usable_soc_frac
    runtime_h    = (usable_kwh / cont_kw) if cont_kw > 0 else math.inf
    net_charge_kw = max(charge_rate_kw - cont_kw, 0.01)               # keep >0 to avoid /0
    charge_time_h = (usable_kwh / charge_efficiency) / charge_rate_kw if charge_rate_kw > 0 else math.inf

    # ----- Daily estimates -----
    daily_energy_kwh   = cont_kw * 24.0
    cycles_per_day     = (daily_energy_kwh / usable_kwh) if usable_kwh > 0 else math.inf
    engine_run_h_day   = (cycles_per_day * charge_time_h) if math.isfinite(cycles_per_day) else math.inf
    daily_fuel_gal     = (engine_run_h_day * fuel_gph) if math.isfinite(engine_run_h_day) else math.inf

    # ----- Persist (only if missing) -----
    _set_if_missing(S, "eboss_model", eboss_model)
    _set_if_missing(S, "eboss_type", eboss_type)
    _set_if_missing(S, "power_module_gen_size", (str(generator_kva) if generator_kva else S.get("power_module_gen_size","")))
    _set_if_missing(S, "battery_kwh", battery_kwh)
    _set_if_missing(S, "gen_kw", round(gen_kw, 2))
    _set_if_missing(S, "cont_capacity_kw", float(spec.get("cont_capacity_kw", 0) or 0))
    _set_if_missing(S, "peak_capacity_kw", float(spec.get("peak_capacity_kw", 0) or 0))
    _set_if_missing(S, "pm_charge_rate_kw_spec", float(spec.get("pm_charge_rate_kw", 0) or 0))
    _set_if_missing(S, "fh_charge_rate_kw_spec", float(spec.get("fh_charge_rate_kw", 0) or 0))
    _set_if_missing(S, "max_charge_rate_kw_spec", float(spec.get("max_charge_rate_kw", 0) or 0))

    _set_if_missing(S, "actual_continuous_load", cont_kw)
    _set_if_missing(S, "actual_peak_load", peak_kw)

    _set_if_missing(S, "charge_rate_kw", charge_rate_kw)
    _set_if_missing(S, "engine_load_pct", round(load_frac * 100.0, 2))
    _set_if_missing(S, "fuel_gph_at_charge", round(fuel_gph, 3))          # ← canonical, interpolation-only

    _set_if_missing(S, "usable_battery_kwh", round(usable_kwh, 2))
    _set_if_missing(S, "battery_runtime_hours_at_cont", round(runtime_h, 2) if math.isfinite(runtime_h) else runtime_h)
    _set_if_missing(S, "charge_time_hours_full", round(charge_time_h, 2) if math.isfinite(charge_time_h) else charge_time_h)

    _set_if_missing(S, "daily_energy_kwh", round(daily_energy_kwh, 1))
    _set_if_missing(S, "daily_cycles", round(cycles_per_day, 3) if math.isfinite(cycles_per_day) else cycles_per_day)
    _set_if_missing(S, "engine_run_hours_per_day", round(engine_run_h_day, 2) if math.isfinite(engine_run_h_day) else engine_run_h_day)
    _set_if_missing(S, "daily_fuel_gal", round(daily_fuel_gal, 2) if math.isfinite(daily_fuel_gal) else daily_fuel_gal)

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

import streamlit as st

# --- helpers ---
def _parse_kva(value) -> float | None:
    """Accepts 65, '65', or '65 kVA' → 65.0 (or None)."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).lower().replace("kva", "").strip()
    try:
        return float(s)
    except ValueError:
        return None

def _gen_kw_from_kva(kva: float) -> float:
    """Rule of thumb: kW ≈ 0.8 × kVA."""
    return 0.8 * float(kva)


# --- single entry point ---
def render_Charge_Rate(
    eboss_model: str,
    eboss_type: str,
    *,
    generator_kva=None,              # PM only: per-unit generator size (kVA or '65 kVA')
    custom_rate: float | None = None,# manual override (kW)
    store_to_session: bool = True,   # write to st.session_state.user_inputs
    session_key: str = "charge_rate_kw"
) -> float | None:
    """
    ONE call to determine and (optionally) store the charge rate (kW, rounded 0.1).

    Rules:
    - Use the model’s FH/PM charge rate from EBOSS_UNITS by default.
    - If custom_rate is provided, use that instead.
    - Full Hybrid: return the rate as-is (no generator gate here).
    - Power Module:
        • If a generator size is given and gen_kW < desired rate, show a warning and let the user:
          - Proceed → auto-adjust to 98% of generator kW
          - Select a larger generator → stop so they can change the input
        • If no generator size is given (or it’s valid & large enough), just return the rate.

    Returns:
        float (kW, rounded to 0.1) or None on invalid inputs.
    """
#   CHARGE RATE LOGIC ======================================================================
    spec = EBOSS_UNITS.get(eboss_model)
    if not spec:
        return None

    # 1) pick desired rate (custom overrides model default)
    if custom_rate is not None:
        try:
            desired = float(custom_rate)
        except (TypeError, ValueError):
            return None
    else:
        if eboss_type == "Full Hybrid":
            desired = float(spec.get("fh_charge_rate_kw", 0.0))
        elif eboss_type == "Power Module":
            desired = float(spec.get("pm_charge_rate_kw", 0.0))
        else:
            return None

    # 2) Full Hybrid logic (simple)
    if eboss_type == "Full Hybrid":
        rate = round(desired, 1)
        if store_to_session:
            st.session_state.setdefault("user_inputs", {})
            st.session_state.user_inputs[session_key] = rate
            st.session_state.user_inputs["charge_rate_source"] = "custom" if custom_rate is not None else "fh_default"
        return rate

    # 3) Power Module logic
    gen_kva = _parse_kva(generator_kva)
    # If no generator specified, assume source is adequate; use desired
    if gen_kva is None or gen_kva <= 0:
        rate = round(desired, 1)
        if store_to_session:
            st.session_state.setdefault("user_inputs", {})
            st.session_state.user_inputs[session_key] = rate
            st.session_state.user_inputs["charge_rate_source"] = "custom" if custom_rate is not None else "pm_default"
        return rate

    gen_kw = _gen_kw_from_kva(gen_kva)

    # OK as-is
    if gen_kw >= desired:
        rate = round(desired, 1)
        if store_to_session:
            st.session_state.setdefault("user_inputs", {})
            st.session_state.user_inputs[session_key] = rate
            st.session_state.user_inputs["charge_rate_source"] = "custom" if custom_rate is not None else "pm_default"
        return rate

    # Underpowered → warn + ask to proceed or pick larger gen
    st.warning(
        f"Selected generator is **{gen_kw:.1f} kW**, which is **below** the desired charge rate "
        f"(**{desired:.1f} kW**) for **{eboss_model}**."
    )
    c1, c2 = st.columns(2)
    proceed = c1.button(
        "Proceed: adjust charge rate to 98% of generator kW",
        key=f"pm_adjust_{eboss_model}_{gen_kva}_{desired}"
    )
    choose_larger = c2.button(
        "Select a larger generator",
        key=f"pm_larger_{eboss_model}_{gen_kva}_{desired}"
    )

    if proceed:
        adjusted = round(0.98 * gen_kw, 1)
        st.success(f"Charge rate adjusted to **{adjusted:.1f} kW** (98% of generator kW).")
        if store_to_session:
            st.session_state.setdefault("user_inputs", {})
            st.session_state.user_inputs[session_key] = adjusted
            st.session_state.user_inputs["charge_rate_source"] = "pm_adjusted_to_98pct_gen"
        return adjusted

    if choose_larger:
        st.info("Please select a larger generator size.")
        st.stop()  # halt so the user can change the generator input

    # wait for a choice
    st.stop()
    return None


# Homepage============================================================================================================
st.markdown("<h1 style='text-align: center;'>EBOSS® Size & Spec Tool</h1>", unsafe_allow_html=True)


with st.container():
    st.markdown(
        "<div style='display:flex;flex-direction:column;align-items:center;width:100%'>",
        unsafe_allow_html=True
    )
# --- Row 1 — external links (no JS; real links styled as buttons)
col1, col2, col3 = st.columns([1,1,1]) 

with col1:
    st.markdown(
        '<a class="cta-link" href="https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform?usp=header" target="_blank" rel="noopener">Request Demo</a>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<a class="cta-link" href="https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform?usp=header" target="_blank" rel="noopener">Request Training</a>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        '<a class="cta-link" href="https://youtu.be/0Om2qO-zZfM?si=XnLKJ_SfyKqqUI-g" target="_blank" rel="noopener">Learn how the EBOSS® works</a>',
        unsafe_allow_html=True
    )

# ----- centered text BETWEEN the two rows -----
st.markdown(
    "<div class='message-text' style='margin:12px 0; text-align:center;'>Please Select an EBOSS Configuration</div>",
    unsafe_allow_html=True
)
with st.container():
    st.markdown(
        "<div style='display:flex;flex-direction:column;align-items:center;width:100%'>",
        unsafe_allow_html=True
    )

st.markdown("<div class='cta-scope'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,1,1])

with col1:
    with st.container():
        manual_select_clicked = st.button(
            "Manually Select EBOSS Type and Model",
            key="btn_manual_select"
            width: 100% !important;
        )

with col2:
    with st.container():
        load_based_clicked = st.button(
            "Use Load Based Suggested EBOSS",
            key="btn_load_based"
            width: 100% !important;
        )

with col3:
    with st.container():
        fuel_efficiency_clicked = st.button(
            "Use EBOSS Model Based on Max Fuel Efficiency",
            key="btn_fuel_eff"
            width: 100% !important;
        )

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
                max_continuous_load = st.number_input("Max Continuous Load", min_value=0.0, step=1.0, format="%g", key="max_continuous_load_input")
                max_peak_load = st.number_input("Max Peak Load", min_value=0.0, step=1.0, format="%g", key="max_peak_load_input")
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
# ===========================
# Compare Page
# ===========================
import streamlit as st

S = st.session_state.setdefault("user_inputs", {})

# Default view
st.session_state.setdefault("view_mode", "spec")

# Current model (from earlier modals)
current_model_key = S.get("eboss_model")  # e.g., "EB125 kVA"
if not current_model_key:
    st.info("Please configure a model first (Manual or Load-Based).")
    st.stop()

# Map EBOSS_UNITS keys -> labels used in the provided spec table
MODEL_LABEL = {
    "EB25 kVA":  "EB 25 kVA",
    "EB70 kVA":  "EB 70 kVA",
    "EB125 kVA": "EB 125 kVA",
    "EB220 kVA": "EB 220 kVA",
    "EB400 kVA": "EB 400 kVA",
}
model_label = MODEL_LABEL.get(current_model_key, current_model_key)

# ───────────── Buttons ─────────────
col_spec, col_cost = st.columns([1, 1])
with col_spec:
    if st.button("📊 Spec Comparison"):
        st.session_state.view_mode = "spec"
with col_cost:
    if st.button("💵 Cost Comparison"):
        st.session_state.view_mode = "cost"

# ───────────── Spec Comparison Table ─────────────
if st.session_state.get("view_mode") == "spec":
    st.markdown(
        "<div class='eboss-card'><strong>EBOSS® vs Standard Generator</strong></div>",
        unsafe_allow_html=True
    )

    # NOTE: keeping your provided values; keys align to model_label above
    spec_table = {
        "EB 25 kVA": [
            ("Three-phase",            "30 kVA / 24 kW",          "27.5 kVA / 22 kW"),
            ("Single-phase",           "20 kVA / 16 kW",          "19.75 kVA / 15.8 kW"),
            ("Frequency",              "60 Hz",                    "60 Hz"),
            ("Simultaneous voltage",   "Yes 120v / 240v / 208v / 480v", "No"),
            ("Voltage regulation",     "Adjustable",               "Adjustable"),
            ("Max Intermittent 208v",  "70 A / 20 kW",             "60 A / 17.29 kW"),
            ("Motor start 208v",       "104 A / 30 kW",            "60 A / 17.3 kW"),
            ("Generator Size",         "25 kVA / 20 kW",           "25 kVA / 20 kW"),
            ("Max Continuous @208v",   "70 A / 20.2 kW",           "60 A"),
        ],
        "EB 70 kVA": [
            ("Three-phase",            "70 kVA / 56 kW",           "77 kVA / 62 kW"),
            ("Single-phase",           "47 kVA / 37 kW",           "N/A"),
            ("Frequency",              "60 Hz",                    "60 Hz"),
            ("Simultaneous voltage",   "Yes 120v / 240v / 208v / 480v", "No"),
            ("Voltage regulation",     "Adjustable",               "Adjustable"),
            ("Max Intermittent 208v",  "194 A / 56 kW",            "168 A / 48 kW"),
            ("Motor start 208v",       "291 A / 84 kW",            "200 A / 57 kW"),
            ("Generator Size",         "45 kVA / 36 kW",           "70 kVA / 56 kW"),
            ("Max Continuous @208v",   "119 A / 34.5 kW",          "168 A"),
        ],
        "EB 125 kVA": [
            ("Three-phase",            "125 kVA / 100 kW",         "137.5 kVA / 110 kW"),
            ("Single-phase",           "N/A",                      "89.8 kVA / 79 kW"),
            ("Frequency",              "60 Hz",                    "60 Hz"),
            ("Simultaneous voltage",   "Yes 208v / 480v",          "No"),
            ("Voltage regulation",     "Adjustable",               "Adjustable"),
            ("Max Intermittent 208v",  "345 A / 99.5 kW",          "300 A / 86 kW"),
            ("Motor start 208v",       "532 A / 153 kW",           "300 A / 86 kW"),
            ("Generator Size",         "70 kVA / 56 kW",           "125 kVA / 100 kW"),
            ("Max Continuous @208v",   "167 A / 48 kW",            "300 A"),
        ],
        "EB 220 kVA": [
            ("Three-phase",            "220 kVA / 176 kW",         "242 kVA / 194 kW"),
            ("Single-phase",           "N/A",                      "N/A"),
            ("Frequency",              "60 Hz",                    "60 Hz"),
            ("Simultaneous voltage",   "Yes 208v / 480v",          "No"),
            ("Voltage regulation",     "Adjustable",               "Adjustable"),
            ("Max Intermittent 208v",  "700 A / 201 kW",           "529 A / 152.5 kW"),
            ("Motor start 208v",       "1065 A / 307 kW",          "600 A / 172.9 kW"),
            ("Generator Size",         "125 kVA / 100 kW",         "220 kVA / 176 kW"),
            ("Max Continuous @208v",   "328 A / 94 kW",            "529 A"),
        ],
        "EB 400 kVA": [
            ("Three-phase",            "400 kVA / 320 kW",         "420 kVA / 336 kW"),
            ("Single-phase",           "N/A",                      "N/A"),
            ("Frequency",              "60 Hz",                    "60 Hz"),
            ("Simultaneous voltage",   "Yes 208v / 480v",          "No"),
            ("Voltage regulation",     "Adjustable",               "Adjustable"),
            ("Max Intermittent 208v",  "481 A / 138.5 kW",         "–"),
            ("Motor start 208v",       "1776 A / 511 kW",          "–"),
            ("Generator Size",         "220 kVA / 176 kW",         "220 kVA / 176 kW"),
            ("Max Continuous @208v",   "481 A",                    "481 A"),
        ],
    }

    model_specs = spec_table.get(model_label, [])
    if not model_specs:
        st.warning(f"No comparison rows found for {model_label}.")
    else:
        col1, col2, col3, col4 = st.columns([2, 3, 3, 1])
        for label, eboss_val, std_val in model_specs:
            with col1:
                st.markdown(f"**{label}**")
            with col2:
                st.markdown(eboss_val)
            with col3:
                st.markdown(std_val)
            with col4:
                st.markdown("✅" if eboss_val != std_val else "–")

# ───────────── Cost Comparison Table ─────────────
elif st.session_state.get("view_mode") == "cost":
    with st.form("cost_input_form", clear_on_submit=False):
        st.markdown(
            "<div class='eboss-card'><strong>Enter Cost Inputs</strong></div>",
            unsafe_allow_html=True
        )
        rental    = st.number_input("Monthly Rental Rate ($)",     min_value=0.0, step=10.0,  key="rental_rate")
        fuel_cost = st.number_input("Fuel Cost per Gallon ($)",    min_value=0.0, step=0.01, key="fuel_cost_per_gal")
        delivery  = st.number_input("Delivery Fee ($)",            min_value=0.0, step=10.0,  key="delivery_fee")
        pm_cost   = st.number_input("PM Service Cost ($/mo)",      min_value=0.0, step=10.0,  key="pm_service_cost")
        days_in_month = st.number_input("Days in Month",           min_value=1,   max_value=31, value=30, step=1)
        submit = st.form_submit_button("Calculate")

    if submit:
        # Pull daily runtime (hours) and interpolated fuel (gph) from session
        daily_runtime_hr = float(S.get("engine_run_hours_per_day") or 0.0)
        fuel_gph         = float(S.get("fuel_gph_at_charge") or 0.0)  # interpolation-only

        if daily_runtime_hr <= 0 or fuel_gph <= 0:
            st.warning("Runtime or fuel burn not available. Configure a model and run the charge/runtime calc first.")
            st.stop()

        # Convert to monthly hours
        monthly_runtime_hr = daily_runtime_hr * float(days_in_month)

        # Use your existing costing helper (returns monthly numbers)
        fuel_total, total_cost, co2_output = calculate_costs_eboss(
            monthly_runtime_hr, fuel_gph, fuel_cost, rental, delivery, pm_cost
        )

        st.markdown("<div class='eboss-card'><strong>Monthly Cost Breakdown</strong></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <table style='width:100%; border: 1px solid #ccc; border-collapse: collapse;'>
              <tr><th style='text-align:left;'>Cost Component</th><th style='text-align:right;'>Amount ($)</th></tr>
              <tr><td>Rental</td><td style='text-align:right;'>{:.2f}</td></tr>
              <tr><td>Fuel</td><td style='text-align:right;'>{:.2f}</td></tr>
              <tr><td>Delivery</td><td style='text-align:right;'>{:.2f}</td></tr>
              <tr><td>PM Service</td><td style='text-align:right;'>{:.2f}</td></tr>
              <tr><td><strong>Total Monthly</strong></td><td style='text-align:right;'><strong>{:.2f}</strong></td></tr>
              <tr><td>Est. CO₂ Emissions (tons)</td><td style='text-align:right;'>{:.2f}</td></tr>
            </table>
            """.format(rental, fuel_total, delivery, pm_cost, total_cost, co2_output),
            unsafe_allow_html=True
        )

# If you had a print/export button defined elsewhere
try:
    print_button()
except Exception:
    pass

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

import streamlit as st
from datetime import date
import pandas as pd

@st.cache_data
def load_spec_table():
    url = "https://github.com/TimBuffington/Eboss-tool-V2/blob/main/assets/stats.xlsx"
    df = pd.read_excel(url)
    model_spec_table = {}

    for model in df["Model"].unique():
        model_df = df[df["Model"] == model]
        blocks = []
        current_block = {"header": "", "rows": []}

        for _, row in model_df.iterrows():
            if pd.isna(row["Spec Value"]):
                if current_block["rows"]:
                    blocks.append(current_block)
                    current_block = {"header": "", "rows": []}
                current_block["header"] = row["Spec Name"]
            else:
                current_block["rows"].append((row["Spec Name"], row["Spec Value"]))
        if current_block["rows"]:
            blocks.append(current_block)
        model_spec_table[model] = blocks

    return model_spec_table


def apply_custom_css():
    st.markdown("""
    <style>
    /* ===============================
       EBOSS® Form Styling: Concrete Theme – Enhanced + Aligned
       =============================== */

    /* Main form containers */
    .form-container {
        background-color: #e2e2e2 !important;  /* Light concrete */
        border-radius: 14px !important;
        padding: 1.2rem !important;
        border: 1px solid #ccc !important;
        min-height: 360px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12) !important;
        transition: all 0.2s ease-in-out;
    }

    .form-container:hover {
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.18) !important;
    }

    /* Section titles */
    .form-section-title {
        font-weight: 700;
        font-size: 1.3rem;
        font-family: 'Segoe UI', sans-serif;
        color: #111111;
        min-height: 2.5rem;
        margin-bottom: 1.2rem;
        text-shadow: 0 1px 1px rgba(0,0,0,0.04);
    }

    /* Labels (including selectbox and number input) */
    label, .form-section-title {
        display: block !important;
        margin-bottom: 0.4rem !important;
        font-weight: 600;
        font-size: 0.95rem;
        color: #111;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Form input fields */
    input, select, textarea,
    .stTextInput > div > div,
    .stNumberInput > div > input,
    .stSelectbox div[role="combobox"],
    .stSelectbox div[role="combobox"] input {
        background-color: #ffffff !important;
        color: #111111 !important;
        font-weight: bold !important;
        font-family: 'Segoe UI', sans-serif !important;
        border-radius: 8px !important;
        padding: 0.6rem 1rem !important;
        border: 1px solid #bbb !important;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);
        margin-bottom: 1.2rem !important;
        width: 100% !important;
        box-sizing: border-box !important;
        transition: border 0.2s, box-shadow 0.2s;
    }

    /* Focus / hover effect */
    input:focus, select:focus, textarea:focus,
    .stTextInput > div > div:focus-within,
    .stNumberInput > div > input:focus,
    .stSelectbox div[role="combobox"]:hover {
        border-color: #81BD47 !important;
        box-shadow: 0 0 0 2px rgba(129, 189, 71, 0.25);
    }

    /* Dropdown value text color fix */
    .stSelectbox div[role="combobox"] *,
    .stSelectbox div[role="combobox"] {
        -webkit-text-fill-color: #111111 !important;
        color: #111111 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ---- CSS for ALL PAGES ----
st.markdown("""
<style>
.stApp {
    background: url("https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/bg.png") no-repeat center center fixed !important;
    background-size: cover !important;
}
.logo-header {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 1.2rem;
    width: 100%;
}
.logo-header img {
    width: 600px;
    max-width: 90vw;
    height: auto;
    filter: drop-shadow(0 2px 16px rgba(0,0,0,0.28));
    margin-top: 1.0rem;
    border-radius: 0.4rem;
}
@media (max-width: 600px) {
    .logo-header img {
        width: 150px !important;
        max-width: 90vw !important;
        margin-top: 0.4rem;
    }
}
.form-section-title, h1 {
    font-family: 'Montserrat', 'Segoe UI', Arial, sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #fff;
    text-shadow: 2px 2px 10px #232325bb, 0 1px 2px #232325cc;
    text-align: center;
    margin-bottom: 1.6rem;
    letter-spacing: .04em;
}
.form-section-title {
    min-height: 2.5rem;
    font-weight: bold;
    font-size: 1.25rem;
    color: #111;
    margin-bottom: 1rem;
    font-family: 'Segoe UI', sans-serif;
}
.stButton > button, .eboss-hero-btn {
    width: 100%;
    min-width: 150px;
    max-width: 340px;
    margin: 1rem auto;
    padding: 1.1rem 0.5rem;
    background: #232325 !important;
    color: #fff !important;
    border-radius: 18px !important;
    border: none !important;
    font-size: 1.24rem !important;
    font-family: 'Montserrat', 'Segoe UI', Arial, sans-serif !important;
    font-weight: 700 !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.36), 0 2px 4px #0002, 0 0 0 #81BD47;
    text-shadow: 2px 2px 7px #000, 0 2px 10px #81BD4740;
    transition: box-shadow 0.22s, background 0.18s, transform 0.14s;
    cursor: pointer;
    display: block;
    outline: none;
    letter-spacing: .02em;
}
.stButton > button:hover, .stButton > button:focus, .eboss-hero-btn:hover, .eboss-hero-btn:focus {
    box-shadow: 0 0 30px 8px #81BD47, 0 10px 32px rgba(0,0,0,0.55);
    background: #2c2c2f !important;
    transform: scale(1.04) translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# =========================================================================================================
if "landing_shown" not in st.session_state:
    st.session_state.landing_shown = True
if "selected_form" not in st.session_state:
    st.session_state.selected_form = None
if "section" not in st.session_state:
    st.session_state.section = "main"
if "user_inputs" not in st.session_state:
    st.session_state.user_inputs = {}

# ---- UTILITY: LOGO & TITLE ----
def show_logo_and_title(title):
    st.markdown(
        '<div class="logo-header"><img src="https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/logo.png" alt="Company Logo"></div>',
        unsafe_allow_html=True
    )
    st.markdown(f'<h1 class="form-section-title">{title}</h1>', unsafe_allow_html=True)

#=====================================================================================================
def top_navbar():
    btn1, btn2, btn3, btn4, btn5 = st.columns(5)

    with btn1:
        if st.button("🧑‍🔧 Tech Specs", key="nav_tech_specs"):
            st.session_state.section = "tech_specs"
            st.session_state.run_tech_specs = True
            st.session_state.landing_shown = False
            st.rerun()

    with btn2:
        if st.button("⚡ Load Specs", key="nav_load_specs"):
            st.session_state.section = "load_specs"
            st.session_state.run_load_calc = True
            st.session_state.landing_shown = False
            st.rerun()

    with btn3:
        if st.button("⚖️ Compare", key="nav_compare"):
            st.session_state.section = "compare"
            st.session_state.run_compare = True
            st.session_state.landing_shown = False
            st.rerun()

    with btn4:
        if st.button("💰 Cost Analysis", key="nav_cost"):
            st.session_state.section = "cost"
            st.session_state.run_cost_calc = True
            st.session_state.landing_shown = False
            st.rerun()

    with btn5:
        if st.button("🧮 Parallel Calculator", key="nav_parallel_calc"):
            st.session_state.section = "parallel_calc"
            st.session_state.run_parallel_calc = True
            st.session_state.landing_shown = False
            st.rerun()


# ===============================================================================================
def landing_page():
    show_logo_and_title("EBOSS&reg Hybrid Energy System<br>Specs and Comparison Tool")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        if st.button("📋 Request a Demo", key="btn_demo"):
            st.session_state.selected_form = "demo"
            st.session_state.landing_shown = False
            st.rerun()
        if st.button("📋 Request On-Site Training", key="btn_training"):
            st.session_state.selected_form = "training"
            st.session_state.landing_shown = False
            st.rerun()
    with col2:
        st.markdown("""
            <a href="https://youtu.be/0Om2qO-zZfM?si=iTiPgIL2t-xDFixc" target="_blank" style="text-decoration:none;">
                <button class="eboss-hero-btn" type="button">
                    Learn How EBOSS&reg; Works
                </button>
            </a>
        """, unsafe_allow_html=True)


        if st.button("🚀 Launch EBOSS&reg Tool", key="btn_launch"):
            st.session_state.selected_form = "tool"
            st.session_state.landing_shown = False
            st.rerun()

# ---- DEMO FORM ----
def render_demo_form():
    show_logo_and_title("📝 Request a Demo")
    top_navbar()
    # ...your form code remains unchanged...

# ---- TRAINING FORM ----
def render_training_form():
    show_logo_and_title("📝 Request On‑Site Training")
    top_navbar()
    # ...your form code remains unchanged...
#=============================================================================================================================
   
def render_user_input_form():
    show_logo_and_title("Tech Specs")
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="form-section-title">EBOSS®</h3>', unsafe_allow_html=True)

        model = st.selectbox("Model", ["EBOSS 25 kVA", "EBOSS 70 kVA", "EBOSS125 kVA", "EBOSS 220 kVA", "EBOSS 400 kVA"], key="model_select")
        gen_type = st.selectbox("Type", ["Full Hybrid", "Power Module"], key="gen_type_select")
        kva_option = st.selectbox("Generator Size", ["25kVA", "45kVA", "65kVA", "125kVA", "220kVA", "400kVA"], key="kva_select") if gen_type == "Power Module" else None

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="form-section-title">Load</h3>', unsafe_allow_html=True)

        cont_load = st.number_input("Continuous Load", 0, 500, step=1, format="%d", key="cont_input")
        peak_load = st.number_input("Max Peak Load", 0, 500, step=1, format="%d", key="peak_input")

        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="form-section-title">Units</h3>', unsafe_allow_html=True)

        load_units = st.selectbox("Units", ["kW", "Amps"], key="unit_select")
        voltage = st.selectbox("Voltage", ["480V", "240V", "208V"], key="voltage_select")

        st.markdown('</div>', unsafe_allow_html=True)

    # Store values
    pf = 0.8
    v_val = int(voltage.replace("V", ""))

    if load_units == "Amps":
        cont_kw = (cont_load * (3 ** 0.5) * v_val * pf) / 1000
        peak_kw = (peak_load * (3 ** 0.5) * v_val * pf) / 1000
        if v_val != 480:
            cont_kw = (cont_load * (3 ** 0.5) * 480 * pf) / 1000
            peak_kw = (peak_load * (3 ** 0.5) * 480 * pf) / 1000
    else:
        cont_kw = cont_load
        peak_kw = peak_load
       
#========================================================================================================
def display_load_threshold_check(user_inputs):
    # Reference data
    EBOSS_KVA = {
        "EB25 kVA": 25,
        "EB70 kVA": 45,
        "EB125 kVA": 65,
        "EB220 kVA": 125,
        "EB400 kVA": 220
    }

    EBOSS_BATTERY_KWH = {
        "EB25 kVA": 15,
        "EB70 kVA": 25,
        "EB125 kVA": 50,
        "EB220 kVA": 75,
        "EB400 kVA": 125
    }

    model = user_inputs.get("model")
    gen_type = user_inputs.get("gen_type")
    cont_kw = user_inputs.get("cont_kw")

    if not model or model not in EBOSS_KVA or model not in EBOSS_BATTERY_KWH:
        st.warning("⚠️ Invalid model selected or missing data.")
        return

    pm_kva = EBOSS_KVA[model]
    battery_kwh = EBOSS_BATTERY_KWH[model]

    try:
        charge_rate = Eboss_Charge_Rates[pm_kva]["power_module" if gen_type == "Power Module" else "full_hybrid"]
        max_safe_limit = charge_rate * 0.9
        efficiency_target = battery_kwh * (2 / 3)
    except Exception as e:
        st.error("⚠️ Could not determine charge rate or battery specs for this model.")
        return

    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown("### 🔒 Load Threshold Check")

    if cont_kw > charge_rate:
        st.error(f"❌ Load ({cont_kw:.1f} kW) exceeds the max charge rate of {charge_rate:.1f} kW for {model}.")

        # 🔍 Find recommended model
        recommended = None
        for name, kva in EBOSS_KVA.items():
            new_rate = Eboss_Charge_Rates[kva]["power_module" if gen_type == "Power Module" else "full_hybrid"]
            if cont_kw <= new_rate * 0.9:
                recommended = name
                break

        if recommended:
            st.warning(f"💡 Recommended EBOSS size: **{recommended}** for your current load.")
        else:
            st.error("❌ No EBOSS size can handle this load. Consider splitting into multiple units.")
    elif cont_kw > max_safe_limit:
        st.warning(f"⚠️ Load is above 90% of the EBOSS charge rate ({charge_rate:.1f} kW).")
    elif cont_kw > efficiency_target:
        st.info(f"ℹ️ Load is within safe range but above the fuel-efficiency threshold (~{efficiency_target:.1f} kW).")
    else:
        st.success(f"✅ Load is optimal for fuel efficiency (≤ {efficiency_target:.1f} kW).")

    st.markdown('</div>', unsafe_allow_html=True)
#============================================================================================================================
def render_calculate_buttons():
    # Horizontal Rule for visual break
    st.markdown("""
    <hr style='
        border: none;
        border-top: 4px solid #999999;
        margin: 2.5rem 0 2rem 0;
        width: 100%;
    '>
    """, unsafe_allow_html=True)

    colA, _, colB = st.columns([1, 0.1, 1])

    with colA:
        if st.button("🧮 Calculate", key="btn_calculate"):
            active_page = st.session_state.get("section")

            if active_page == "load_specs":
                st.session_state.run_load_calc = True
            elif active_page == "cost":
                st.session_state.run_cost_calc = True
            elif active_page == "parallel_calc":
                st.session_state.run_parallel_calc = True
            elif active_page == "tech_specs":
                st.session_state.run_tech_specs = True
            elif active_page == "compare":
                st.session_state.run_compare = True

            st.session_state.calculation_done = True

    with colB:
        if st.button("♻️ Clear", key="btn_clear"):
            st.session_state.user_inputs = {
                "model": "EB25 kVA",
                "gen_type": "Full Hybrid",
                "kva_option": None,
                "cont_kw": 0,
                "peak_kw": 0,
                "raw_cont_load": 0,
                "raw_peak_load": 0,
                "load_units": "kW",
                "voltage": "480V"
            }
            # Clear all calculation flags
            for key in [
                "run_cost_calc", "run_load_calc", "run_parallel_calc",
                "run_tech_specs", "run_compare", "calculation_done"
            ]:
                st.session_state[key] = False
            st.rerun()


#==============================================================================================================================
    kva_map = {
        25: [0.67, 0.94, 1.26, 1.62],
        45: [1.04, 1.60, 2.20, 2.03],
        65: [2.9, 3.8, 4.8, 5.6],
        125: [5.0, 7.1, 9.1, 10.8],
        220: [8.8, 12.5, 16.6, 20.2],
        400: [14.9, 21.3, 28.6, 35.4]
    }
    breakpoints = [0.25, 0.5, 0.75, 1.0]
    values = kva_map.get(kva, kva_map[25])
    load_pct = max(0.25, min(load_pct, 1.0))
    for i in range(len(breakpoints) - 1):
        if breakpoints[i] <= load_pct <= breakpoints[i + 1]:
            x1, x2 = breakpoints[i], breakpoints[i + 1]
            y1, y2 = values[i], values[i + 1]
            return round(y1 + (load_pct - x1) * (y2 - y1) / (x2 - x1), 3)
    return values[0]
#=======================================================================================================
def calculate_runtime_specs(model, gen_type, cont_kw, kva):
    gen_kva = EBOSS_KVA.get(model, 0) if gen_type == "Full Hybrid" else float(kva.replace("kVA", ""))
    gen_kw = gen_kva * 0.8
    charge_kw = calculate_charge_rate(model, gen_type, kva)
    battery_kwh = {
        "EB25 kVA": 15,
        "EB70 kVA": 25,
        "EB125 kVA": 50,
        "EB220 kVA": 75,
        "EB400 kVA": 125
    }.get(model, 20)
    battery_life = battery_kwh / cont_kw if cont_kw else 0
    charge_time = battery_kwh / charge_kw if charge_kw else 0
    cycles_per_day = 24 / (battery_life + charge_time) if battery_life + charge_time > 0 else 0
    total_runtime = charge_time * cycles_per_day
    engine_pct = charge_kw / gen_kw if gen_kw else 0
    fuel_gph = interpolate_gph(int(gen_kva), engine_pct)
    return {
        "battery_kwh": battery_kwh,
        "battery_life": battery_life,
        "charge_time": charge_time,
        "runtime": total_runtime,
        "engine_pct": engine_pct,
        "fuel_gph": fuel_gph
    }

# ---- TECH SPECS PAGE ----
def render_tech_specs_page():
    show_logo_and_title("Tech Specs")
    top_navbar()

    import pandas as pd
    from collections import defaultdict

    @st.cache_data
    def load_transposed_spec_table():
        url = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/data/EBoss%20Stats%20final.xlsx"
        df = pd.read_excel(url, header=None)

        models = df.iloc[0, 1:].tolist()
        labels = df.iloc[:, 0].tolist()

        model_spec_data = {model: [] for model in models}
        current_header = None

        for i, label in enumerate(labels[2:], start=2):
            if pd.isna(df.iloc[i, 1]):
                current_header = df.iloc[i, 0]
            else:
                for col_index, model in enumerate(models, start=1):
                    model_spec_data[model].append({
                        "section": current_header,
                        "label": df.iloc[i, 0],
                        "value": df.iloc[i, col_index]
                    })
        return model_spec_data

    complete_model_spec_data = load_transposed_spec_table()
    selected_model = st.session_state.get("model_select", "EBOSS 25 kVA")
    model_data = complete_model_spec_data.get(selected_model, [])

    if not model_data:
        st.warning(f"No data found for model: {selected_model}")
        return

    grouped = defaultdict(list)
    for row in model_data:
        grouped[row["section"]].append((row["label"], row["value"]))

    for section, rows in grouped.items():
        st.markdown(f"""
        <div style="background-color:#232325; color:white; font-weight:bold;
                    padding:0.7rem 1rem; border-radius:8px; font-size:1rem;
                    margin:2rem 0 1rem 0; text-transform:uppercase;">
            {section}
        </div>
        """, unsafe_allow_html=True)

        for i in range(0, len(rows), 2):
            col1, col2 = st.columns(2)
            with col1:
                if i < len(rows):
                    label, value = rows[i]
                    st.markdown(f"""
                    <div style="b


# ---- LOAD SPECS PAGE ----
def render_load_specs_page():
    show_logo_and_title("Load Specs")
    render_user_input_form()
    top_navbar()
    inputs = st.session_state.user_inputs

    model = inputs.get("model")
    pm_kva = EBOSS_KVA[model]
    gen_type = inputs.get("gen_type")
    cont_kw = inputs.get("cont_kw")
    peak_kw = inputs.get("peak_kw")

    if gen_type == "Power Module":
        default_charge_rate = inputs.get("pm_charge_rate", Eboss_Charge_Rates[pm_kva]["power_module"])
        max_charge_rate = Eboss_Charge_Rates[pm_kva]["max"]
        charge_rate = st.number_input(
            "Set Power Module Charge Rate (kW)",
            min_value=1.0,
            max_value=max_charge_rate,
            value=float(default_charge_rate),
            step=0.5,
            key="user_pm_charge_rate"
        )
        if charge_rate > max_charge_rate:
            st.error(
                f"Charge rate cannot exceed max allowed ({max_charge_rate} kW) for this EBOSS size. "
                "Increase EBOSS size or lower load."
            )
            st.stop()
        st.session_state.user_inputs["pm_charge_rate"] = charge_rate

    elif gen_type == "Full Hybrid":
        default_charge_rate = Eboss_Charge_Rates[pm_kva]["full_hybrid"]
        max_charge_rate = Eboss_Charge_Rates[pm_kva]["max"]
        charge_rate = st.number_input(
            "Set Full Hybrid Charge Rate (kW)",
            min_value=1.0,
            max_value=max_charge_rate,
            value=float(default_charge_rate),
            step=0.5,
            key="user_full_charge_rate"
        )
        if charge_rate > max_charge_rate:
            st.error(
                f"Charge rate cannot exceed max allowed ({max_charge_rate} kW) for this EBOSS size. "
                "Increase EBOSS size or lower load."
            )
            st.stop()
        st.session_state.user_inputs["charge_rate"] = charge_rate

    # ...rest of your load specs calculations/output here...

#======================================================================================================

def render_compare_page():
    show_logo_and_title("Comparison")
    render_user_input_form()
    top_navbar()

    # 4. Continue with the rest of the page
    model = st.session_state.get("model_select", "")
    if not model:
        st.warning("Please select an EBOSS model.")
        return
    

    if not st.session_state.get("run_compare"):
        st.warning("Please fill out the form and click 'Calculate' before viewing comparison results.")
        return

    # Placeholder for future comparison output
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="form-section-title">🔍 EBOSS® vs Standard Generator</h3>', unsafe_allow_html=True)
    st.markdown("Comparison data will be displayed here.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Optional: reset flag
    st.session_state.run_compare = False

# ---- COST ANALYSIS PAGE ----
def render_cost_analysis_page():
    show_logo_and_title("Cost Analysis")
    top_navbar()
    inputs = st.session_state.user_inputs
    model = inputs.get("model")
    gen_type = inputs.get("gen_type")
    cont_kw = inputs.get("cont_kw")
    kva_option = inputs.get("kva_option")
    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="form-section-title">💰 Cost Inputs</h3>', unsafe_allow_html=True)
        fuel_price = st.number_input("Fuel Price ($/gal)", 0.0, 100.0, 3.5, 0.01)
        delivery_fee = st.number_input("Delivery Fee ($)", 0.0, 1000.0, 75.0, 1.0)
        pm_interval = st.number_input("PM Interval (hrs)", 10.0, 1000.0, 500.0, 10.0)
        pm_cost = st.number_input("Cost per PM ($)", 0.0, 5000.0, 150.0, 10.0)
        eboss_rent = st.number_input("EBOSS&reg Monthly Rental ($)", 0.0, 100000.0, 3800.0, 50.0)
        std_rent = st.number_input("Standard Generator Monthly Rental ($)", 0.0, 100000.0, 3500.0, 50.0)
        std_gen = st.selectbox("Standard Generator Size", list(STANDARD_GENERATORS.keys()))
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("✅ Run Cost Comparison"):
            runtime = calculate_runtime_specs(model, gen_type, cont_kw, kva_option)
            std_runtime = 720  # Full 24x30 month
            std_gph = STANDARD_GENERATORS[std_gen]
            from math import ceil
            def fmt(x): return f"{x:,.2f}"
            def render_cost_comparison_table():
                e_fuel = runtime["fuel_gph"] * runtime["runtime"]
                s_fuel = std_gph * std_runtime
                e_cost = e_fuel * fuel_price
                s_cost = s_fuel * fuel_price
                e_pms = ceil(runtime["runtime"] / pm_interval)
                s_pms = ceil(std_runtime / pm_interval)
                e_pm_cost = e_pms * pm_cost
                s_pm_cost = s_pms * pm_cost
                e_co2 = e_fuel * 22.4
                s_co2 = s_fuel * 22.4
                e_total = eboss_rent + e_cost + delivery_fee + e_pm_cost
                s_total = std_rent + s_cost + delivery_fee + s_pm_cost
                diff = s_total - e_total
                rows = [
                    ("Generator Size", f"{EBOSS_KVA[model]} kVA / {int(EBOSS_KVA[model]*0.8)} kW", std_gen, ""),
                    ("Rental Cost ($)", eboss_rent, std_rent, std_rent - eboss_rent),
                    ("Fuel Used (gal)", e_fuel, s_fuel, s_fuel - e_fuel),
                    ("Fuel Cost ($)", e_cost, s_cost, s_cost - e_cost),
                    ("PM Services", e_pms, s_pms, s_pms - e_pms),
                    ("PM Cost ($)", e_pm_cost, s_pm_cost, s_pm_cost - e_pm_cost),
                    ("CO₂ Emissions (lbs)", e_co2, s_co2, s_co2 - e_co2),
                    ("Delivery Fee ($)", delivery_fee, delivery_fee, 0),
                    ("**Total Cost ($)**", e_total, s_total, diff)
                ]
                st.markdown('<div class="form-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="form-section-title">📊 Monthly Cost Comparison</h3>', unsafe_allow_html=True)
                st.markdown(f"""
                <table style='width:100%; text-align:left; font-size:0.9rem;'>
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>EBOSS&reg Model<br>{model}</th>
                            <th>Standard Generator<br>{std_gen}</th>
                            <th>Difference</th>
                        </tr>
                    </thead>
                    <tbody>
                """, unsafe_allow_html=True)
                for label, e_val, s_val, d_val in rows:
                    st.markdown(f"""
                        <tr>
                            <td>{label}</td>
                            <td>{fmt(e_val) if isinstance(e_val, (int, float)) else e_val}</td>
                            <td>{fmt(s_val) if isinstance(s_val, (int, float)) else s_val}</td>
                            <td><strong>{fmt(d_val) if isinstance(d_val, (int, float)) else d_val}</strong></td>
                        </tr>
                    """, unsafe_allow_html=True)
                st.markdown("</tbody></table></div>", unsafe_allow_html=True)
            render_cost_comparison_table()
    # Print CSS and print button (add here if desired)


# ==========Parallel Page============

def render_parallel_calculator_page():
    show_logo_and_title("Parallel Calculator")
    top_navbar()
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown("## Parallel/Hybrid Sizing Tool")

    # --- Load requirements
    st.markdown("### Required Project Load")
    required_cont_kw = st.number_input("Required Continuous Load (kW)", 0, 2000, step=1)
    required_peak_kw = st.number_input("Required Max Peak Load (kW)", 0, 2500, step=1)

    # --- Sizing preference
    st.markdown("### Sizing Criterion")
    sizing_pref = st.radio(
        "Do you want to size for **optimal fuel efficiency** (max continuous = 2/3 battery kWh) or **minimum number of items** (max allowed per your chart)?",
        ["Optimal fuel efficiency", "Minimum item count"], horizontal=True
    )

    # --- Show user inventory
    st.markdown("### EBOSS Units in Inventory")
    eboss_inventory = {}
    eboss_charge_overrides = {}
    for model in EBOSS_KVA.keys():
        col1, col2 = st.columns([2,1])
        with col1:
            qty = st.number_input(f"{model} (quantity)", 0, 20, step=1, key=f"eboss_{model}")
        with col2:
            eboss_kva = EBOSS_KVA[model]
            set_rate = Eboss_Charge_Rates[eboss_kva]["power_module"]
            max_rate = Eboss_Charge_Rates[eboss_kva]["max"]
            charge_rate = st.number_input(
                f"Set charge rate for {model} (default {set_rate} kW)", min_value=1.0, max_value=max_rate,
                value=float(set_rate), step=0.5, key=f"charge_{model}"
            )
            if charge_rate > max_rate:
                st.error(f"Charge rate for {model} cannot exceed max allowed ({max_rate} kW).")
                st.stop()
            eboss_charge_overrides[model] = charge_rate
        eboss_inventory[model] = qty

    st.markdown("### Generators in Inventory")
    gen_inventory = {}
    for gen in STANDARD_GENERATORS.keys():
        qty = st.number_input(f"{gen} (quantity)", 0, 10, step=1, key=f"gen_{gen}")
        gen_inventory[gen] = qty

    st.markdown("### What do you want to calculate?")
    need_option = st.radio(
        "Show me:",
        ["Total number of items required", "Additional items needed (based on inventory)"],
        horizontal=True
    )

    # --- Calculate needed EBoss units
    if st.button("🔢 Calculate Paralleled System"):
        # Determine per-unit kW based on sizing_pref
        unit_capacity = {}
        for model in EBOSS_KVA.keys():
            if sizing_pref == "Optimal fuel efficiency":
                battery_kwh = {
                    "EB25 kVA": 15,
                    "EB70 kVA": 25,
                    "EB125 kVA": 50,
                    "EB220 kVA": 75,
                    "EB400 kVA": 125,
                }[model]
                ideal_kw = (2/3) * battery_kwh
            else:
                ideal_kw = eboss_charge_overrides[model]
            unit_capacity[model] = ideal_kw

        # Step 1: Apply user's inventory
        total_supported_kw = 0
        used_inventory = {}
        for model, qty in eboss_inventory.items():
            if qty > 0:
                model_kw = unit_capacity[model]
                model_total_kw = qty * model_kw
                total_supported_kw += model_total_kw
                used_inventory[model] = qty

        # Step 2: Determine how many more units are needed
        additional_units = {}
        deficit = max(0, required_cont_kw - total_supported_kw)
        if deficit > 0:
            for model, model_kw in sorted(unit_capacity.items(), key=lambda x: -x[1]):
                need_qty = int(deficit // model_kw)
                if deficit % model_kw != 0:
                    need_qty += 1
                if need_qty > 0:
                    additional_units[model] = need_qty
                    deficit -= need_qty * model_kw
                    if deficit <= 0:
                        break

        # Results for EBoss units
        st.markdown("### 📊 Results: EBOSS Units")
        if need_option == "Total number of items required":
            for model in unit_capacity:
                total = used_inventory.get(model, 0) + additional_units.get(model, 0)
                if total > 0:
                    st.write(f"{model}: {total} (each set to {unit_capacity[model]:.1f} kW)")
        else:
            for model, qty in additional_units.items():
                if qty > 0:
                    st.write(f"Still need: {qty} x {model} (set to {unit_capacity[model]:.1f} kW)")

        # Calculate recommended generator sizing for EBOSS units
        st.markdown("### 🔌 Generator Sizing for EBOSS System")
        pf = 0.8
        total_eboss_kw = sum((used_inventory.get(model, 0) + additional_units.get(model, 0)) * unit_capacity[model] for model in EBOSS_KVA.keys())
        min_gen_kva = total_eboss_kw / pf
        st.write(f"Recommended generator size for charging: **{total_eboss_kw:.1f} kW** ({min_gen_kva:.1f} kVA, PF=0.8)")

        # --- Standard Generator Comparison Button
        if st.button("Compare to Standard Generator System"):
            st.markdown("## Standard Generator Comparison")

            # Calculate total kW output from all EBoss units
            st.markdown(f"**Total EBoss kW Output:** {total_eboss_kw:.1f} kW")

            # 1. Show generator count per size for EBoss system charging
            st.markdown("#### Generator Count for EBOSS Charging:")
            required_gen_kw = total_eboss_kw
            generator_rows = []
            remaining_gen_kw = required_gen_kw
            for gen, gph in sorted(STANDARD_GENERATORS.items(), key=lambda x: -EBOSS_KVA.get(x[0].split(" ")[0] + " kVA", 0)):
                gen_kw = float(gen.split("/")[1].replace("kW", "").strip())
                qty = int(remaining_gen_kw // gen_kw)
                if remaining_gen_kw % gen_kw != 0:
                    qty += 1
                if qty > 0:
                    generator_rows.append((gen, qty))
                    remaining_gen_kw -= qty * gen_kw
                    if remaining_gen_kw <= 0:
                        break
            for gen, qty in generator_rows:
                st.write(f"{gen}: {qty}")

            # 2. Show generator runtime and fuel
            st.markdown("#### Generator Runtime & Fuel Analysis:")
            total_gph = sum(STANDARD_GENERATORS[gen] * qty for gen, qty in generator_rows)
            st.write(f"**Total GPH (gallons per hour):** {total_gph:.2f} gph")
            st.write(f"**Gallons per day:** {total_gph * 24:.1f} gal")
            st.write(f"**Gallons per week:** {total_gph * 24 * 7:.1f} gal")
            st.write(f"**Gallons per month (30 days):** {total_gph * 24 * 30:.1f} gal")

            # 3. Now compare to using only standard generators (no EBOSS)
            st.markdown("### Standard-Only Generator System (No EBOSS):")
            std_rows = []
            std_remaining_kw = required_cont_kw
            for gen, gph in sorted(STANDARD_GENERATORS.items(), key=lambda x: -float(x[0].split("/")[1].replace("kW", "").strip())):
                gen_kw = float(gen.split("/")[1].replace("kW", "").strip())
                qty = int(std_remaining_kw // gen_kw)
                if std_remaining_kw % gen_kw != 0:
                    qty += 1
                if qty > 0:
                    std_rows.append((gen, qty))
                    std_remaining_kw -= qty * gen_kw
                    if std_remaining_kw <= 0:
                        break
            for gen, qty in std_rows:
                st.write(f"{gen}: {qty}")

            std_total_gph = sum(STANDARD_GENERATORS[gen] * qty for gen, qty in std_rows)
            st.write(f"**Total Standard Gen GPH:** {std_total_gph:.2f} gph")
            st.write(f"**Gallons per day:** {std_total_gph * 24:.1f} gal")
            st.write(f"**Gallons per week:** {std_total_gph * 24 * 7:.1f} gal")
            st.write(f"**Gallons per month (30 days):** {std_total_gph * 24 * 30:.1f} gal")

            # --- Print-friendly button with logo and title ---
            today = date.today().strftime("%B %d, %Y")
            st.markdown("""
            <style>
            @media print {
                body * { visibility: hidden; }
                .print-logo, .print-logo * { visibility: visible; }
                .form-container, .form-container * { visibility: visible; }
                .form-container {
                    position: relative;
                    background: white !important;
                    color: black !important;
                    box-shadow: none !important;
                }
                .form-container h3, th, td {
                    color: black !important;
                    text-shadow: none !important;
                }
            }
            </style>
            """, unsafe_allow_html=True)
            st.markdown(f'''
            <div class="print-logo" style="text-align:center; margin-top:2rem;">
              <img src="https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/logo.png" width="240"><br><br>
              <div style="font-size:1.3rem; font-weight:bold;">
                EBOSS&reg Parallel Sizing and Generator Comparison Report
              </div>
              <div style="font-size:0.9rem; margin-top:0.2rem;">{today}</div>
              <div style="font-size:0.95rem; margin-top:0.8rem;">
                <b>Load Parameters:</b> {required_cont_kw} kW continuous, {required_peak_kw} kW peak
              </div>
            </div>
            ''', unsafe_allow_html=True)
            st.markdown("""
            <button class="eboss-hero-btn" onclick="window.print()" style="margin: 0 auto; display: block;">
                 Print Parallel Calculation
            </button>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)



# ---- NAVIGATION BLOCK (at the bottom) ----
if st.session_state.landing_shown:
    landing_page()
    st.stop()
elif st.session_state.selected_form == "demo":
    render_demo_form()
    st.stop()
elif st.session_state.selected_form == "training":
    render_training_form()
    st.stop()
elif st.session_state.section == "tech_specs":
    render_tech_specs_page()
    st.stop()
elif st.session_state.section == "load_specs":
    render_load_specs_page()
    st.stop()
elif st.session_state.section == "compare":
    # render_compare_page()  # define as needed
    st.write("Compare Page (to be implemented)")
    st.stop()
elif st.session_state.section == "cost":
    render_cost_analysis_page()
    st.stop()
elif st.session_state.selected_form == "tool":
    top_navbar()
    render_user_input_form()
    st.stop()
elif st.session_state.section == "parallel_calc":
    render_parallel_calculator_page()
    st.stop()


# ---- FOOTER ----
st.markdown("""
<style>
.footer {
    position: relative;
    bottom: 0;
    width: 100%;
    padding: 1rem 0;
    text-align: center;
    font-size: 0.9rem;
    background: rgba(0,0,0,0.7);
    color: white;
    margin-top: 3rem;
    border-top: 1px solid rgba(255,255,255,0.1);
    text-shadow: 1px 1px 2px rgba(0,0,0,0.4);
}
.footer a {
    color: #81BD47;
    text-decoration: none;
    font-weight: bold;
}
</style>
<div class="footer">
    ANA EBOSS&reg;Spec and Comparison Tool &nbsp; | &nbsp;
    <a href="https://anacorp.com/hybrid-energy-systems/" target="_blank">
        anacorp.com/hybrid-energy-systems
    </a>
</div>
""", unsafe_allow_html=True)

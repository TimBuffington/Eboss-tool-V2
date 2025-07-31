import streamlit as st
import requests
from datetime import date

import streamlit as st

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
input, select, textarea, .stSelectbox > div > div, .stTextInput > div > div {
    background-color: #e0e0e0 !important;
    border: .5px solid #232325 !important;
    color: #111 !important;        /* Black text */
    font-weight: bold !important;
    font-family: 'Montserrat', 'Segoe UI', Arial, sans-serif !important;
    text-shadow: none !important;  /* No text shadow */
    border-radius: 12px !important;
    box-shadow: none !important;   /* No sunken/3D effect */
   81BD47
    padding: 0.65rem 1.1rem !important;
}
input:focus, select:focus, textarea:focus, 
.stSelectbox > div > div:focus, .stTextInput > div > div:focus {
    border: 2px solid #81BD47 !important;
     box-shadow: none !important;
}

a, a:visited, a:active {
    text-decoration: none !important;
    color: inherit !important;
}
</style>
""", unsafe_allow_html=True)

# ---- STATE ----
if "landing_shown" not in st.session_state:
    st.session_state.landing_shown = True
if "selected_form" not in st.session_state:
    st.session_state.selected_form = None

def show_logo_and_title(title):
    st.markdown(
        '<div class="logo-header"><img src="https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/logo.png" alt="Company Logo"></div>',
        unsafe_allow_html=True
    )
    st.markdown(f'<h1 class="form-section-title">{title}</h1>', unsafe_allow_html=True)

def landing_page():
    show_logo_and_title("EBOSS® Hybrid Energy System<br>Specs and Comparison Tool")
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
                🎥 Learn How EBOSS&reg; Works
            </button>
        </a>
        """, unsafe_allow_html=True)
        if st.button("🚀 Launch EBOSS® Tool", key="btn_launch"):
            st.session_state.selected_form = "tool"
            st.session_state.landing_shown = False
            st.rerun()


# ---- DEMO FORM ----
def render_demo_form():
    show_logo_and_title("📝 Request a Demo")
    if st.session_state.get("demo_success"):
        st.success("✅ Thank you for your submission!")
        st.write("Would you like to return to the landing page or open the EBOSS Spec Tool?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Back to Landing Page", key="demo_back"):
                st.session_state.selected_form = None
                st.session_state.landing_shown = True
                st.session_state.demo_success = False
                st.rerun()
        with col2:
            if st.button("🚀 Open EBOSS Spec Tool", key="demo_tool"):
                st.session_state.selected_form = "tool"
                st.session_state.landing_shown = False
                st.session_state.demo_success = False
                st.rerun()
        st.stop()

    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    colA, colB = st.columns(2)
    with colA:
        first_name = st.text_input("First Name")
        company = st.text_input("Company")
        phone = st.text_input("Phone Number")
        city = st.text_input("City")
        email = st.text_input("Email Address")
    with colB:
        last_name = st.text_input("Last Name")
        title = st.text_input("Title")
        street = st.text_input("Street Address")
        state = st.text_input("State")
        zip_code = st.text_input("Zip Code")
    submit, cancel = st.columns(2)
    with submit:
        if st.button("📨 Submit Request", key="demo_submit"):
            st.session_state.demo_success = True
            st.rerun()
    with cancel:
        if st.button("Cancel", key="demo_cancel"):
            st.session_state.selected_form = None
            st.session_state.landing_shown = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---- TRAINING FORM ----
def render_training_form():
    show_logo_and_title("📝 Request On‑Site Training")
    if st.session_state.get("training_success"):
        st.success("✅ Thank you for your submission!")
        st.write("Would you like to return to the landing page or open the EBOSS Spec Tool?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Back to Landing Page", key="training_back"):
                st.session_state.selected_form = None
                st.session_state.landing_shown = True
                st.session_state.training_success = False
                st.rerun()
        with col2:
            if st.button("🚀 Open EBOSS Spec Tool", key="training_tool"):
                st.session_state.selected_form = "tool"
                st.session_state.landing_shown = False
                st.session_state.training_success = False
                st.rerun()
        st.stop()

    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    colA, colB = st.columns(2)
    with colA:
        first_name = st.text_input("First Name", key="train_first_name")
        company = st.text_input("Company", key="train_company")
        phone = st.text_input("Phone Number", key="train_phone")
        city = st.text_input("City", key="train_city")
        email = st.text_input("Email Address", key="train_email")
        attendees = st.number_input("Number of Attendees", min_value=1, step=1, key="attendees")
    with colB:
        last_name = st.text_input("Last Name", key="train_last_name")
        title = st.text_input("Title", key="train_title")
        street = st.text_input("Street Address", key="train_street")
        state = st.text_input("State", key="train_state")
        zip_code = st.text_input("Zip Code", key="train_zip")
        model = st.selectbox("EBOSS® Model for Training", ["EB25 kVA", "EB70 kVA", "EB125 kVA", "EB220 kVA", "EB400 kVA"])
        train_type = st.radio("Training Type", ["Sales", "Technical"], horizontal=True)
        onsite = st.radio("Is an EBOSS® unit already onsite?", ["Yes", "No"], horizontal=True)
        train_date = st.date_input("Preferred Training Date")
        tv = st.checkbox("A TV is available to present training materials")
    submit, cancel = st.columns(2)
    with submit:
        if st.button("📨 Submit Training Request", key="train_submit"):
            st.session_state.training_success = True
            st.rerun()
    with cancel:
        if st.button("Cancel", key="train_cancel"):
            st.session_state.selected_form = None
            st.session_state.landing_shown = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---- HOME PAGE / MAIN TOOL ----
def render_home():
    show_logo_and_title("EBOSS® Model Selection Tool")
    st.markdown("<!-- Your tool's content goes here -->")
    st.write("Welcome to the EBOSS Spec Tool Home Page!")
  

# ---- NAVIGATION ----
if st.session_state.landing_shown:
    landing_page()
    st.stop()
elif st.session_state.selected_form == "demo":
    render_demo_form()
    st.stop()
elif st.session_state.selected_form == "training":
    render_training_form()
    st.stop()
elif st.session_state.selected_form == "tool":
    render_home()
    st.stop()
# ──────────────────────────────
# 📊 EBOSS&reg;Reference Data
# ──────────────────────────────
EBOSS_KVA = {
    "EB25 kVA": 25,
    "EB70 kVA": 45,
    "EB125 kVA": 65,
    "EB220 kVA": 125,
    "EB400 kVA": 220
}
STANDARD_GENERATORS = {
    "25 kVA / 20 kW": 1.8,
    "45 kVA / 36 kW": 2.7,
    "65 kVA / 52 kW": 3.5,
    "125 kVA / 100 kW": 6.5,
    "220 kVA / 176 kW": 12.5,
    "400 kVA / 320 kW": 22.0
}
# ──────────────────────────────
# 🔢 Core Formulas
# ──────────────────────────────
def calculate_charge_rate(model, gen_type, kva=None):
    if gen_type == "Full Hybrid":
        gen_kva = EBOSS_KVA.get(model, 0)
        return round(gen_kva * 0.8 * 0.98, 2)
    elif gen_type == "Power Module" and kva:
        try:
            gen_kva = float(kva.replace("kVA", ""))
            return round(gen_kva * 0.8 * 0.90 * 0.98, 2)
        except:
            return 0.0
    return 0.0


def interpolate_gph(kva, load_pct):
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


#──────────────────────────────
# 🚀 Main UI
# ──────────────────────────────

def render_home():
    # Show logo and main tool header
    show_logo_and_title("EBOSS® Model Selection Tool")

    with st.container():
        col1, col2 = st.columns([1, 1])

        # Left Column — System Configuration
        with col1:
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="form-section-title">⚙️ System Configuration</h3>', unsafe_allow_html=True)

            model = st.selectbox("EBOSS® Model", list(EBOSS_KVA.keys()))
            gen_type = st.selectbox("EBOSS® Type", ["Full Hybrid", "Power Module"])

            if gen_type == "Power Module":
                kva_option = st.selectbox("Generator Size", ["25kVA", "45kVA", "65kVA", "125kVA", "220kVA", "400kVA"])
            else:
                kva_option = None

            st.markdown('</div>', unsafe_allow_html=True)

        # Right Column — Load Requirements
        with col2:
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="form-section-title">⚡ Load Requirements</h3>', unsafe_allow_html=True)

            cont_kw = st.number_input("Continuous Load (kW)", 0.0, 500.0, step=1.0)
            peak_kw = st.number_input("Max Peak Load (kW)", 0.0, 500.0, step=1.0)

            st.markdown('</div>', unsafe_allow_html=True)

    # 🔘 Button Panel (NOW with Contact Us)
    btn1, btn2, btn3, btn4, btn5 = st.columns(5)

    with btn1:
        if st.button("📋 View Specs"):
            st.session_state.section = "specs"

    with btn2:
        if st.button("⚡ Load-Based Specs"):
            st.session_state.section = "load"

    with btn3:
        if st.button("⚖️ Compare"):
            st.session_state.section = "compare"

    with btn4:
        if st.button("💰 Cost Analysis"):
            st.session_state.section = "cost"

    with btn5:
        if st.button("📞 Contact Us"):
            st.markdown("""
            <script>
            window.open("https://anacorp.com/contact/", "_blank");
            </script>
            """, unsafe_allow_html=True)

# ──────────────────────────────
# 💰 Cost Analysis Modal + Table
# ──────────────────────────────
if st.session_state.section == "cost":
    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="form-section-title">💰 Cost Inputs</h3>', unsafe_allow_html=True)

        fuel_price = st.number_input("Fuel Price ($/gal)", 0.0, 100.0, 3.5, 0.01)
        delivery_fee = st.number_input("Delivery Fee ($)", 0.0, 1000.0, 75.0, 1.0)
        pm_interval = st.number_input("PM Interval (hrs)", 10.0, 1000.0, 500.0, 10.0)
        pm_cost = st.number_input("Cost per PM ($)", 0.0, 5000.0, 150.0, 10.0)
        eboss_rent = st.number_input("EBOSS&reg;Monthly Rental ($)", 0.0, 100000.0, 3800.0, 50.0)
        std_rent = st.number_input("Standard Generator Monthly Rental ($)", 0.0, 100000.0, 3500.0, 50.0)
        std_gen = st.selectbox("Standard Generator Size", list(STANDARD_GENERATORS.keys()))

        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("✅ Run Cost Comparison"):
        runtime = calculate_runtime_specs(model, gen_type, cont_kw, kva_option)
        std_runtime = 720  # Full 24x30 month
        std_gph = STANDARD_GENERATORS[std_gen]

        from math import ceil
        def fmt(x): return f"{x:,.2f}"

        # Table logic
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
                        <th>EBOSS&reg;Model<br>{model}</th>
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
st.markdown(f"""
    <style>
    @media print {{
        body * {{
            visibility: hidden;
        }}
        .print-logo, .print-logo * {{
            visibility: visible;
        }}
        .form-container, .form-container * {{
            visibility: visible;
        }}
        .form-container {{
            position: relative;
            background: white !important;
            color: black !important;
            box-shadow: none !important;
        }}
        .form-container h3, th, td {{
            color: black !important;
            text-shadow: none !important;
        }}
    }}
    </style>
""", unsafe_allow_html=True)

from datetime import date
today = date.today().strftime("%B %d, %Y")

html = f'''
<div class="print-logo" style="text-align:center; margin-top:2rem;">
       page_icon="assets/logo.png”, 
       width="200"><br><br>
  <div style="font-size:1.2rem; font-weight:bold;">
    EBOSS&reg; Hybrid Energy System vs Standard Diesel Generator Cost Comparison
  </div>
  <div style="font-size:0.9rem; margin-top:0.2rem;">{today}</div>
</div>

<div style="text-align:right; margin-top:1rem;">
  <button onclick="window.print()" style="
    background-color:#81BD47;
    color:white;
    padding:0.6rem 1.2rem;
    font-size:1rem;
    border:none;
    border-radius:6px;
    cursor:pointer;
    box-shadow:2px 2px 4px rgba(0,0,0,0.3);
  ">
    🖨️ Print Report
  </button>
</div>
'''

st.markdown(html, unsafe_allow_html=True)

# ──────────────────────────────
# 📋 EBOSS&reg;Technical Specs
# ──────────────────────────────
def render_specs(model):
    specs_data = {
        "EB25 kVA": {
            "Battery Capacity": "15 kWh",
            "Inverter": "Pure Sine Wave",
            "Voltage Options": "120/240 (1Φ) • 208/480 (3Φ)",
            "Weight": "8,200 lbs",
            "Dimensions": '108" x 45" x 62"',
            "Warranty": "2 Years"
        },
        "EB70 kVA": {
            "Battery Capacity": "25 kWh",
            "Inverter": "Pure Sine Wave",
            "Voltage Options": "120/240 (1Φ) • 208/480 (3Φ)",
            "Weight": "13,200 lbs",
            "Dimensions": '108" x 60" x 62"',
            "Warranty": "2 Years"
        },
        # Add more specs for other models as needed
    }

    data = specs_data.get(model)
    if not data:
        st.warning("Specs not available for this model.")
        return

    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="form-section-title">📋 Technical Specs</h3>', unsafe_allow_html=True)
    for key, value in data.items():
        st.markdown(f"**{key}:** {value}")
    st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────
# ⚡ Load-Based Specs Output
# ──────────────────────────────
def render_load_specs(model, gen_type, cont_kw, kva_option):
    specs = calculate_runtime_specs(model, gen_type, cont_kw, kva_option)
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="form-section-title">⚡ Load-Based Performance</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.metric("Battery Capacity", f"{specs['battery_kwh']} kWh")
    col1.metric("Battery Longevity", f"{specs['battery_life']:.2f} hrs")
    col1.metric("Charge Time", f"{specs['charge_time']:.2f} hrs")

    col2.metric("Charges/Day", f"{24 / (specs['battery_life'] + specs['charge_time']):.2f}")
    col2.metric("Runtime/Day", f"{specs['runtime']:.2f} hrs")
    col2.metric("Fuel Consumption", f"{specs['fuel_gph']:.2f} GPH")

    st.markdown('</div>', unsafe_allow_html=True)

# Show selected section
if st.session_state.section == "specs":
    render_specs(model)

elif st.session_state.section == "load":
    render_load_specs(model, gen_type, cont_kw, kva_option)

# ──────────────────────────────
# 🔗 Branded Footer (Sticky)
# ──────────────────────────────
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

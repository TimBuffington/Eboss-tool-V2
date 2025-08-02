import streamlit as st
from datetime import date
import pandas as pd
def render_card(label, value):
    st.markdown(f'''
    <div class="card">
        <div class="card-label">{label}</div>
        <div class="card-value">{value}</div>
    </div>
    ''', unsafe_allow_html=True)

def apply_custom_css():
    st.markdown("""
    <style>
    /* === GLOBAL === */
    html, body, .stApp {
        font-family: 'Segoe UI', sans-serif;
        font-size: 1.1rem;
        line-height: 1.6;
        background: url("https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/bg.png") no-repeat center center fixed;
        background-size: cover;
        color: #fff;
        margin: 0;
        padding: 0;
    }

/* === HEADINGS === */
h1, .form-section-title {
    font-family: 'Montserrat', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    text-align: center;
    color: #fff;
    text-shadow: 2px 2px 10px rgba(0,0,0,0.6);
    margin-bottom: 1.5rem;
}

/* === CARD BLOCK === */
.card {
    background: linear-gradient(145deg, #000, #1b1b1b);
    border-radius: 16px;
    padding: 1.4rem 1.8rem;
    margin-bottom: 1.5rem;
    border: 1px solid #939598;
    box-shadow: 0 8px 20px rgba(0,0,0,0.65),
                inset 0 1px 2px rgba(255,255,255,0.05);
    transition: transform 0.2s ease-in-out;
    color: #fff;
}

.card-label {
    font-size: 1rem;
    font-weight: 600;
    color: #81BD47;
    margin-bottom: 0.4rem;
    text-shadow: 0 1px 1px rgba(0,0,0,0.6);
}

.card-value {
    font-size: 1.2rem;
    font-weight: 700;
    color: #fff;
    text-shadow: 0 2px 4px rgba(0,0,0,0.4);
}

/* === BUTTONS === */
.stButton > button, .eboss-hero-btn {
    width: 100%;
    max-width: 340px;
    margin: 1rem auto;
    padding: 1.1rem 0.5rem;
    background: #232325;
    color: #fff;
    border-radius: 18px;
    font-size: 1.2rem;
    font-weight: 700;
    border: none;
    box-shadow: 0 8px 24px rgba(0,0,0,0.36);
    transition: all 0.2s ease-in-out;
}

.stButton > button:hover {
    background: #2c2c2f;
    transform: scale(1.04) translateY(-2px);
    box-shadow: 0 0 30px 8px #81BD47;
}

/* === FORM INPUTS === */
input, select, textarea {
    background-color: #fff;
    color: #111;
    font-weight: bold;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    border: 1px solid #bbb;
    width: 100%;
    box-sizing: border-box;
    margin-bottom: 1rem;
    transition: border 0.2s, box-shadow 0.2s;
}

input:focus, select:focus, textarea:focus {
    border-color: #81BD47;
    box-shadow: 0 0 0 2px rgba(129,189,71,0.25);
}

/* === LOGO === */
.logo-header {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 1rem;
}

.logo-header img {
    width: 90%;
    max-width: 360px;
    height: auto;
    filter: drop-shadow(0 2px 16px rgba(0,0,0,0.28));
    border-radius: 0.4rem;
}

/* === MOBILE === */
@media (max-width: 600px) {
    .logo-header img {
        width: 80% !important;
    }
    h1, .form-section-title {
        font-size: 1.5rem;
    }
    .card-label {
        font-size: 0.95rem;
    }
    .card-value {
        font-size: 1.05rem;
    }
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
spec_data = {
    "EBOSS 25 kVA": {
        "Maximum Intermittent Load": [
            ("Three-phase", "30 kva / 24 kw"),
            ("Single-phase", "20 kva / 16 kw"),
            ("Frequency", "60 Hz"),
            ("Simultaneous voltage", "Yes 120v / 240v / 208v / 480v"),
            ("Voltage regulation", "Adjustable"),
            ("Max. Intermittent 208v", "70 A / 20 kW"),
            ("Max. Intermittent amp-load 480v", "30 A / 25 kW"),
            ("Motor start rating - 3 second 208v", "104 A / 30 kW"),
            ("Motor start rating - 3 second 480v", "45 A / 37 kW")
        ],
        "Maximum Continuous Load": [
            ("Generator Size", "25 kVA / 20 kW"),
            ("Three-phase output", "23 kVA / 19 kW"),
            ("Single-phase output", "20 kVA / 16 kW"),
            ("Simultaneous voltage", "Yes 120v / 240v / 208v / 480v"),
            ("Max. Continuous load @208v", "70 A / 20.2 kW"),
            ("Max. Continuous load @480v", "30 A / 20 kW")
        ],
        "Engine Specs": [
            ("Runtime Hrs per Day", "Calculated"),
            ("Battery Storage", "15 kWH")
        ]
    },
    "EBOSS 70 kVA": {
        "Maximum Intermittent Load": [
            ("Three-phase", "70 kVA / 56 kW"),
            ("Single-phase", "47 kVA / 37 kW"),
            ("Frequency", "60 Hz"),
            ("Simultaneous voltage", "Yes 120v / 240v / 208v / 480v"),
            ("Voltage regulation", "Adjustable"),
            ("Max. Intermittent 208v", "194 A / 56 kW"),
            ("Max. Intermittent amp-load 480v", "84 A / 70 kW"),
            ("Motor start rating - 3 second 208v", "291 A / 84 kW"),
            ("Motor start rating - 3 second 480v", "126 A / 104 kW")
        ],
        "Maximum Continuous Load": [
            ("Generator Size", "45 kVA / 36 kW"),
            ("Three-phase output", "42 kVA / 33 kW"),
            ("Single-phase output", "28 kVA / 22 kW"),
            ("Simultaneous voltage", "Yes 120v / 240v / 208v / 480v"),
            ("Max. Continuous load @208v", "119 A / 34.5 kW"),
            ("Max. Continuous load @480v", "54 A / 36 kW")
        ],
        "Engine Specs": [
            ("Runtime Hrs per Day", "Calculated"),
            ("Battery Storage", "25 kWH")
        ]
    },
    "EBOSS125 kVA": {
        "Maximum Intermittent Load": [
            ("Three-phase", "125 kVA / 100 kW"),
            ("Single-phase", "N/A / N/A"),
            ("Frequency", "60 Hz"),
            ("Simultaneous voltage", "Yes 208v / 480v"),
            ("Voltage regulation", "Adjustable"),
            ("Max. Intermittent 208v", "345 A / 99.5 kW"),
            ("Max. Intermittent amp-load 480v", "150 A / 125 kW"),
            ("Motor start rating - 3 second 208v", "532 A / 153 kW"),
            ("Motor start rating - 3 second 480v", "231 A / 192 kW")
        ],
        "Maximum Continuous Load": [
            ("Generator Size", "70 kVA / 56 kW"),
            ("Three-phase output", "62 kVA / 50 kW"),
            ("Single-phase output", "N/A"),
            ("Simultaneous voltage", "Yes 208v / 480v"),
            ("Max. Continuous load @208v", "167 A / 48 kW"),
            ("Max. Continuous load @480v", "76 A / 50.5 kW")
        ],
        "Engine Specs": [
            ("Runtime Hrs per Day", "Calculated"),
            ("Battery Storage", "50 kWH")
        ]
    },
    "EBOSS 220 kVA": {
        "Maximum Intermittent Load": [
            ("Three-phase", "220 kVA / 176 kW"),
            ("Single-phase", "N/A / N/A"),
            ("Frequency", "60 Hz"),
            ("Simultaneous voltage", "Yes 208v / 480v"),
            ("Voltage regulation", "Adjustable"),
            ("Max. Intermittent 208v", "700 A / 201 kW"),
            ("Max. Intermittent amp-load 480v", "303 A / 252 kW"),
            ("Motor start rating - 3 second 208v", "1065 A / 307 kW"),
            ("Motor start rating - 3 second 480v", "461 A / 383 kW")
        ],
        "Maximum Continuous Load": [
            ("Generator Size", "125 kVA / 100 kW"),
            ("Three-phase output", "120 kVA / 96 kW"),
            ("Single-phase output", "N/A"),
            ("Simultaneous voltage", "Yes 208v / 480v"),
            ("Max. Continuous load @208v", "328 A / 94 kW"),
            ("Max. Continuous load @480v", "150 A / 99.8 kW")
        ],
        "Engine Specs": [
            ("Runtime Hrs per Day", "Calculated"),
            ("Battery Storage", "75 kWH")
        ]
    },
    "EBOSS 400 kVA": {
        "Maximum Intermittent Load": [
            ("Three-phase", "400 kVA / 320 kW"),
            ("Single-phase", "N/A"),
            ("Frequency", "60 Hz"),
            ("Simultaneous voltage", "Yes 208v / 480v"),
            ("Voltage regulation", "Adjustable"),
            ("Max. Intermittent 208v", "481 A / 138.5 kW"),
            ("Max. Intermittent amp-load 480v", "769 A / 639 kW"),
            ("Motor start rating - 3 second 208v", "1776 A / 511 kW"),
            ("Motor start rating - 3 second 480v", "769 A / 639 kW")
        ],
        "Maximum Continuous Load": [
            ("Generator Size", "220 kVA / 176 kW"),
            ("Three-phase output", "210 kVA / 168 kW"),
            ("Single-phase output", "N/A"),
            ("Simultaneous voltage", "Yes 208v / 480v"),
            ("Max. Continuous load @208v", "481 A"),
            ("Max. Continuous load @480v", "—")
        ],
        "Engine Specs": [
            ("Runtime Hrs per Day", "Calculated"),
            ("Battery Storage", "125 kWH")
        ]
    }
}

def top_navbar():
    btn0, btn1, btn2, btn3, btn4, btn5 = st.columns(6)

    with btn0:
        if st.button("📥 User Input", key="nav_input"):
            st.session_state.selected_form = "tool"
            st.session_state.section = "input"
            st.session_state.landing_shown = False
            st.rerun()

    with btn1:
        if st.button("🧑‍🔧 Tech Specs", key="nav_tech_specs"):
            st.session_state.selected_form = "tool"
            st.session_state.section = "tech_specs"
            st.session_state.run_tech_specs = True
            st.session_state.landing_shown = False
            st.rerun()

    with btn2:
        if st.button("⚡ Load Specs", key="nav_load_specs"):
            st.session_state.selected_form = "tool"
            st.session_state.section = "load_specs"
            st.session_state.run_load_calc = True
            st.session_state.landing_shown = False
            st.rerun()

    with btn3:
        if st.button("⚖️ Compare", key="nav_compare"):
            st.session_state.selected_form = "tool"
            st.session_state.section = "compare"
            st.session_state.run_compare = True
            st.session_state.landing_shown = False
            st.rerun()

    with btn4:
        if st.button("💰 Cost Analysis", key="nav_cost"):
            st.session_state.selected_form = "tool"
            st.session_state.section = "cost"
            st.session_state.run_cost_calc = True
            st.session_state.landing_shown = False
            st.rerun()

    with btn5:
        if st.button("🧮 Parallel Calculator", key="nav_parallel_calc"):
            st.session_state.selected_form = "tool"
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


    if st.button("🚀 Launch EBOSS® Tool", key="btn_launch"):
        st.session_state.selected_form = "tool"
        st.session_state.section = "input"  # 👈 or "tech_specs" if you prefer
        st.session_state.landing_shown = False
        st.rerun()




# ──────────────────────────────
# 📝 Contact Form Logic
# ──────────────────────────────
def render_contact_form(form_type="demo"):
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown(f'<h3 class="form-section-title">📝 Request { "a Demo" if form_type == "demo" else "On‑Site Training" }</h3>', unsafe_allow_html=True)

    with st.form(f"{form_type}_form"):
        st.text_input("First Name", key="first_name")
        st.text_input("Last Name", key="last_name")
        st.text_input("Company", key="company")
        st.text_input("Title", key="title")
        st.text_input("Phone Number", key="phone")
        st.text_input("Street Address", key="street")
        st.text_input("City", key="city")
        st.text_input("State", key="state")
        st.text_input("Zip Code", key="zip")
        st.text_input("Email Address", key="email")

        if form_type == "training":
            st.selectbox("EBOSS® Model for Training", ["EB25 kVA", "EB70 kVA", "EB125 kVA", "EB220 kVA", "EB400 kVA"], key="model")
            st.radio("Training Type", ["Sales", "Technical"], horizontal=True, key="train_type")
            st.radio("Is an EBOSS® unit already onsite?", ["Yes", "No"], horizontal=True, key="onsite")
            st.date_input("Preferred Training Date", key="train_date")
            st.number_input("Number of Attendees", min_value=1, step=1, key="attendees")
            tv = st.checkbox("A TV is available to present training materials")
        else:
            tv = None

        submitted = st.form_submit_button("📨 Submit Request")

    if submitted:
        if form_type == "demo":
            user_data = {k: st.session_state[k] for k in ["first_name", "last_name", "company", "title", "phone", "street", "city", "state", "zip", "email"]}
            status = submit_demo_request(user_data)
        else:
            user_data = {k: st.session_state[k] for k in ["first_name", "last_name", "company", "title", "phone", "street", "city", "state", "zip", "email", "model", "train_type", "onsite", "train_date", "attendees"]}
            user_data["train_date"] = str(user_data["train_date"])
            user_data["tv"] = "TV available" if tv else "TV not available"
            status = submit_training_request(user_data)

        if status == 200:
            st.success("✅ Your request was successfully submitted.")
        else:
            st.error("❌ Submission failed. Please try again.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔁 Continue with Tool"):
                st.session_state.landing_shown = False
                st.session_state.show_contact_form = False
                st.rerun()
        with col2:
            if st.button("🌐 Visit ANA Website"):
                st.markdown("""<script>window.open("https://anacorp.com", "_blank");</script>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────
# 🏠 Landing Page Logic
# ──────────────────────────────
if "landing_shown" not in st.session_state:
    st.session_state.landing_shown = True
if "show_contact_form" not in st.session_state:
    st.session_state.show_contact_form = False
if "form_type" not in st.session_state:
    st.session_state.form_type = None

if st.session_state.landing_shown:
    apply_custom_css()
    st.image("https://anacorp.com/wp-content/uploads/2023/10/ANA-ENERGY-LOGO-PADDED.png", width=250)
    st.markdown("<h1>EBOSS® Hybrid Energy System Specs and Comparison Tool</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 Request a Demo"):
            st.session_state.form_type = "demo"
            st.session_state.show_contact_form = True
            st.session_state.landing_shown = False
            st.rerun()
    with col2:
        if st.button("📋 Request On-Site Training"):
            st.session_state.form_type = "training"
            st.session_state.show_contact_form = True
            st.session_state.landing_shown = False
            st.rerun()

    col3, col4 = st.columns(2)
    with col3:
        if st.button("🎥 Learn How EBOSS® Works"):
            st.markdown("""<script>window.open("https://youtu.be/0Om2qO-zZfM?si=iTiPgIL2t-xDFixc", "_blank");</script>""", unsafe_allow_html=True)
    with col4:
        if st.button("🚀 Launch EBOSS® Tool"):
            st.session_state.landing_shown = False
            st.session_state.show_contact_form = False
            st.session_state.form_type = None
            st.rerun()

    st.stop()

if st.session_state.show_contact_form:
    render_contact_form(form_type=st.session_state.form_type)

#=============================================================================================================================
   
def render_user_input_form():
    show_logo_and_title("Tech Specs")

    with st.container():
        with st.columns(3)[0]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-label">EBOSS®</div>', unsafe_allow_html=True)

            st.session_state.user_inputs["model"] = st.selectbox("Model", ["EBOSS 25 kVA", "EBOSS 70 kVA", "EBOSS125 kVA", "EBOSS 220 kVA", "EBOSS 400 kVA"], key="model_select")
            st.session_state.user_inputs["gen_type"] = st.selectbox("Type", ["Full Hybrid", "Power Module"], key="gen_type_select")
            if st.session_state.user_inputs["gen_type"] == "Power Module":
                st.session_state.user_inputs["kva_option"] = st.selectbox("Generator Size", ["25kVA", "45kVA", "65kVA", "125kVA", "220kVA", "400kVA"], key="kva_select")

            st.markdown('</div>', unsafe_allow_html=True)

        with st.columns(3)[1]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-label">Load</div>', unsafe_allow_html=True)

            st.session_state.user_inputs["raw_cont_load"] = st.number_input("Continuous Load", 0, 500, step=1, format="%d", key="cont_input")
            st.session_state.user_inputs["raw_peak_load"] = st.number_input("Max Peak Load", 0, 500, step=1, format="%d", key="peak_input")

            st.markdown('</div>', unsafe_allow_html=True)

        with st.columns(3)[2]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-label">Units</div>', unsafe_allow_html=True)

            st.session_state.user_inputs["load_units"] = st.selectbox("Units", ["kW", "Amps"], key="unit_select")
            st.session_state.user_inputs["voltage"] = st.selectbox("Voltage", ["480V", "240V", "208V"], key="voltage_select")

            st.markdown('</div>', unsafe_allow_html=True)

    # ---- Kw conversion logic
    pf = 0.8
    v_val = int(st.session_state.user_inputs["voltage"].replace("V", ""))
    cont = st.session_state.user_inputs["raw_cont_load"]
    peak = st.session_state.user_inputs["raw_peak_load"]

    if st.session_state.user_inputs["load_units"] == "Amps":
        # Normalize voltage for calcs
        st.session_state.user_inputs["cont_kw"] = (cont * (3 ** 0.5) * 480 * pf) / 1000
        st.session_state.user_inputs["peak_kw"] = (peak * (3 ** 0.5) * 480 * pf) / 1000
    else:
        st.session_state.user_inputs["cont_kw"] = cont
        st.session_state.user_inputs["peak_kw"] = peak

    top_navbar()  # ✅ Nav buttons moved below input cards

def render_user_input_page():
    show_logo_and_title("User Input")
    render_user_input_form()
    top_navbar()

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

    model = st.session_state.get("model_select", "EBOSS 25 kVA")
    specs = spec_data.get(model)

    if not specs:
        st.warning(f"No data available for {model}")
        return

    for section, items in specs.items():
        st.markdown(f'''
        <div class="card" style="background-color: #636569; color: white; font-weight: 700;
            font-size: 1.2rem; padding: 0.8rem 1.5rem; border-radius: 12px;
            margin: 2rem 0 1rem 0; text-align: center; text-transform: uppercase;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
            {section}
        </div>
        ''', unsafe_allow_html=True)

        for i in range(0, len(items), 2):
            col1, col2 = st.columns(2)

            for idx, col in enumerate([col1, col2]):
                if i + idx < len(items):
                    label, value = items[i + idx]
                    with col:
                        render_card(label, value)

    top_navbar()

# ---- LOAD SPECS PAGE ----
def render_load_specs_page():
    show_logo_and_title("Load Specs")

    # 👉 Render form UI
    render_user_input_form()

    # 👉 Validate inputs globally
    enforce_session_validation()
    inputs = st.session_state.user_inputs
    kva = EBOSS_KVA[inputs["model"]]
    spec = Eboss_Specs[kva]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🔒 Load Threshold Check")

    charge_rate = inputs["charge_rate"]
    battery_kwh = spec["battery_kwh"]
    cont_kw = inputs["cont_kw"]
    peak_kw = inputs["peak_kw"]
    max_safe_limit = spec["max_charge"] * 0.9
    efficiency_target = battery_kwh * (2 / 3)

    # ⚙️ Threshold visual feedback
    if cont_kw > spec["max_charge"]:
        st.error(f"❌ Load ({cont_kw:.1f} kW) exceeds max charge rate ({spec['max_charge']} kW).")
    elif cont_kw > max_safe_limit:
        st.warning(f"⚠️ Load is above 90% of the charge rate ({max_safe_limit:.1f} kW).")
    elif cont_kw > efficiency_target:
        st.info(f"ℹ️ Load is within safe range but above the fuel-efficiency threshold (~{efficiency_target:.1f} kW).")
    else:
        st.success(f"✅ Load is optimal for fuel efficiency (≤ {efficiency_target:.1f} kW).")

    # 🔺 Peak load check
    if peak_kw > spec["max_peak"]:
        st.error(f"❌ Peak load ({peak_kw:.1f} kW) exceeds EBOSS peak limit ({spec['max_peak']} kW).")

    st.markdown('</div>', unsafe_allow_html=True)

    top_navbar()


def render_compare_page():
    import re

    show_logo_and_title("Compare EBOSS vs Standard Generator")
    top_navbar()

    model = st.session_state.get("model_select", "EBOSS 25 kVA")
    eboss_specs = spec_data.get(model, {})
    std_specs = std_gen_data.get(model, {})
    cont_kw = st.session_state.user_inputs.get("cont_kw", 10)

    def extract_kva(m):
        match = re.search(r"(\d+)", m)
        return int(match.group(1)) if match else 0

    kva = extract_kva(model)
    charge_kw = Eboss_Charge_Rates[kva]["full_hybrid"]
    gen_kw = kva * 0.8
    battery_kwh = {
        "EBOSS 25 kVA": 15,
        "EBOSS 70 kVA": 25,
        "EBOSS125 kVA": 50,
        "EBOSS 220 kVA": 75,
        "EBOSS 400 kVA": 125
    }.get(model, 0)

    battery_life = battery_kwh / cont_kw if cont_kw else 0
    charge_time = battery_kwh / charge_kw if charge_kw else 0
    cycles_per_day = 24 / (battery_life + charge_time) if battery_life + charge_time > 0 else 0
    runtime_hrs = charge_time * cycles_per_day
    eboss_gph = interpolate_gph(kva, charge_kw / gen_kw if gen_kw else 1)
    std_gph = interpolate_gph(kva, 1.0)

    eboss_gpd = round(eboss_gph * runtime_hrs, 2)
    std_gpd = round(std_gph * 24, 2)
    eboss_gpw = round(eboss_gpd * 7, 2)
    std_gpw = round(std_gpd * 7, 2)
    eboss_gpm = round(eboss_gpd * 30, 2)
    std_gpm = round(std_gpd * 30, 2)

    spec_layout = {
        "Maximum Intermittent Load": [
            "Three-phase", "Single-phase", "Frequency", "Simultaneous voltage", "Voltage regulation",
            "Max. Intermittent 208v", "Max. Intermittent amp-load 480v",
            "Motor start rating - 3 second 208v", "Motor start rating - 3 second 480v"
        ],
        "Maximum Continuous Load": [
            "Generator Size", "Three-phase output", "Single-phase output", "Simultaneous voltage",
            "Max. Continuous load @208v", "Max. Continuous load @480v"
        ],
        "Engine Specs": [
            ("Runtime Hrs per Day", f"{round(runtime_hrs,1)}", "24"),
            ("Battery Storage", f"{battery_kwh} kWH", "0 kWH"),
            ("Gallons per Day", f"{eboss_gpd} gal", f"{std_gpd} gal"),
            ("Gallons per Week", f"{eboss_gpw} gal", f"{std_gpw} gal"),
            ("Gallons per Month", f"{eboss_gpm} gal", f"{std_gpm} gal")
        ]
    }

    for section, rows in spec_layout.items():
        st.markdown(f'''
        <div class="card" style="background-color: #636569; color: white; font-weight: 700;
            font-size: 1.2rem; padding: 0.8rem 1.5rem; border-radius: 12px;
            margin: 2rem 0 1rem 0; text-align: center; text-transform: uppercase;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
            {section}
        </div>
        ''', unsafe_allow_html=True)

        if isinstance(rows[0], str):
            eboss_sec = dict(eboss_specs.get(section, []))
            std_sec = dict(std_specs.get(section, []))

            for label in rows:
                col1, col2, col3 = st.columns(3)
                with col1:
                    render_card("Metric", label)
                with col2:
                    render_card("EBOSS®", eboss_sec.get(label, "–"))
                with col3:
                    render_card("Standard Gen", std_sec.get(label, "–"))
        else:
            for label, eboss_val, std_val in rows:
                col1, col2, col3 = st.columns(3)
                with col1:
                    render_card("Metric", label)
                with col2:
                    render_card("EBOSS®", eboss_val)
                with col3:
                    render_card("Standard Gen", std_val)

# ---- COST ANALYSIS PAGE ----
def render_cost_analysis_page():
    from math import ceil
    from datetime import date

    show_logo_and_title("Cost Analysis")
    top_navbar()

    inputs = st.session_state.user_inputs
    model = inputs.get("model")
    gen_type = inputs.get("gen_type")
    cont_kw = inputs.get("cont_kw")
    kva_option = inputs.get("kva_option")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 💰 Cost Inputs")

    fuel_price = st.number_input("Fuel Price ($/gal)", 0.0, 100.0, 3.5, 0.01)
    delivery_fee = st.number_input("Delivery Fee ($)", 0.0, 1000.0, 75.0, 1.0)
    pm_interval = st.number_input("PM Interval (hrs)", 10.0, 1000.0, 500.0, 10.0)
    pm_cost = st.number_input("Cost per PM ($)", 0.0, 5000.0, 150.0, 10.0)
    eboss_rent = st.number_input("EBOSS® Monthly Rental ($)", 0.0, 100000.0, 3800.0, 50.0)
    std_rent = st.number_input("Standard Generator Monthly Rental ($)", 0.0, 100000.0, 3500.0, 50.0)
    std_gen = st.selectbox("Standard Generator Size", list(STANDARD_GENERATORS.keys()))

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("✅ Run Cost Comparison"):
        runtime = calculate_runtime_specs(model, gen_type, cont_kw, kva_option)
        std_runtime = 720  # 30 days × 24 hrs
        std_gph = STANDARD_GENERATORS[std_gen]

        def fmt(x): return f"{x:,.2f}"

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

        # ---- COST TABLE ----
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

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"<h3 class='form-section-title'>📊 Monthly Cost Comparison</h3>", unsafe_allow_html=True)

        st.markdown(f"""
        <table style='width:100%; text-align:left; font-size:0.95rem;'>
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>EBOSS® Model<br>{model}</th>
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

        # ---- PRINT-FRIENDLY BUTTON ----
        today = date.today().strftime("%B %d, %Y")
        st.markdown("""
        <style>
        @media print {
            body * { visibility: hidden; }
            .card, .card * { visibility: visible; }
            .card {
                background: white !important;
                color: black !important;
                box-shadow: none !important;
            }
            .form-section-title, th, td {
                color: black !important;
                text-shadow: none !important;
            }
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f'''
        <div class="card" style="text-align:center;">
            <div style="font-size:1.3rem;font-weight:bold;margin-bottom:1rem;">
                EBOSS® Cost Analysis Report
            </div>
            <div style="font-size:0.9rem;">{today}</div>
            <button class="eboss-hero-btn" onclick="window.print()" style="margin-top:1.5rem;">
                 🖨️ Print Cost Report
            </button>
        </div>
        ''', unsafe_allow_html=True)


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
    render_compare_page()
    st.stop()
elif st.session_state.section == "cost":
    render_cost_analysis_page()
    st.stop()
elif st.session_state.section == "input":
    render_user_input_page()
    st.stop()

    st.stop()
elif st.session_state.section == "parallel_calc":
    render_parallel_calculator_page()
    st.stop()
# ---- FOOTER ----

st.markdown(r"""
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

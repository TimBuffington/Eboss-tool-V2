import streamlit as st
from datetime import date
import pandas as pd
from itertools import combinations_with_replacement
from typing import Dict, List, Tuple, Any


def apply_custom_css():
    st.markdown("""
    <style>
    /* === GLOBAL STYLES === */
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

    /* === HEADER & SECTION TITLES === */
    h1, .form-section-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        text-align: center;
        color: #fff;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.6);
        margin-bottom: 1.5rem;
    }

    /* === CARD === */
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

    /* === MOBILE STYLES === */
    @media (max-width: 768px) {
        .stColumn {
            flex: 1 0 100% !important;
            max-width: 100% !important;
        }
        h1, .form-section-title {
            font-size: 1.6rem !important;
        }
        .card-label, .card-value {
            font-size: 1rem !important;
        }
        .logo-header img {
            width: 80% !important;
        }
    }
    .card-label {
    display: block;
    font-size: 1.1rem;
    font-weight: 700;
    color: #81BD47;
    margin-bottom: 0.6rem;
    text-align: left;
    text-transform: uppercase;
}

    </style>
    """, unsafe_allow_html=True)
@st.cache_data(show_spinner=False)
def load_std_gen_specs_from_excel(path: str = "/mnt/data/Grn Compare.xlsx") -> Dict[str, Dict[str, List[Tuple[str, Any]]]]:
    """
    Read the diesel generator reference workbook and return:
    {
      "25": {"Maximum Intermittent Load":[("Three-phase","..."), ...],
             "Maximum Continuous Load":[(...), ...],
             "Engine Specs & Fuel Use":[(...), ...]},
      "70": {...}, ...
    }
    Notes:
    - We accept a few common header spellings and coerce to our spec keys.
    - If the file is missing or structure is unexpected, we return {} and the UI will show "–".
    """
    try:
        xls = pd.ExcelFile(path)
    except Exception:
        return {}

    # Try to be flexible: use the first sheet by default
    try:
        df = pd.read_excel(xls, xls.sheet_names[0])
    except Exception:
        return {}

    # Normalize column names
    df.columns = [str(c).strip().lower() for c in df.columns]

    # Heuristics for key columns
    # Expect at least: 'kva' or 'model', 'section', 'spec'/'metric', 'value'
    # We'll try a few likely variants
    def pick(*names):
        for n in names:
            if n in df.columns:
                return n
        return None

    col_kva     = pick("kva", "rating_kva", "rating", "size_kva", "model_kva")
    col_model   = pick("model", "name")
    col_section = pick("section", "category")
    col_label   = pick("spec", "metric", "label", "item")
    col_value   = pick("value", "val", "data")

    if not (col_section and col_label and col_value and (col_kva or col_model)):
        # Structure is too different — return empty to keep app stable
        return {}

    # Extract "kva_key" we’ll group by (stringified integer like "25", "70", …)
    def kva_key(row):
        import re
        if col_kva:
            try:
                return str(int(round(float(row[col_kva]))))
            except Exception:
                pass
        # fallback: get number from model like "125 kVA"
        m = re.search(r"(\d+)", str(row.get(col_model, "")))
        return m.group(1) if m else None

    # Normalize sections to our expected keys if possible
    def map_section(name: str) -> str:
        n = str(name).strip().lower()
        if "intermittent" in n: return "Maximum Intermittent Load"
        if "continuous"  in n: return "Maximum Continuous Load"
        if "engine" in n or "fuel" in n: return "Engine Specs & Fuel Use"
        return name  # keep original if we can’t map

    std: Dict[str, Dict[str, List[Tuple[str, Any]]]] = {}
    for _, row in df.iterrows():
        key = kva_key(row)
        if not key:
            continue
        section = map_section(row[col_section])
        label   = str(row[col_label]).strip()
        value   = row[col_value]
        std.setdefault(key, {}).setdefault(section, []).append((label, value))

    return std
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
    "EBOSS 125 kVA": {
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
EBOSS_KVA = {
    "EBOSS 25 kVA": 25,
    "EBOSS 70 kVA": 70,
    "EBOSS 125 kVA": 125,
    "EBOSS 220 kVA": 220,
    "EBOSS 400 kVA": 400
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

# ==== UNIFIED MODEL KEYS (make sure your spec_data uses these exact strings) ====
VALID_MODELS = ["EBOSS 25 kVA", "EBOSS 70 kVA", "EBOSS 125 kVA", "EBOSS 220 kVA", "EBOSS 400 kVA"]

# kVA name -> kVA value
EBOSS_KVA = {
    "EBOSS 25 kVA": 25,
    "EBOSS 70 kVA": 70,
    "EBOSS 125 kVA": 125,
    "EBOSS 220 kVA": 220,
    "EBOSS 400 kVA": 400,
}

# Battery sizes (kWh) for EBOSS®
EBOSS_BATTERY_KWH = {
    "EBOSS 25 kVA": 15,
    "EBOSS 70 kVA": 25,
    "EBOSS 125 kVA": 50,
    "EBOSS 220 kVA": 75,
    "EBOSS 400 kVA": 125,
}

# Charge-rate envelope per kVA (you can tune these with real data)
Eboss_Specs = {
    25:  {"full_hybrid": 19.5, "power_module": 18.5,  "max_charge": 20, "max_peak": 20.0, "max_cont":18, "battery_kwh": 15},
    70:  {"full_hybrid": 36, "power_module": 233, "max_charge": 45, "max_peak": 56.0, "max_cont": 40, "battery_kwh": 25},
    125: {"full_hybrid": 52, "power_module": 48, "max_charge": 65, "max_peak": 125.0, "max_cont":58, "battery_kwh": 50},
    220: {"full_hybrid": 100, "power_module": 96, "max_charge": 125,"max_peak": 252.0, "max_cont":112, "battery_kwh": 75},
    400: {"full_hybrid": 176.0,"power_module": 166,"max_charge": 220.0,"max_peak": 639.0, "max_cont":198, "battery_kwh": 125},
}

# Simple fuel maps for a standard generator running near nameplate (gal/hour)
STANDARD_GENERATORS = {
    "25 kVA (≈20 kW)",
    "45 kVA (≈36 kW)",
    "65 kVA (≈52 kW)",
    "125 kVA (≈100 kW)",
    "220 kVA (≈176 kW)",
    "400 kVA (≈320 kW)"
}

def interpolate_gph(kva: int, load_pct: float) -> float:
    """
    Very rough interpolation of fuel burn (gallons/hour) vs. load % for a generator of given kVA.
    Calibrated with made-up but monotonic points—replace with field data when available.
    """
    # piecewise points per kVA @ 25/50/75/100% load
    table = {
        25:  [0.7, 1.0, 1.3, 1.6],
        45:  [1.0, 1.5, 2.1, 2.7],
        65:  [1.5, 2.3, 3.3, 4.3],
        125: [2.9, 4.2, 5.9, 7.8],
        220: [5.5, 8.2, 11.0, 13.5],
        400: [9.5, 14.0, 18.5, 22.0],
    }
    xs = [0.25, 0.5, 0.75, 1.0]
    ys = table.get(int(kva), table[25])
    load = max(0.25, min(load_pct or 0.25, 1.0))
    # linear interpolate
    for i in range(len(xs) - 1):
        if xs[i] <= load <= xs[i + 1]:
            x1, x2 = xs[i], xs[i + 1]
            y1, y2 = ys[i], ys[i + 1]
            return y1 + (load - x1) * (y2 - y1) / (x2 - x1)
    return ys[-1]

def calculate_charge_rate(model: str, eboss_type: str, pm_gen: str | None) -> float:
    """
    Charge rate is determined ONLY by the EBOSS model + mode.
    PM generator size does NOT change the charge rate; it's validated separately.
    Always clamp to max_charge for safety.
    """
    # Resolve model kVA (handles "EBOSS 125 kVA" and minor key quirks)
    model_kva = EBOSS_KVA.get(model)
    if model_kva is None:
        import re
        m = re.search(r"(\d+)", model or "")
        model_kva = int(m.group(1)) if m else 0

    spec = Eboss_Specs[model_kva]
    max_charge = float(spec["max_charge"])

    if eboss_type == "Full Hybrid":
        charge_rate = float(spec["full_hybrid"])
    else:
        # Power Module
        charge_rate = float(spec["power_module"])

    # Safety: never exceed EBOSS max_charge
    return min(charge_rate, max_charge)

def get_charge_rate(model: str, eboss_type: str) -> float:
    """
    Charge rate depends only on model + mode.
    PM generator size does NOT affect the rate; it's validated separately.
    Always clamp to max_charge for safety.
    """
    if model not in EBOSS_KVA:
        raise ValueError(f"Unknown model: {model}")

    kva = EBOSS_KVA[model]              # numeric kVA for the EBOSS model
    spec = Eboss_Specs[kva]             # envelope for this kVA
    base_rate = spec["power_module"] if eboss_type == "Power Module" else spec["full_hybrid"]
    return min(float(base_rate), float(spec["max_charge"]))  # safety cap only

def validate_pm_generator(model: str, pm_gen: str) -> tuple[bool, list[str]]:
    """
    Power Module validation.
    - If gen kW < required PM charge rate → block (cannot continue).
    - If gen kW > 2/3 of PM charge rate → warn (allowed, but fuel efficiency may be worse).
    Returns (can_continue, messages).
    """
    messages: list[str] = []
    can_continue = True

    # Model → kVA → PM charge rate
    model_kva = EBOSS_KVA.get(model)
    if model_kva is None:
        import re
        m = re.search(r"(\d+)", model or "")
        model_kva = int(m.group(1)) if m else 0

    pm_charge_rate = float(Eboss_Specs[model_kva]["power_module"])

    # Parse PM generator kW capacity (~0.8 × kVA)
    import re
    m = re.search(r"(\d+)", str(pm_gen))
    pm_kva_val = int(m.group(1)) if m else 0
    pm_gen_kw_cap = 0.8 * pm_kva_val if pm_kva_val > 0 else 0.0

    # Hard fail if undersized
    if pm_gen_kw_cap < pm_charge_rate:
        messages.append(
            f"❌ Selected generator is {pm_gen_kw_cap:.1f} kW, which is LESS than the "
            f"Power Module charge rate ({pm_charge_rate:.1f} kW). Select a larger generator to continue."
        )
        can_continue = False
    # Efficiency warning if > 2/3 of PM charge rate (your rule)
    elif pm_gen_kw_cap > (pm_charge_rate * (2/3)):
        messages.append(
            f"⚠️ Selected generator is {pm_gen_kw_cap:.1f} kW, which is more than 2/3 of the "
            f"Power Module charge rate ({pm_charge_rate:.1f} kW). You may not see optimal fuel efficiency."
        )

    return can_continue, messages


def enforce_session_validation():
    """
    Ensures user_inputs exists, computes charge_rate, and (if PM) validates generator.
    Will block page rendering (st.stop) when PM generator is undersized.
    """
    ui = st.session_state.user_inputs

    model = ui.get("model")
    eboss_type = ui.get("eboss_type") or "Full Hybrid"
    pm_gen = ui.get("pm_gen")

    # Store charge rate back into session (used everywhere else)
    ui["charge_rate"] = calculate_charge_rate(model, eboss_type, pm_gen)

    # PM validation rules (do NOT change rate, just gate + warn)
    if eboss_type == "Power Module":
        if not pm_gen:
            st.error("❌ Please select a PM Generator size to continue.")
            st.stop()
        can_continue, msgs = validate_pm_generator(model, pm_gen)
        for msg in msgs:
            # show warning vs error
            (st.warning if msg.startswith("⚠️") else st.error)(msg)
        if not can_continue:
            st.stop()

# No-op backends so buttons won't crash in Cloud
def submit_demo_request(_): return 200
def submit_training_request(_): return 200

# ===============================================================================================

def landing_page():
    apply_custom_css()
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
    st.markdown(f'<h3 class="form-section-title">📝 Request { "a Demo" if form_type == "demo" else "On Site Training" }</h3>', unsafe_allow_html=True)

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
        if st.button("🚀 Launch EBOSS® Tool", key="btn_launch"):
            st.session_state.selected_form = "tool"
            st.session_state.section = "input"
            st.session_state.landing_shown = False
            st.rerun()
     
    st.stop()

if st.session_state.show_contact_form:
    render_contact_form(form_type=st.session_state.form_type)

#=============================================================================================================================
 # ──────────────────────────────────────────────────────────────
# 🔋 CHARGE RATE ENGINE
# ──────────────────────────────────────────────────────────────



def validate_charge_rate(model: str,
                         eboss_type: str,
                         entered_rate: float,
                         gen_kw: float | None = None) -> tuple[bool, list[str]]:
    """
    Validate an entered charge rate against the envelope, and (for PM) validate the generator.
    Rules:
      - entered_rate must not exceed max_charge (hard fail)
      - PM: if gen_kw provided:
          * FAIL if gen_kw < power_module
          * WARN if gen_kw > (2/3) * power_module  (may reduce fuel efficiency)
    """
    messages: list[str] = []
    if model not in EBOSS_KVA:
        return False, [f"❌ Unknown model: {model}"]

    kva = EBOSS_KVA[model]
    spec = Eboss_Specs[kva]
    max_rate = float(spec["max_charge"])
    pm_rate  = float(spec["power_module"])

    is_valid = True

    # cap check for any mode
    if float(entered_rate) > max_rate:
        messages.append(f"❌ Charge rate ({entered_rate:.1f} kW) exceeds model max ({max_rate:.1f} kW).")
        is_valid = False

    # PM generator checks (gen_kw optional; only applies in PM mode)
    if eboss_type == "Power Module" and gen_kw is not None:
        gen_kw = float(gen_kw)

        # Hard fail if undersized versus PM charge rate
        if gen_kw < pm_rate:
            messages.append(
                f"❌ Selected generator ({gen_kw:.1f} kW) is smaller than the Power Module charge rate "
                f"({pm_rate:.1f} kW). Select a larger generator to continue."
            )
            is_valid = False
        # Efficiency warning if sized above 2/3 of PM charge rate (per your rule)
        elif gen_kw > (pm_rate * (2/3)):
            messages.append(
                f"⚠️ Selected generator ({gen_kw:.1f} kW) is more than 2/3 of the Power Module charge rate "
                f"({pm_rate:.1f} kW). You may not see optimal fuel efficiency."
            )

    return is_valid, messages

def render_user_input_form():
    with st.container():
        cols = st.columns([1, 1, 1], gap="large")

        # ───── Column 1: EBOSS® ─────
        with cols[0]:
            st.markdown('''
                <div class="card">
                    <div class="card-label">EBOSS®</div>
            ''', unsafe_allow_html=True)

            st.session_state.user_inputs["model"] = st.selectbox(
                "Model", list(EBOSS_KVA.keys()), key="model_select"
            )

            st.session_state.user_inputs["eboss_type"] = st.selectbox(
                "Type", ["Full Hybrid", "Power Module"], key="eboss_type_select"
            )

            if st.session_state.user_inputs["eboss_type"] == "Power Module":
                st.session_state.user_inputs["pm_gen"] = st.selectbox(
                    "Generator Size", ["25kVA", "45kVA", "65kVA", "125kVA", "220kVA", "400kVA"],
                    key="pm_gen_select"
                )

            st.markdown('</div>', unsafe_allow_html=True)

        # ───── Column 2: Load ─────
        with cols[1]:
            st.markdown('''
                <div class="card">
                    <div class="card-label">Load</div>
            ''', unsafe_allow_html=True)

            st.session_state.user_inputs["raw_cont_load"] = st.number_input(
                "Continuous Load", 0, 500, step=1, format="%d", key="cont_input"
            )

            st.session_state.user_inputs["raw_peak_load"] = st.number_input(
                "Max Peak Load", 0, 500, step=1, format="%d", key="peak_input"
            )

            st.markdown('</div>', unsafe_allow_html=True)

        # ───── Column 3: Units ─────
        with cols[2]:
            st.markdown('''
                <div class="card">
                    <div class="card-label">Units</div>
            ''', unsafe_allow_html=True)

            st.session_state.user_inputs["load_units"] = st.selectbox(
                "Units", ["kW", "Amps"], key="unit_select"
            )

            st.session_state.user_inputs["voltage"] = st.selectbox(
                "Voltage", ["480V", "240V", "208V"], key="voltage_select"
            )

            st.markdown('</div>', unsafe_allow_html=True)

    # ───── KW Conversion Logic ─────
    pf = 0.8
    v_val = int(st.session_state.user_inputs["voltage"].replace("V", ""))
    cont = st.session_state.user_inputs["raw_cont_load"]
    peak = st.session_state.user_inputs["raw_peak_load"]

    if st.session_state.user_inputs["load_units"] == "Amps":
        st.session_state.user_inputs["cont_kw"] = (cont * (3 ** 0.5) * v_val * pf) / 1000
        st.session_state.user_inputs["peak_kw"] = (peak * (3 ** 0.5) * v_val * pf) / 1000
    else:
        st.session_state.user_inputs["cont_kw"] = cont
        st.session_state.user_inputs["peak_kw"] = peak



   
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
    eboss_type = user_inputs.get("eboss_type")
    cont_kw = user_inputs.get("cont_kw")

    if not model or model not in EBOSS_KVA or model not in EBOSS_BATTERY_KWH:
        st.warning("⚠️ Invalid model selected or missing data.")
        return

    pm_kva = EBOSS_KVA[model]
    battery_kwh = EBOSS_BATTERY_KWH[model]

    try:
        charge_rate = Eboss_Charge_Rates[pm_kva]["power_module" if eboss_type == "Power Module" else "full_hybrid"]
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
            new_rate = Eboss_Charge_Rates[kva]["power_module" if eboss_type == "Power Module" else "full_hybrid"]
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
                "eboss_type": "Full Hybrid",
                "pm_gen": None,
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
def render_card(label, value):
    st.markdown(f'''
        <div class="card">
            <div class="card-label">{label}</div>
            <div class="card-value">{value}</div>
        </div>
    ''', unsafe_allow_html=True)

def calculate_runtime_specs(model, eboss_type, cont_kw, pm_gen):
    # Determine generator size based on mode
    gen_kva = EBOSS_KVA.get(model, 0) if eboss_type == "Full Hybrid" else int(__import__("re").search(r"(\d+)", str(pm_gen or "")).group(1)) if pm_gen else 0
    gen_kw = gen_kva * 0.8

    # Use the unified envelope for charge/battery
    model_kva = EBOSS_KVA.get(model, gen_kva)
    charge_kw = calculate_charge_rate(model, eboss_type, pm_gen)
    battery_kwh = Eboss_Specs[model_kva]["battery_kwh"]  # ← unified & correct

    battery_life = battery_kwh / cont_kw if cont_kw else 0
    charge_time  = battery_kwh / charge_kw if charge_kw else 0
    cycles_per_day = 24 / (battery_life + charge_time) if (battery_life + charge_time) > 0 else 0
    total_runtime  = charge_time * cycles_per_day
    engine_pct     = charge_kw / gen_kw if gen_kw else 0
    fuel_gph       = interpolate_gph(int(gen_kva), max(0.25, min(engine_pct, 1.0))) if gen_kva else 0.0

    return {
        "battery_kwh": battery_kwh,
        "charge_time": charge_time,
        "battery_life": battery_life,
        "runtime": total_runtime,
        "engine_pct": engine_pct,
        "fuel_gph": fuel_gph
    }

# ---- TECH SPECS PAGE ----
def render_user_input_page():
    apply_custom_css()  # ✅ ADD THIS
    show_logo_and_title("Eboss & Load Data")
    top_navbar()
    render_user_input_form()

def render_tech_specs_page():
    apply_custom_css()
    show_logo_and_title("Tech Specs")
    top_navbar()

    # model selected elsewhere; fall back to first available
    model = st.session_state.get("model_select")
    if not model:
        model = next(iter(spec_data.keys()))

    # handle inconsistent key for 125 kVA
    if model not in spec_data and model.replace(" 125 kVA", "125 kVA") in spec_data:
        model = model.replace(" 125 kVA", "125 kVA")

    specs = spec_data.get(model)
    if not specs:
        st.warning(f"No data available for {model}")
        return

    # Render each section as: one full-width header card, followed by rows of (spec card | value card)
    for section, items in specs.items():
        st.markdown(f"""
        <div class="card" style="background-color:#636569;color:white;font-weight:700;
             font-size:1.2rem;padding:0.8rem 1.5rem;border-radius:12px;margin:2rem 0 1rem 0;
             text-align:center;text-transform:uppercase;box-shadow:0 4px 8px rgba(0,0,0,0.3);">
            {section}
        </div>
        """, unsafe_allow_html=True)

        for label, value in items:
            render_spec_value_row(label, value)


def render_compare_page():
    import re
    apply_custom_css()
    show_logo_and_title("Compare — EBOSS® vs Standard Generator")
    top_navbar()

    # Selected EBOSS model
    model = st.session_state.get("model_select")

    # Normalize odd key for 125
    if model not in spec_data and model.replace(" 125 kVA", "125 kVA") in spec_data:
        model = model.replace(" 125 kVA", "125 kVA")

    eboss_specs = spec_data.get(model, {})
    # If you have a dict of std-gen specs keyed similarly; otherwise leave it empty
    std_specs = globals().get("std_gen_data", {}).get(model, {})

    cont_kw = float(st.session_state.user_inputs.get("cont_kw", 10))

    # Extract kVA and simple performance envelope
    m = re.search(r"(\d+)", model)
    kva = int(m.group(1)) if m else 25
    gen_kw = kva * 0.8

    # Charge rate and battery (adjust with your real tables)
    charge_kw = Eboss_Specs[kva]["full_hybrid"]
    battery_kwh = Eboss_Specs[kva]["battery_kwh"]

    # Duty-cycle estimates
    batt_runtime_h = battery_kwh / cont_kw if cont_kw > 0 else 0
    charge_time_h = battery_kwh / charge_kw if charge_kw > 0 else 0
    cycles_per_day = 24 / (batt_runtime_h + charge_time_h) if (batt_runtime_h + charge_time_h) > 0 else 0
    runtime_hrs = charge_time_h * cycles_per_day

    # Fuel estimates (EBOSS runs only during charge; Std Gen runs 24h @ ~100%)
    eboss_gph = interpolate_gph(kva, min(max(charge_kw / gen_kw, 0.25), 1.0))
    std_gph   = interpolate_gph(kva, 1.0)

    eboss_gpd = round(eboss_gph * runtime_hrs, 2)
    std_gpd   = round(std_gph * 24.0, 2)
    eboss_gpw, std_gpw = round(eboss_gpd * 7, 2), round(std_gpd * 7, 2)
    eboss_gpm, std_gpm = round(eboss_gpd * 30, 2), round(std_gpd * 30, 2)

    # ---- Sections ----
    sections = {
        "Maximum Intermittent Load": eboss_specs.get("Maximum Intermittent Load", []),
        "Maximum Continuous Load":   eboss_specs.get("Maximum Continuous Load",   []),
    }

    # Render tech sections (for each metric show EBOSS vs Std Gen as a two-card row)
    for section, rows in sections.items():
        st.markdown(f"""
        <div class="card" style="background-color:#636569;color:white;font-weight:700;
             font-size:1.2rem;padding:0.8rem 1.5rem;border-radius:12px;margin:2rem 0 1rem 0;
             text-align:center;text-transform:uppercase;box-shadow:0 4px 8px rgba(0,0,0,0.3);">
            {section}
        </div>
        """, unsafe_allow_html=True)

        std_sec = dict(std_specs.get(section, []))

        for label, eboss_val in rows:
            # little header row for the metric label
            st.markdown(f"""
            <div class="card" style="background-color:#47484b;color:#fff;font-weight:700;
                 font-size:1.0rem;padding:0.5rem 1rem;border-radius:10px;margin:0.2rem 0 0.4rem 0;">
                {label}
            </div>
            """, unsafe_allow_html=True)
            # then the two cards: EBOSS vs Std Gen
            col1, col2 = st.columns(2, gap="large")
            with col1:
                st.markdown(f"""
                    <div class="card">
                        <div class="card-label">EBOSS®</div>
                        <div class="card-value">{eboss_val}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class="card">
                        <div class="card-label">Standard Gen</div>
                        <div class="card-value">{std_sec.get(label, "–")}</div>
                    </div>
                """, unsafe_allow_html=True)

    # Engine / fuel comparison section
    st.markdown("""
    <div class="card" style="background-color:#636569;color:white;font-weight:700;
         font-size:1.2rem;padding:0.8rem 1.5rem;border-radius:12px;margin:2rem 0 1rem 0;
         text-align:center;text-transform:uppercase;box-shadow:0 4px 8px rgba(0,0,0,0.3);">
        Engine Specs & Fuel Use
    </div>
    """, unsafe_allow_html=True)

    metrics = [
        ("Runtime Hrs per Day", f"{runtime_hrs:.1f} h", "24 h"),
        ("Battery Storage",     f"{battery_kwh} kWh",  "0 kWh"),
        ("Gallons per Day",     f"{eboss_gpd} gal",    f"{std_gpd} gal"),
        ("Gallons per Week",    f"{eboss_gpw} gal",    f"{std_gpw} gal"),
        ("Gallons per Month",   f"{eboss_gpm} gal",    f"{std_gpm} gal"),
    ]
    for label, eb_val, st_val in metrics:
        # metric label header
        st.markdown(f"""
        <div class="card" style="background-color:#47484b;color:#fff;font-weight:700;
             font-size:1.0rem;padding:0.5rem 1rem;border-radius:10px;margin:0.2rem 0 0.4rem 0;">
            {label}
        </div>
        """, unsafe_allow_html=True)
        # EBOSS vs Std Gen as two cards
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown(f"""
                <div class="card">
                    <div class="card-label">EBOSS®</div>
                    <div class="card-value">{eb_val}</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="card">
                    <div class="card-label">Standard Gen</div>
                    <div class="card-value">{st_val}</div>
                </div>
            """, unsafe_allow_html=True)

    
def render_spec_value_row(spec_label: str, spec_value: str):
    """Render a row with two separate cards: left for spec, right for value."""
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown(f'''
            <div class="card">
                <div class="card-label">{spec_label}</div>
            </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
            <div class="card">
                <div class="card-value">{spec_value}</div>
            </div>
        ''', unsafe_allow_html=True)
        
def render_spec_value_row_2(left_label: str, left_value: str, right_label: str, right_value: str):
    """Two cards in the row (used in headers that have two sides occasionally)."""
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown(f"""
            <div class="card">
                <div class="card-label">{left_label}</div>
                <div class="card-value">{left_value}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="card">
                <div class="card-label">{right_label}</div>
                <div class="card-value">{right_value}</div>
            </div>
        """, unsafe_allow_html=True)

def render_spec_value_row_4(spec_label: str, eboss_val: str, std_val: str, diff_val: str | None = None):
    """Four cards in one row: Spec | EBOSS | Std Gen | Difference (if numeric)."""
    c1, c2, c3, c4 = st.columns(4, gap="large")

    # auto-compute pretty delta unless caller supplies one
    diff_html = _delta_badge(eboss_val, std_val) if diff_val is None else _delta_badge(diff_val, "0")

    with c1:
        st.markdown(f"""
            <div class="card">
                <div class="card-label">{spec_label}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="card">
                <div class="card-label">EBOSS®</div>
                <div class="card-value">{eboss_val}</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="card">
                <div class="card-label">Standard Gen</div>
                <div class="card-value">{std_val}</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
            <div class="card">
                <div class="card-label">Difference</div>
                <div class="card-value">{diff_html}</div>
            </div>
        """, unsafe_allow_html=True)


def _num(x):
    """Extract first float from a string like '70 A / 20.2 kW' -> 70.0 (prefers kW if present)."""
    if x is None: return None
    s = str(x)
    # prefer a value labeled 'kW' if present
    m_kw = re.search(r"([0-9]*\.?[0-9]+)\s*kW", s, flags=re.I)
    if m_kw:
        return float(m_kw.group(1))
    m = re.search(r"([0-9]*\.?[0-9]+)", s)
    return float(m.group(1)) if m else None

def _delta(a, b):
    """Return a-b if both numeric else None."""
    try:
        fa, fb = _num(a), _num(b)
        if fa is None or fb is None:
            return None
        d = fa - fb
        return f"{d:+.2f}"
    except Exception:
        return None

# ---- LOAD SPECS PAGE ----
def render_load_specs_page():
    apply_custom_css()
    show_logo_and_title("Load Based Specs")
    top_navbar()

    # 👉 Render form UI
    render_user_input_form()

    # 👉 Validate inputs
    enforce_session_validation()
    inputs = st.session_state.user_inputs
    kva = EBOSS_KVA[inputs["model"]]
    spec = Eboss_Specs[kva]

    charge_rate = inputs["charge_rate"]
    battery_kwh = spec["battery_kwh"]
    cont_kw = inputs["cont_kw"]
    peak_kw = inputs["peak_kw"]
    max_safe_limit = spec["max_charge"] * 0.9
    efficiency_target = battery_kwh * (2 / 3)

    # ---- Threshold Check ----
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🔒 Load Threshold Check")
    if cont_kw > spec["max_charge"]:
        st.error(f"❌ Load ({cont_kw:.1f} kW) exceeds max charge rate ({spec['max_charge']} kW).")
    elif cont_kw > max_safe_limit:
        st.warning(f"⚠️ Load is above 90% of the charge rate ({max_safe_limit:.1f} kW).")
    elif cont_kw > efficiency_target:
        st.info(f"ℹ️ Load is within safe range but above the fuel-efficiency threshold (~{efficiency_target:.1f} kW).")
    else:
        st.success(f"✅ Load is optimal for fuel efficiency (≤ {efficiency_target:.1f} kW).")
    if peak_kw > spec["max_peak"]:
        st.error(f"❌ Peak load ({peak_kw:.1f} kW) exceeds EBOSS peak limit ({spec['max_peak']} kW).")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Calculations ----
    gen_kw = kva * 0.8
    batt_runtime_h = battery_kwh / cont_kw if cont_kw > 0 else 0
    charge_time_h = battery_kwh / charge_rate if charge_rate > 0 else 0
    cycles_per_day = 24 / (batt_runtime_h + charge_time_h) if (batt_runtime_h + charge_time_h) > 0 else 0
    engine_runtime_day = charge_time_h * cycles_per_day
    engine_load_pct = max(0.25, min(charge_rate / gen_kw, 1.0))
    fuel_gph = interpolate_gph(kva, engine_load_pct)
    fuel_day = fuel_gph * engine_runtime_day
    fuel_week = fuel_day * 7
    fuel_month = fuel_day * 30
    co2_day_lbs = fuel_day * 22.4


      # ---- Battery & Charging ----
    st.markdown("""
    <div class="card" style="background-color:#636569;color:#fff;font-weight:700;
         font-size:1.1rem;padding:0.6rem 1.2rem;border-radius:12px;margin:1rem 0 0.8rem 0;
         text-align:center;text-transform:uppercase;box-shadow:0 4px 8px rgba(0,0,0,0.3);">
        Battery & Charging
    </div>
    """, unsafe_allow_html=True)
    render_spec_value_row("EBOSS® Model", inputs["model"])
    render_spec_value_row("Battery Capacity", f"{battery_kwh} kWh")
    render_spec_value_row("Selected Charge Rate", f"{charge_rate:.1f} kW")
    render_spec_value_row("Battery-only Runtime", f"{batt_runtime_h:.2f} h @ {cont_kw:.1f} kW")
    render_spec_value_row("Charge Time", f"{charge_time_h:.2f} h")
    render_spec_value_row("Cycles per Day", f"{cycles_per_day:.2f}")

    # ---- Engine & Fuel ----
    st.markdown("""
    <div class="card" style="background-color:#636569;color:#fff;font-weight:700;
         font-size:1.1rem;padding:0.6rem 1.2rem;border-radius:12px;margin:1rem 0 0.8rem 0;
         text-align:center;text-transform:uppercase;box-shadow:0 4px 8px rgba(0,0,0,0.3);">
        Engine & Fuel
    </div>
    """, unsafe_allow_html=True)
    render_spec_value_row("Generator Nameplate", f"{kva} kVA / {gen_kw:.0f} kW")
    render_spec_value_row("Engine Load (approx.)", f"{engine_load_pct*100:.0f}%")
    render_spec_value_row("Engine Runtime / Day", f"{engine_runtime_day:.2f} h")
    render_spec_value_row("Fuel Burn (gph)", f"{fuel_gph:.2f} gal/h")
    render_spec_value_row("Fuel / Day", f"{fuel_day:.2f} gal")
    render_spec_value_row("Fuel / Week", f"{fuel_week:.2f} gal")
    render_spec_value_row("Fuel / Month", f"{fuel_month:.2f} gal")
    render_spec_value_row("CO₂ / Day", f"{co2_day_lbs:.0f} lbs")

    # ---- Nameplate & Limits ----
    st.markdown("""
    <div class="card" style="background-color:#636569;color:#fff;font-weight:700;
         font-size:1.1rem;padding:0.6rem 1.2rem;border-radius:12px;margin:1.4rem 0 0.8rem 0;
         text-align:center;text-transform:uppercase;box-shadow:0 4px 8px rgba(0,0,0,0.3);">
        Nameplate & Limits
    </div>
    """, unsafe_allow_html=True)
    render_spec_value_row("Continuous Load", f"{cont_kw:.1f} kW")
    render_spec_value_row("Peak Load", f"{peak_kw:.1f} kW")
    render_spec_value_row("Max Charge Rate", f"{spec['max_charge']:.1f} kW")
    render_spec_value_row("Max Peak (EBOSS®)", f"{spec['max_peak']:.1f} kW")




def render_compare_page():
    import re
    apply_custom_css()
    show_logo_and_title("Compare — EBOSS® vs Standard Generator")
    top_navbar()

    # Load the diesel reference once (cached)
    STD_REF = load_std_gen_specs_from_excel("/mnt/data/Grn Compare.xlsx")

    # Selected EBOSS model (normalize the 125 key if needed)
    model = st.session_state.get("model_select")
    if model not in spec_data and model.replace(" 125 kVA", "125 kVA") in spec_data:
        model = model.replace(" 125 kVA", "125 kVA")

    eboss_specs = spec_data.get(model, {})

    # Determine kVA and map to Excel block
    m = re.search(r"(\d+)", model)
    kva_key = m.group(1) if m else "25"
    std_specs = STD_REF.get(kva_key, {})  # empty dict if not found

    # ---- Optional: show which std-gen bucket we matched
    st.markdown(f"""
    <div class="card" style="background-color:#636569;color:white;font-weight:700;
         font-size:1.0rem;padding:0.6rem 1rem;border-radius:12px;margin:0.5rem 0 1rem 0;">
        Matched Standard Generator: <span style="font-weight:900;">{kva_key} kVA class</span>
    </div>
    """, unsafe_allow_html=True)

    # ---------- SECTION 1: Maximum Intermittent ----------
    st.markdown("""
    <div class="card" style="background-color:#636569;color:white;font-weight:700;
         font-size:1.2rem;padding:0.8rem 1.5rem;border-radius:12px;margin:1.2rem 0 0.6rem 0;
         text-align:center;text-transform:uppercase;box-shadow:0 4px 8px rgba(0,0,0,0.3);">
        Maximum Intermittent Load
    </div>
    """, unsafe_allow_html=True)
    e_rows = eboss_specs.get("Maximum Intermittent Load", [])
    s_rows = dict(std_specs.get("Maximum Intermittent Load", []))
    for label, e_val in e_rows:
        s_val = s_rows.get(label, "–")
        render_spec_value_row_4(label, e_val, s_val, _delta(e_val, s_val))

    # ---------- SECTION 2: Maximum Continuous ----------
    st.markdown("""
    <div class="card" style="background-color:#636569;color:white;font-weight:700;
         font-size:1.2rem;padding:0.8rem 1.5rem;border-radius:12px;margin:1.2rem 0 0.6rem 0;
         text-align:center;text-transform:uppercase;box-shadow:0 4px 8px rgba(0,0,0,0.3);">
        Maximum Continuous Load
    </div>
    """, unsafe_allow_html=True)
    e_rows = eboss_specs.get("Maximum Continuous Load", [])
    s_rows = dict(std_specs.get("Maximum Continuous Load", []))
    for label, e_val in e_rows:
        s_val = s_rows.get(label, "–")
        render_spec_value_row_4(label, e_val, s_val, _delta(e_val, s_val))

    # ---------- SECTION 3: Engine / Fuel (computed + Excel) ----------
    # Compute EBOSS duty-cycle metrics from your envelopes (same method you used before)
    inputs = st.session_state.user_inputs
    cont_kw = float(inputs.get("cont_kw", 10))
    kva = int(kva_key)
    gen_kw = kva * 0.8
    charge_kw   = Eboss_Specs[kva]["full_hybrid"]
    battery_kwh = Eboss_Specs[kva]["battery_kwh"]

    batt_runtime_h  = battery_kwh / cont_kw if cont_kw > 0 else 0
    charge_time_h   = battery_kwh / charge_kw if charge_kw > 0 else 0
    cycles_per_day  = 24 / (batt_runtime_h + charge_time_h) if (batt_runtime_h + charge_time_h) > 0 else 0
    runtime_hrs     = charge_time_h * cycles_per_day

    eboss_gph = interpolate_gph(kva, min(max(charge_kw / gen_kw, 0.25), 1.0))
    std_gph   = interpolate_gph(kva, 1.0)

    eboss_gpd = round(eboss_gph * runtime_hrs, 2)
    std_gpd   = round(std_gph * 24.0, 2)
    eboss_gpw, std_gpw = round(eboss_gpd * 7, 2), round(std_gpd * 7, 2)
    eboss_gpm, std_gpm = round(eboss_gpd * 30, 2), round(std_gpd * 30, 2)

    st.markdown("""
    <div class="card" style="background-color:#636569;color:white;font-weight:700;
         font-size:1.2rem;padding:0.8rem 1.5rem;border-radius:12px;margin:1.2rem 0 0.6rem 0;
         text-align:center;text-transform:uppercase;box-shadow:0 4px 8px rgba(0,0,0,0.3);">
        Engine Specs & Fuel Use
    </div>
    """, unsafe_allow_html=True)

    engine_rows = [
        ("Runtime Hrs per Day", f"{runtime_hrs:.1f} h", "24 h"),
        ("Battery Storage",     f"{battery_kwh} kWh",  "0 kWh"),
        ("Gallons per Day",     f"{eboss_gpd} gal",    f"{std_gpd} gal"),
        ("Gallons per Week",    f"{eboss_gpw} gal",    f"{std_gpw} gal"),
        ("Gallons per Month",   f"{eboss_gpm} gal",    f"{std_gpm} gal"),
    ]
    for label, e_val, s_val in engine_rows:
        render_spec_value_row_4(label, e_val, s_val, _delta(e_val, s_val))


# ---- COST ANALYSIS PAGE ----
def render_cost_analysis_page():
    from math import ceil
    from datetime import date

    show_logo_and_title("Cost Analysis")
    top_navbar()

    inputs = st.session_state.user_inputs
    model = inputs.get("model")
    eboss_type = inputs.get("eboss_type")
    cont_kw = inputs.get("cont_kw")
    pm_gen = inputs.get("pm_gen")

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
        runtime = calculate_runtime_specs(model, eboss_type, cont_kw, pm_gen)
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

def render_parallel_calculator_page():
    apply_custom_css()
    show_logo_and_title("Parallel Sizing Tool")
    top_navbar()

    # ----------------------------------
    # User Input
    cont_kw = st.number_input("Required Continuous Load (kW)", min_value=0.0, step=0.1)
    peak_kw = st.number_input("Required Peak Load (kW)", min_value=0.0, step=0.1)
    sizing_mode = st.radio("Sizing Strategy", ["No Efficiency Preference", "Max Fuel Efficiency"])
    view_mode = st.selectbox("View Output As", ["Equipment Only", "Comparison EBOSS vs Gen-Only"])

    if st.button("Calculate"):
        results = calculate_parallel_sizing(cont_kw, peak_kw, sizing_mode)

        # ----------------------------------
        # Render Equipment Table
        st.subheader("Equipment Requirement")
        for section, rec in results.items():
            st.markdown(f"### {section}")
            cols = st.columns([1,1,1,1,1])
            headers = ["Scenario","EBOSS QTY","Generator QTY","Charge kW","Fuel (gal/day)"]
            for c, h in zip(cols, headers): c.markdown(f"**{h}**")
            for rec_item in rec:
                scenario, units, gens, charge, fuel = rec_item.values()
                row = [scenario, units, gens, f"{charge:.1f}", f"{fuel:.2f}"]
                for c, val in zip(cols, row): c.markdown(val)

        # ----------------------------------
        # Render Comparison if requested
        if view_mode == "Comparison EBOSS vs Gen-Only":
            st.subheader("Fuel Comparison")
            # display side-by-side fuel totals

        st.markdown("---")

# ─────────────────────────────────────────────────────────────────
def render_parallel_calculator_page():
    apply_custom_css()
    show_logo_and_title("Parallel Sizing Tool")
    top_navbar()

    # ───────────── Inputs ─────────────
    cont_kw = st.number_input("Required Continuous Load (kW)", min_value=0.0, step=0.1)
    peak_kw = st.number_input("Required Peak Load (kW)", min_value=0.0, step=0.1)
    sizing_mode = st.radio("Sizing Strategy:", ["No Efficiency Preference", "Max Fuel Efficiency"], horizontal=True)
    view_mode = st.selectbox("View Output As:", ["Equipment Only", "Comparison: EBOSS vs Generator-Only"])

    if st.button("🔢 Calculate"):
        results = calculate_parallel_sizing(cont_kw, peak_kw, sizing_mode)

        render_parallel_results(results, view_mode)

        # ────────── Print Friendly Button ──────────
        today = date.today().strftime("%B %d, %Y")
        st.markdown(f'''
            <div class="print-logo" style="text-align:center; margin-top:2rem;">
              <img src="https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/logo.png" width="240"><br><br>
              <div style="font-size:1.3rem; font-weight:bold;">EBOSS® Parallel Sizing Report</div>
              <div style="font-size:0.9rem;">{today}</div>
            </div>
            <button class="eboss-hero-btn" onclick="window.print()" style="margin:2rem auto; display:block;">
                🖨️ Print Report
            </button>
            <style>
            @media print {{
                body * {{ visibility: hidden; }}
                .print-logo, .print-logo *, .stContainer, .stMarkdown {{ visibility: visible; }}
                .stApp, .stButton, .topNavBar {{ display: none !important; }}
                .stContainer {{ background: white !important; color: black !important; box-shadow: none !important; }}
            }}
            </style>
        ''', unsafe_allow_html=True)

from itertools import combinations_with_replacement
def calculate_parallel_sizing(required_cont_kw, required_peak_kw, sizing_mode):
    """
    Determines EBOSS and generator sizing options based on required load and strategy.
    
    Returns:
        dict: {
            "Full Hybrid Only": [...],
            "Power Module + Gen Support": [...],
            "Gen Only": [...]
        }
    """
    results = {
        "Full Hybrid Only": [],
        "Power Module + Gen Support": [],
        "Gen Only": []
    }
    # Helper: generator fuel rate by kW
    gen_fuel_gph = {25: 2.0, 45: 3.5, 65: 5.0, 125: 8.5, 220: 14.0}  # replace with real data

    # 1. Full Hybrid scenarios
    for kva, spec in Eboss_Specs.items():
        charge_rate = spec["full_hybrid"]
        units_needed = -(-required_cont_kw // charge_rate)  # ceiling division
        total_charge = units_needed * charge_rate
        est_fuel = units_needed * (charge_rate * 0.015)  # eboss fuel formula
        results["Full Hybrid Only"].append({
            "scenario": f"EBOSS {kva} kVA Only",
            "units": int(units_needed),
            "gens": 0,
            "charge": total_charge,
            "fuel": est_fuel
        })

    # Mixed-model full hybrid combos
    all_kvas = list(Eboss_Specs.keys())
    combos = list(combinations_with_replacement(all_kvas, 2))  # pairs
    mixed = []
    for combo in combos:
        charge = sum(Eboss_Specs[k]["full_hybrid"] for k in combo)
        if charge >= required_cont_kw:
            total_fuel = sum(c * (charge * 0.005) for c, k in zip([1,1], combo))
            mixed.append((combo, charge, total_fuel))
    mixed = sorted(mixed, key=lambda x: (len(x[0]), x[2]))[:2]
    for idx, item in enumerate(mixed, 1):
        kva_list, charge, fuel = item
        results["Full Hybrid Only"].append({
            "scenario": f"Mixed Option {idx}: " + " + ".join(f"{k} kVA" for k in kva_list),
            "units": len(kva_list),
            "gens": 0,
            "charge": charge,
            "fuel": fuel
        })

    # 2. Power Module + Gen Support
    for kva, spec in Eboss_Specs.items():
        charge_rate = spec["power_module"]
        units_needed = -(-required_cont_kw // charge_rate)
        total_charge = units_needed * charge_rate
        gen_needed = -(-total_charge // spec["max_charge"])
        # assume smallest generator kvas available
        gens = gen_needed
        total_fuel = gens * gen_fuel_gph.get(kva, 5.0) * 24
        results["Power Module + Gen Support"].append({
            "scenario": f"PM {kva} kVA Only",
            "units": int(units_needed),
            "gens": gens,
            "charge": total_charge,
            "fuel": total_fuel
        })

    # Mixed PM combos
    pm_mixed = []
    for combo in combos:
        charge = sum(Eboss_Specs[k]["power_module"] for k in combo)
        if charge >= required_cont_kw:
            gens = -(-charge // max(Eboss_Specs[k]["max_charge"] for k in combo))
            fuel = gens * gen_fuel_gph.get(combo[0], 5.0) * 24
            pm_mixed.append((combo, charge, fuel))
    pm_mixed = sorted(pm_mixed, key=lambda x: (len(x[0]), x[2]))[:2]
    for idx, item in enumerate(pm_mixed, 1):
        combo, charge, fuel = item
        gens = -(-charge // max(Eboss_Specs[k]["max_charge"] for k in combo))
        results["Power Module + Gen Support"].append({
            "scenario": f"PM Mixed Option {idx}: " + " + ".join(f"{k} kVA" for k in combo),
            "units": len(combo),
            "gens": gens,
            "charge": charge,
            "fuel": fuel
        })

    # 3. Generator only
    for kva in gen_fuel_gph.keys():
        gens_needed = -(-required_cont_kw // kva)
        fuel = gens_needed * gen_fuel_gph[kva] * 24
        results["Gen Only"].append({
            "scenario": f"Gen {kva} kVA Only",
            "units": 0,
            "gens": gens_needed,
            "charge": gens_needed * kva,
            "fuel": fuel
        })
    # Mixed gen combos
    gen_kvas = list(gen_fuel_gph.keys())
    gen_combos = list(combinations_with_replacement(gen_kvas, 2))
    mixed_gen = []
    for combo in gen_combos:
        charge = sum(combo)
        if charge >= required_cont_kw:
            fuel = sum(gen_fuel_gph[k] for k in combo) * 24
            mixed_gen.append((combo, charge, fuel))
    mixed_gen = sorted(mixed_gen, key=lambda x: (len(x[0]), x[2]))[:2]
    for idx, item in enumerate(mixed_gen, 1):
        combo, charge, fuel = item
        results["Gen Only"].append({
            "scenario": f"Gen Mixed Option {idx}: " + " + ".join(f"{k} kVA" for k in combo),
            "units": 0,
            "gens": len(combo),
            "charge": charge,
            "fuel": fuel
        })

    return results

  
from datetime import date

# ─────────────────────────────────────────────────────────────────
def render_parallel_results(results, view_mode="Equipment Only"):
    st.markdown("---")
    for category, items in results.items():
        st.markdown(f"## {category}")
        if not items:
            st.info("No valid configuration found.")
            continue

        headers = ["Plan", "EBOSS Units", "Generators", "Charge (kW)", "Fuel (gal/day)"]
        cols = st.columns([2,1,1,1.3,1])
        for col, h in zip(cols, headers):
            col.markdown(f"**{h}**")

        for item in items:
            row = [
                item["scenario"],
                str(item["units"]),
                str(item["gens"]),
                f"{item['charge']:.1f}",
                f"{item['fuel']:.2f}"
            ]
            for col, val in zip(cols, row):
                with col:
                    st.markdown(f'<div class="card-value">{val}</div>' if headers[cols.index(col)]!="Plan"
                                else f'<div class="card-label">{val}</div>', unsafe_allow_html=True)

    if "Comparison" in view_mode:
        st.markdown("### 🔍 Fuel Comparison Summary (gal/day)")
        totals = {k: sum(x["fuel"] for x in v) for k, v in results.items()}
        comp_cols = st.columns(3)
        names = ["Full Hybrid", "Hybrid + PM Support", "Generator Only"]
        for c, name in zip(comp_cols, names):
            c.markdown(f"**{name}**\n\nFuel: {totals.get(name+' Only', totals.get(name,0)):.2f}")

        st.markdown("---")

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




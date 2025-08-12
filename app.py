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

# Apply custom CSS for branding, layout centering, and components
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

    /* ===== Centering stack for all main elements ===== */
    .main-center-stack {{
        display: flex;
        flex-direction: column;
        align-items: center;      /* horizontal centering of all children */
        width: 100%;
        text-align: center;       /* center text inside children by default */
        margin: 0 auto;           /* center the stack if it gets a max-width */
        max-width: 960px;         /* keeps everything on one vertical axis */
        gap: 12px;                /* small space between stacked elements */
    }}

    .sidebar .sidebar-content {{
        background-color: {COLORS['Asphalt']};
        color: {COLORS['Alpine White']};
    }}

    /* Buttons (including link_button look) */
    button {{
        background-color: {COLORS['Energy Green']};
        color: {COLORS['Asphalt']};
        border: 1px solid {COLORS['Charcoal']};
        border-radius: 5px;
        padding: 10px 20px;
        transition: box-shadow 0.3s ease;
        width: 100%;
        margin: 5px 0;
    }}
    button:hover {{
        box-shadow: 0 0 10px {COLORS['Energy Green']};
    }}

    /* Inputs */
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

    .logo-container {{
        text-align: center;
        margin: 20px 0 8px 0;
    }}
    .logo {{
        max-width: 200px;
        display: inline-block;
    }}

    .message-text {{
        font-size: 1.5em;
        text-align: center;
        transition: box-shadow 0.3s ease;
        padding: 10px;
    }}
    .message-text:hover {{
        box-shadow: 0 0 10px {COLORS['Energy Green']};
    }}

    /* Three-button row stays centered as a group */
    .button-container {{
        display: flex;
        justify-content: center;
        gap: 10px;
        width: 100%;
        flex-wrap: wrap; /* responsive */
    }}
    .button-block {{
        flex: 1 1 220px;  /* responsive width */
        max-width: 300px;
        min-width: 220px;
    }}

    /* Radio group centered & evenly spaced */
    .centered-radio {{
        width: 100%;
        display: flex;
        justify-content: center;
    }}
    .centered-radio [role="radiogroup"] {{
        display: flex !important;
        justify-content: center !important;
        align-items: center;
        gap: 28px;
        flex-wrap: wrap;
        width: 100%;
    }}
    .centered-radio label {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 8px 12px;
        border: 1px solid {COLORS['Light Grey']};
        border-radius: 6px;
        min-width: 220px;
        text-align: center;
        background: rgba(0,0,0,0.25);
    }}

    /* Enter Data button centered via column trick */
    .centered-button {{
        width: 100%;
    }}

    /* Footer perfectly centered */
    .footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: {COLORS['Asphalt']};
        color: {COLORS['Alpine White']};
        padding: 10px 12px;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        z-index: 999;
    }}
    .footer-inner {{
        text-align: center;
        display: inline-flex;
        gap: 10px;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
        max-width: 100%;
    }}
    .footer-inner a {{
        color: {COLORS['Alpine White']};
        text-decoration: underline;
    }}

    /* Mobile tweaks */
    @media (max-width: 768px) {{
        .logo {{ max-width: 160px; }}
        .button-block {{ max-width: 100%; min-width: 180px; }}
        .centered-radio label {{ min-width: 160px; }}
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
    st.session_state.selected_option = None
if "recommended_model" not in st.session_state:
    st.session_state.recommended_model = ""
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ===== MAIN CENTER STACK (keeps everything on the s

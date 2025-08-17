import streamlit as st
import math
import logging
import pandas as pd
import numpy as np

st.markdown("""
<style>
/* ===== Hide Streamlit Header & Toolbar ===== */
[data-testid="stHeader"] {visibility: hidden; height: 0px;}
[data-testid="stToolbar"] {visibility: hidden; height: 0px;}
.block-container {padding-top: 0rem !important;}

/* ===== Hide Streamlit Footer / "Manage app" ===== */
footer {visibility: hidden;}
[data-testid="stFooter"] {visibility: hidden;}
div.viewerBadge_link,
div[data-testid="stDecoration"],
#MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
st.markdown(
        """
        <style>
        .stDeployButton {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

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

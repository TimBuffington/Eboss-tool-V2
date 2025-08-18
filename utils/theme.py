import streamlit as st

COLORS = {
    "Asphalt": "#000000",
    "Concrete": "#939598",
    "Charcoal": "#636569",
    "Alpine White": "#FFFFFF",
    "Energy Green": "#80BD47",
    "Light Grey": "#D3D3D3",
}

LOGO_URL = "https://raw.githubusercontent.com/TimBuffington/troubleshooting/refs/heads/main/assets/ANA-ENERGY-LOGO-HORIZONTAL-WHITE-GREEN.png"
BG_URL   = "https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/bg.png"

def apply_theme():
    st.markdown(f"""
    <style>
    /* Hide default chrome */
    [data-testid="stHeader"], [data-testid="stToolbar"], footer, [data-testid="stFooter"], #MainMenu {{
      visibility: hidden; height: 0 !important;
    }}
    .block-container {{ padding-top: 0 !important; }}

    /* Background & text */
    .stApp {{
      background-image: url("{BG_URL}"
      background-size: cover; background-position:center; background-repeat:no-repeat; background-attachment:fixed;
      color: {COLORS['Alpine White']}; font-family: Arial, sans-serif;
    }}

    /* Centered, responsive logo */
    .logo-wrap {{ display:flex; justify-content:center; align-items:center; margin:8px 0 16px; }}
    .logo-wrap img {{ width: clamp(220px, 55vw, 560px); height:auto; }}

    /* Link-as-button CTA */
    .cta-link, .cta-link:link, .cta-link:visited, .cta-link:active, .cta-link:hover {{
      color: {COLORS['Alpine White']} !important; text-decoration:none !important; -webkit-text-fill-color:{COLORS['Alpine White']} !important;
    }}
    .cta-link {{
      display:flex; align-items:center; justify-content:center; width:100%; min-height:56px; line-height:1.2;
      background:{COLORS['Asphalt']}; border:2px solid {COLORS['Concrete']};
      font:700 16px Arial, sans-serif; text-shadow:0 0 6px {COLORS['Energy Green']};
      border-radius:10px; padding:12px 14px; box-sizing:border-box; transition: box-shadow .25s, transform .15s;
    }}
    .cta-link:hover {{ box-shadow:0 0 28px {COLORS['Energy Green']}; transform: translateY(-1px); }}

    /* Make st.button rows match CTA look (scope with .cta-scope) */
    .cta-scope [data-testid="column"] .stButton {{ width:100% !important; }}
    .cta-scope .stButton > button {{
      display:block; width:100% !important; min-height:56px; line-height:1.2; box-sizing:border-box; text-align:center;
      background:{COLORS['Asphalt']} !important; color:{COLORS['Alpine White']} !important;
      border:2px solid {COLORS['Concrete']} !important;
      font:700 16px Arial, sans-serif; text-shadow:0 0 6px {COLORS['Energy Green']} !important;
      border-radius:10px; padding:12px 14px; transition: box-shadow .25s, transform .15s;
    }}
    .cta-scope .stButton > button:hover {{ box-shadow:0 0 28px {COLORS['Energy Green']}; transform: translateY(-1px); }}

    /* Inputs */
    .stTextInput input, .stNumberInput input, .stDateInput input, .stTimeInput input,
    [data-baseweb="select"] div {{
      background:{COLORS['Asphalt']}; color:{COLORS['Alpine White']};
      border:1px solid {COLORS['Light Grey']}; border-radius:6px; padding:8px; transition: box-shadow .2s;
    }}
    .stTextInput input:hover, .stNumberInput input:hover, [data-baseweb="select"] div:hover {{
      box-shadow:0 0 10px {COLORS['Energy Green']};
    }}

    /* Responsive */
    @media (max-width: 900px) {{
      .block-container {{ padding-left:.75rem; padding-right:.75rem; }}
      [data-testid="stHorizontalBlock"] {{ flex-direction:column !important; gap:.75rem !important; }}
      [data-testid="column"] {{ width:100% !important; flex:1 1 100% !important; }}
      .logo-wrap img {{ width: clamp(180px, 70vw, 520px); }}
    }}
    </style>
    """, unsafe_allow_html=True)

def render_logo():
    st.markdown(f"<div class='logo-wrap'><img src='{LOGO_URL}' alt='ANA Energy Logo' /></div>", unsafe_allow_html=True)
    
 render apply_theme() 




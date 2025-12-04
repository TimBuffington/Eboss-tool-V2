from pathlib import Path
import streamlit as st


def global_css():
    
    st.markdown("""
    <style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for color palette */
    :root {
        --black-asphalt;
        --cool-gray-;
        --cool-gray-;
        --charcoal;
        --alpine-white;
        --energy-green;
    }
    
    /* Hide Streamlit branding and white bar completely */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp > header {
        background-color: transparent;
        height: 0px;
    }
    .stApp {
        margin-top: -90px;
        padding-top: 0;
    }
    /* Force hide any remaining header elements */
    [data-testid="stHeader"] {
        display: none;
    }
    .stAppHeader {
        display: none;
    }
    /* Remove top padding from main block */
    .block-container {
        padding-top: 0rem;
    }
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, var(--black-asphalt) 0%, var(--charcoal) 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main-container {
        background: var(--alpine-white);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        border: 1px solid var(--cool-gray-8c);
    }
    
    /* Title styling */
    .main-title {
        color: var(--black-asphalt);
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .subtitle {
        color: var(--cool-gray-10c);
        font-size: 1.2rem;
        font-weight: 400;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Form container styling */
    .form-container {
        background: var(--charcoal);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .form-section-title {
        color: var(--alpine-white);
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }
    
    /* Input styling */
    .stSelectbox > div > div {
        background-color: var(--cool-gray-10c) !important;
        border: 2px solid var(--energy-green) !important;
        border-radius: 8px !important;
        color: var(--alpine-white) !important;
        font-family: Arial, sans-serif !important;
        font-weight: 500 !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.4), inset 0 2px 4px rgba(0,0,0,0.3) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--energy-green);
        box-shadow: 0 8px 16px rgba(129, 189, 71, 0.5), inset 0 2px 4px rgba(0,0,0,0.3) !important;
        transform: translateY(-1px);
    }
    
    .stSelectbox > div > div > div {
        color: var(--alpine-white) !important;
        font-family: Arial, sans-serif !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
    }
    
    .stNumberInput > div > div {
        background-color: var(--cool-gray-10c) !important;
        border: 2px solid var(--energy-green) !important;
        border-radius: 8px !important;
        color: var(--alpine-white) !important;
        font-family: Arial, sans-serif !important;
        font-weight: 500 !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.4), inset 0 2px 4px rgba(0,0,0,0.3) !important;
    }
    
    .stNumberInput > div > div:hover {
        border-color: var(--energy-green);
        box-shadow: 0 8px 16px rgba(129, 189, 71, 0.5), inset 0 2px 4px rgba(0,0,0,0.3) !important;
        transform: translateY(-1px);
    }
    
    .stNumberInput input {
        background-color: transparent !important;
        color: var(--alpine-white) !important;
        font-family: Arial, sans-serif !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
        border: none !important;
    }
    
    /* Enhanced Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--energy-green) 0%, #6ba534 100%);
        color: var(--alpine-white);
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-family: Arial, sans-serif;
        font-weight: 600;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 6px 12px rgba(129, 189, 71, 0.4), inset 0 1px 2px rgba(255,255,255,0.2);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #6ba534 0%, var(--energy-green) 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(129, 189, 71, 0.6), inset 0 1px 2px rgba(255,255,255,0.3);
    }
    
    /* Enhanced Checkbox styling */
    .stCheckbox > label {
        color: var(--alpine-white) !important;
        font-family: Arial, sans-serif !important;
        font-weight: 500 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
    }
    
    .stCheckbox > label > div {
        background-color: var(--cool-gray-10c) !important;
        border: 2px solid var(--energy-green) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3), inset 0 1px 2px rgba(0,0,0,0.2) !important;
    }
    
    /* Labels */
    .stSelectbox > label,
    .stNumberInput > label {
        color: var(--alpine-white) !important;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
    }
    
    /* Dialog/Modal styling */
    .stDialog {
        background-color: var(--charcoal) !important;
    }
    
    .stDialog h1, .stDialog h2, .stDialog h3, .stDialog h4, .stDialog h5, .stDialog h6 {
        color: var(--alpine-white) !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7) !important;
    }
    
    .stDialog p, .stDialog div, .stDialog span, .stDialog label {
        color: var(--alpine-white) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
    }
    
    .stDialog .stMarkdown {
        color: var(--alpine-white) !important;
    }
    
    .stDialog .stMarkdown h1, .stDialog .stMarkdown h2, .stDialog .stMarkdown h3, 
    .stDialog .stMarkdown h4, .stDialog .stMarkdown h5, .stDialog .stMarkdown h6 {
        color: var(--alpine-white) !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7) !important;
    }
    
    .stDialog .stMarkdown p, .stDialog .stMarkdown div, .stDialog .stMarkdown span {
        color: var(--alpine-white) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
    }
    
    .stDialog .stRadio > label {
        color: var(--alpine-white) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
    }
    
    .stDialog .stRadio > div > label {
        color: var(--alpine-white) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, var(--energy-green) 0%, #6ba534 100%);
        color: var(--alpine-white);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(129, 189, 71, 0.3);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        color: var(--alpine-white);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
    }
    
    /* Logo styling */
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.5rem 0;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .main-container {
            margin: 0.5rem;
            padding: 1rem;
        }
        
        .main-title {
            font-size: 1.8rem;
            margin-top: 0.5rem;
        }
        
        .subtitle {
            font-size: 1rem;
        }
        
        .form-container {
            padding: 1rem;
        }
        
        .stButton > button {
            width: 100%;
            margin: 0.5rem 0;
        }
        
        /* Mobile logo adjustments */
        .logo-container img {
            max-width: 150px !important;
            width: auto !important;
        }
    }
    
    /* Desktop optimization */
    @media (min-width: 1200px) {
        .main-container {
            max-width: 1200px;
            margin: 2rem auto;
        }
    }
</style>
""", unsafe_allow_html=True)

def inject_css_file(path: str):
    css = Path(path).read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def inject_theme_vars(colors: dict):
    st.markdown(
        f"""
        <style>
        :root {{
          --asphalt: {colors["Asphalt"]};
          --alpine: {colors["Alpine White"]};
          --concrete: {colors["Concrete"]};
          --energy: {colors["Energy Green"]};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def inject_theme_css():
    st.markdown(
        """
        <style>
        .cta-scope [data-testid="column"] .stButton { width: 100%; }
        .cta-scope .stButton > button{
            display:block; width:100%;
            background-color: var(--asphalt);
            color: var(--alpine);
            border: 2px solid var(--concrete);
            border-radius: 10px;
            font-weight: 700;
            padding: 12px 14px;
            text-shadow: 0 0 6px var(--energy);
            transition: box-shadow .25s ease, transform .15s ease;
        }
        .cta-scope .stButton > button:hover{
            box-shadow: 0 0 28px var(--energy);
            transform: translateY(-1px);
        }
        .cta-link{
            display:flex; align-items:center; justify-content:center;
            width:100%; min-height:56px; text-decoration:none!important;
            background-color: var(--asphalt);
            color: var(--alpine);
            border: 2px solid var(--concrete);
            border-radius: 10px;
            padding: 12px 14px;
            font-weight: 700;
            text-shadow: 0 0 6px var(--energy);
            transition: box-shadow .25s ease, transform .15s ease;
        }
        .cta-link:hover{ box-shadow: 0 0 28px var(--energy); transform: translateY(-1px); }
        </style>
        """,
        unsafe_allow_html=True,
    )

def ensure_global_css(colors: dict, extra_files: list[str] | None = None):
    if st.session_state.get("_css_injected"):
        return
    inject_theme_vars(colors)
    inject_theme_css()
    for f in (extra_files or []):
        try:
            inject_css_file(f)
        except FileNotFoundError:
            pass
    st.session_state["_css_injected"] = True

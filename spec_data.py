import streamlit as st
from spec_data import spec_data

def apply_custom_css():
    st.markdown("""
    <style>
    html, body, [class*="css"]  {
        max-width: 100vw;
        overflow-x: hidden;
    }

    .stApp {
        background: url("https://raw.githubusercontent.com/TimBuffington/EBOSS®-tool-V2/main/assets/bg.png") no-repeat center center fixed;
        background-size: cover;
    }

    .stSelectbox > div > div,
    .stTextInput > div > div,
    .stNumberInput > div > div,
    .stSlider > div,
    .stButton > button {
        background-color: #000000 !important;
        color: #81BD47 !important;
        border: 1px solid #D3D3D3 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease-in-out;
    }

    .stSelectbox div[role="combobox"] span,
    .stTextInput input,
    .stNumberInput input {
        color: #81BD47 !important;
        font-weight: bold !important;
    }

    .stButton > button:hover,
    .stSelectbox:hover > div > div,
    .stTextInput:hover > div > div,
    .stNumberInput:hover > div > div,
    .stSlider > div:hover {
        box-shadow: 0 0 20px 4px #81BD47 !important;
        border-color: #81BD47 !important;
        transform: scale(1.03);
    }

    .st-expanderHeader {
        color: #81BD47 !important;
        font-weight: bold !important;
    }

    .logo-header {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 1rem;
        margin-bottom: 2rem;
        width: 100%;
    }

    .logo-header img {
        max-width: 80%;
        height: auto;
        filter: drop-shadow(0 0 10px #81BD47);
    }

    .top-nav-print {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .print-button,
    .back-button {
        background-color: #000000 !important;
        color: #81BD47 !important;
        font-weight: bold;
        border: 1px solid #D3D3D3 !important;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        cursor: pointer;
    }

    .print-button:hover,
    .back-button:hover {
        box-shadow: 0 0 20px 4px #81BD47;
        border-color: #81BD47;
        transform: scale(1.03);
    }

    .footer {
        text-align: center;
        font-size: 12px;
        color: #81BD47;
        margin-top: 3rem;
        padding: 1rem 0;
        border-top: 1px solid #81BD47;
    }

    @media (max-width: 768px) {
        .stSelectbox > div > div,
        .stTextInput > div > div,
        .stNumberInput > div > div {
            font-size: 16px !important;
            padding: 0.4rem 0.8rem !important;
        }

        .stButton > button {
            font-size: 14px !important;
        }

        .logo-header img {
            max-width: 90%;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <script>
    function printPage() {
        window.print();
    }
    </script>
    <div class="top-nav-print">
        <button class="back-button" onclick="window.location.reload()">Back to Input</button>
        <button class="print-button" onclick="printPage()">Print This Page</button>
        <a href='mailto:EBOSSAPPLICATIONS@ANACORP.COM'><button class="print-button">Contact Support</button></a>
    </div>
    <div class="footer">
        EBOSS® Tool &copy; 2025 ANA Energy. All rights reserved. |
        <a href='https://anacorp.com' style='color:#81BD47; text-decoration: none;'>anacorp.com</a>
    </div>
    """, unsafe_allow_html=True)

# styling.py

import streamlit as st

def apply_custom_css():
    st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("app://./AdobeStock_209254754.jpeg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .main-title {{
            color: #FFFFFF;
            font-size: 2.5rem;
            text-align: center;
        }}
        .form-container {{
            background: rgba(0, 0, 0, 0.75);
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem 0;
            color: #FFF;
        }}
        .form-section-title {{
            font-size: 1.3rem;
            font-weight: 600;
            color: #81BD47;
        }}
        .info-box, .warning-box {{
            color: #FFF;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 8px;
        }}
        .info-box {{
            background-color: #81BD47;
        }}
        .warning-box {{
            background-color: #FF6B6B;
        }}

        /* Mobile styling */
        @media (max-width: 768px) {{
            .form-container {{
                padding: 1rem;
                margin: 0.5rem 0;
            }}

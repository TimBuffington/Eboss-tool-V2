import streamlit as st
import webbrowser

# Color mappings based on provided hex codes
COLORS = {
    "Asphalt": "#000000",
    "Concrete": "#939598",
    "Charcoal": "#636569",
    "Energy Green": "#81BD47",
    "Alpine White": "#FFFFFF",
    "Light Grey": "#D3D3D3"  # Added for border
}

# Apply custom CSS for branding, full-screen background, mobile-friendly, and container styles
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
    .sidebar .sidebar-content {{
        background-color: {COLORS['Asphalt']};
        color: {COLORS['Alpine White']};
    }}
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
    .stTextInput > div > div > input, .stSelectbox > div > div > div, .stNumberInput > div > div > input {{
        background-color: {COLORS['Asphalt']};
        color: {COLORS['Alpine White']};
        border: 1px solid {COLORS['Light Grey']};
        border-radius: 5px;
        padding: 8px;
        transition: box-shadow 0.3s ease;
        width: 100%;
    }}
    .stTextInput > div > div > input:hover, .stSelectbox > div > div > div:hover, .stNumberInput > div > div > input:hover {{
        box-shadow: 0 0 10px {COLORS['Energy Green']};
    }}
    .logo {{
        max-width: 150px;
        display: block;
        margin: 20px auto 0; /* Top center with margin */
    }}
    .footer {{
        text-align: center;
        color: {COLORS['Alpine White']};
        padding: 10px;
        background-color: {COLORS['Asphalt']};
        position: fixed;
        bottom: 0;
        width: 100%;
    }}
    @media (max-width: 768px) {{
        .logo {{
            max-width: 120px;
        }}
        button {{
            width: 100%;
            box-sizing: border-box;
        }}
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
    st.session_state.selected_option = "Select EBOSS® Model"
if "recommended_model" not in st.session_state:
    st.session_state.recommended_model = ""
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Corporate logo top center
st.image("https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/ANA-ENERGY-LOGO-HORIZONTAL-WHITE-GREEN.png", use_column_width=False, width=150, output_format="PNG", caption="ANA Logo")

# Page title
st.title("EBOSS® Size & Spec Tool")

# Buttons for Google Docs and YouTube
col_buttons = st.columns(1)
with col_buttons[0]:
    st.button("Request Demo", on_click=lambda: webbrowser.open_new_tab("https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform?usp=header"))
    st.button("Request Training", on_click=lambda: webbrowser.open_new_tab("https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform?usp=header"))
    st.button("Learn how the EBOSS® works", on_click=lambda: webbrowser.open_new_tab("https://youtu.be/0Om2qO-zZfM?si=XnLKJ_SfyKqqUI-g"))

# Radio buttons for EBOSS® option
st.session_state.selected_option = st.radio("Choose EBOSS® Configuration:", ("Select EBOSS® Model", "Get Recommended EBOSS® Model"))

# Text
st.write("Choose a page or tool and click Calculate to proceed.")

# Enter Data button with modal
if st.button("Enter Data"):
    if st.session_state.selected_option == "Get Recommended EBOSS® Model":
        # Placeholder for recommended model logic
        st.session_state.recommended_model = "EB 70 kVA"  # Example
        with st.dialog("Recommended EBOSS® Configuration"):
            st.write(f"Recommended EBOSS® Model: {st.session_state.recommended_model}")
            # Modal stops here as per your request
    else:  # Select EBOSS® Model
        with st.dialog("EBOSS® Configuration"):
            st.write("Enter your EBOSS® configuration:")
            # Modal stops here as per your request

# Footer with links (placeholder for other pages)
st.markdown(f"""
<div class="footer">
EBOSS® Size & Spec Tool | 
<a href="#" onclick="window.open('https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform?usp=header', '_blank')">Request Demo</a> |
<a href="#" onclick="window.open('https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform?usp=header', '_blank')">Request Training</a> |
<a href="#" onclick="window.open('https://youtu.be/0Om2qO-zZfM?si=XnLKJ_SfyKqqUI-g', '_blank')">Learn how the EBOSS® works</a>
</div>
""", unsafe_allow_html=True)

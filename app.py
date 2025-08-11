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
try:
    st.image("https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/logo.png", use_column_width=False, width=150, output_format="PNG")
except Exception as e:
    st.error(f"Logo failed to load: {e}. Please verify the file at https://github.com/TimBuffington/Eboss-tool-V2/tree/main/assets/logo.png.")

# Page title
st.title("EBOSS® Size & Spec Tool")

# Navbar for navigation (always visible)
navbar_pages = ["Home", "Technical Specs", "Load Based Specs", "EBOSS® to Standard Comparison", "Cost Analysis", "Parallel Calculator"]
st.session_state.page = st.radio("Navigate to:", navbar_pages, horizontal=True, index=navbar_pages.index(st.session_state.page))

if st.session_state.page == "Home":
    # Buttons for Google Docs and YouTube
    col_buttons = st.columns(1)
    with col_buttons[0]:
        st.link_button("Request Demo", url="https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform?usp=header")
        st.link_button("Request Training", url="https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform?usp=header")
        st.link_button("Learn how the EBOSS® works", url="https://youtu.be/0Om2qO-zZfM?si=XnLKJ_SfyKqqUI-g")

    # Radio buttons for EBOSS® option
    st.session_state.selected_option = st.radio("Choose EBOSS® Configuration:", ("Select EBOSS® Model", "Get Recommended EBOSS® Model"))

    # Text
    st.write("Choose a page or tool and click Enter Data to proceed.")

    # Enter Data button with modal
    if st.button("Enter Data"):
        try:
            print("Entering dialog...")  # Debug log to console
            if st.session_state.selected_option == "Get Recommended EBOSS® Model":
                st.session_state.recommended_model = "EB 70 kVA"  # Placeholder
                with st.dialog("Recommended EBOSS® Configuration") as dialog:
                    st.write(f"Recommended EBOSS® Model: {st.session_state.recommended_model}")
                    if st.button("Close", key="close_recommended"):
                        dialog.close()
            else:  # Select EBOSS® Model
                with st.dialog("EBOSS® Configuration") as dialog:
                    st.write("Enter your EBOSS® configuration:")
                    if st.button("Close", key="close_select"):
                        dialog.close()
        except Exception as e:
            print(f"Error in modal: {e}")  # Debug log to console
            st.error(f"Error in modal: {str(e)}. Please check the console output.")

elif st.session_state.page == "Technical Specs":
    st.header("Technical Specs")
    # Placeholder content
elif st.session_state.page == "Load Based Specs":
    st.header("Load Based Specs")
    # Placeholder content
elif st.session_state.page == "EBOSS® to Standard Comparison":
    st.header("EBOSS® to Standard Comparison")
    # Placeholder content
elif st.session_state.page == "Cost Analysis":
    st.header("Cost Analysis")
    # Placeholder content
elif st.session_state.page == "Parallel Calculator":
    st.header("Parallel Calculator")
    # Placeholder content

# Footer with links
st.markdown(f"""
<div class="footer">
EBOSS® Size & Spec Tool | 
<a href="#" onclick="window.open('https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform?usp=header', '_blank')">Request Demo</a> |
<a href="#" onclick="window.open('https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform?usp=header', '_blank')">Request Training</a> |
<a href="#" onclick="window.open('https://youtu.be/0Om2qO-zZfM?si=XnLKJ_SfyKqqUI-g', '_blank')">Learn how the EBOSS® works</a>
</div>
""", unsafe_allow_html=True)

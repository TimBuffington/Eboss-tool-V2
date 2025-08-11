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
        max-width: 200px; /* Restored original size */
        display: block;
        margin: 20px auto 0; /* Centered with top margin */
    }}
    .footer {{
        display: flex;
        justify-content: center;
        color: {COLORS['Alpine White']};
        padding: 10px;
        background-color: {COLORS['Asphalt']};
        position: fixed;
        bottom: 0;
        width: 100%;
    }}
    .button-container {{
        display: flex;
        justify-content: center;
        gap: 5px; /* Reduced gap for closer spacing */
        width: 100%;
    }}
    .button-block {{
        flex: 1;
        max-width: 300px; /* Equal width, adjustable for mobile */
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
    @media (max-width: 768px) {{
        .logo {{
            max-width: 160px; /* Adjusted for mobile */
        }}
        .button-container {{
            flex-direction: column;
            gap: 5px;
        }}
        .button-block {{
            max-width: 100%;
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
    st.session_state.selected_option = None  # No default selection
if "recommended_model" not in st.session_state:
    st.session_state.recommended_model = ""
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Corporate logo top center
try:
    st.image("https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/logo.png", use_container_width=False, width=200, output_format="PNG")
except Exception as e:
    st.error(f"Logo failed to load: {e}. Please verify the file at https://github.com/TimBuffington/Eboss-tool-V2/tree/main/assets/logo.png.")

# Page title centered under logo
st.markdown("<h1 style='text-align: center;'>EBOSS® Size & Spec Tool</h1>", unsafe_allow_html=True)

# Buttons for Google Docs and YouTube, centered horizontally with equal width
with st.container():
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    col_buttons = st.columns(3)
    with col_buttons[0]:
        st.markdown("<div class='button-block'>", unsafe_allow_html=True)
        st.link_button("Request Demo", url="https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform?usp=header")
        st.markdown("</div>", unsafe_allow_html=True)
    with col_buttons[1]:
        st.markdown("<div class='button-block'>", unsafe_allow_html=True)
        st.link_button("Request Training", url="https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform?usp=header")
        st.markdown("</div>", unsafe_allow_html=True)
    with col_buttons[2]:
        st.markdown("<div class='button-block'>", unsafe_allow_html=True)
        st.link_button("Learn how the EBOSS® works", url="https://youtu.be/0Om2qO-zZfM?si=XnLKJ_SfyKqqUI-g")
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Message centered under buttons with increased size and glow effect
st.markdown(f"<div class='message-text'>Please Select a Configuration</div>", unsafe_allow_html=True)

# Radio buttons centered under message
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
selected_option = st.radio(" ", ("Select a EBOSS® Model", "Use Load Based Suggested EBOSS® Model"), horizontal=True)
st.session_state.selected_option = selected_option  # Update session state
st.markdown("</div>", unsafe_allow_html=True)

# Enter Data button centered under radio buttons
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if st.button("Enter Data", key="enter_data_button"):
    try:
        print("Entering dialog...")  # Debug log to console
        if st.session_state.selected_option == "Use Load Based Suggested EBOSS® Model":
            st.session_state.recommended_model = "EB 70 kVA"  # Placeholder
            dialog = st.dialog("Recommended EBOSS® Configuration")
            dialog.markdown(f"Recommended EBOSS® Model: {st.session_state.recommended_model}")  # Changed from write to markdown
            col1, col2, col3 = dialog.columns(3)
            with col2:
                dialog.number_input("Max Continuous Load", min_value=0.0, step=0.1, key="max_continuous_load_input")
                dialog.number_input("Max Peak Load", min_value=0.0, step=0.1, key="max_peak_load_input")
                dialog.selectbox("Units", options=["kW", "Amps"], key="units_input")
                dialog.selectbox("Voltage", options=["120", "240", "208", "480"], key="voltage_input")
            if dialog.button("Launch Tool", key="launch_tool_recommended"):
                # Convert load to kW at 480V three-phase if needed
                max_continuous_load = float(st.session_state.get("max_continuous_load_input", "0.0"))
                max_peak_load = float(st.session_state.get("max_peak_load_input", "0.0"))
                units = st.session_state.get("units_input", "kW")
                voltage = st.session_state.get("voltage_input", "480")
                if units == "Amps":
                    pf = 0.8  # Power Factor
                    st.session_state.user_inputs["actual_continuous_load"] = (max_continuous_load * float(voltage) * 1.732 * pf) / 1000
                    st.session_state.user_inputs["actual_peak_load"] = (max_peak_load * float(voltage) * 1.732 * pf) / 1000
                else:
                    st.session_state.user_inputs["actual_continuous_load"] = max_continuous_load
                    st.session_state.user_inputs["actual_peak_load"] = max_peak_load
                st.session_state.user_inputs["max_continuous_load"] = max_continuous_load
                st.session_state.user_inputs["max_peak_load"] = max_peak_load
                st.session_state.user_inputs["units"] = units
                st.session_state.user_inputs["voltage"] = voltage
                st.session_state.show_calculator = True
                st.session_state.page = "Tool Selection"
                dialog.close()
                st.rerun()
        else:  # Select a EBOSS® Model
            dialog = st.dialog("EBOSS® Configuration")
            dialog.markdown("Enter your EBOSS® configuration:")  # Changed from write to markdown
            col1, col2, col3 = dialog.columns(3)
            with col1:
                dialog.selectbox("EBOSS® Model", options=["EB 25 kVA", "EB 70 kVA", "EB 125 kVA", "EB 220 kVA", "EB 400 kVA"], key="eboss_model_input")
                dialog.selectbox("EBOSS® Type", options=["Full Hybrid", "Power Module"], key="eboss_type_input")
                if st.session_state.get("eboss_type_input", "") == "Power Module":
                    dialog.selectbox("Power Module Generator Size", options=["25 kVA", "70 kVA", "125 kVA", "220 kVA", "400 kVA"], key="power_module_gen_size_input")
            with col2:
                dialog.number_input("Max Continuous Load", min_value=0.0, step=0.1, key="max_continuous_load_input")
                dialog.number_input("Max Peak Load", min_value=0.0, step=0.1, key="max_peak_load_input")
            with col3:
                dialog.selectbox("Units", options=["kW", "Amps"], key="units_input")
                dialog.selectbox("Voltage", options=["120", "240", "208", "480"], key="voltage_input")
            if dialog.button("Launch Tool", key="launch_tool_select"):
                # Store input data
                st.session_state.user_inputs["eboss_model"] = st.session_state.get("eboss_model_input", "")
                st.session_state.user_inputs["eboss_type"] = st.session_state.get("eboss_type_input", "")
                st.session_state.user_inputs["power_module_gen_size"] = st.session_state.get("power_module_gen_size_input", "")
                st.session_state.user_inputs["max_continuous_load"] = st.session_state.get("max_continuous_load_input", 0.0)
                st.session_state.user_inputs["max_peak_load"] = st.session_state.get("max_peak_load_input", 0.0)
                st.session_state.user_inputs["units"] = st.session_state.get("units_input", "kW")
                st.session_state.user_inputs["voltage"] = st.session_state.get("voltage_input", "480")
                # Convert to kW if needed
                if st.session_state.user_inputs["units"] == "Amps":
                    pf = 0.8  # Power Factor
                    st.session_state.user_inputs["actual_continuous_load"] = (st.session_state.user_inputs["max_continuous_load"] * float(st.session_state.user_inputs["voltage"]) * 1.732 * pf) / 1000
                    st.session_state.user_inputs["actual_peak_load"] = (st.session_state.user_inputs["max_peak_load"] * float(st.session_state.user_inputs["voltage"]) * 1.732 * pf) / 1000
                else:
                    st.session_state.user_inputs["actual_continuous_load"] = st.session_state.user_inputs["max_continuous_load"]
                    st.session_state.user_inputs["actual_peak_load"] = st.session_state.user_inputs["max_peak_load"]
                st.session_state.show_calculator = True
                st.session_state.page = "Tool Selection"
                dialog.close()
                st.rerun()
    except Exception as e:
        print(f"Error in modal: {e}")  # Debug log to console
        st.error(f"Error in modal: {str(e)}. Please check the console output.")

elif st.session_state.page == "Tool Selection":
    st.header("Tool Selection")
    # Placeholder for tool selection page
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
    <span style="display: flex; justify-content: center; width: 100%;">
        EBOSS® Size & Spec Tool | 
        <a href="#" onclick="window.open('https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform?usp=header', '_blank')">Request Demo</a> |
        <a href="#" onclick="window.open('https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform?usp=header', '_blank')">Request Training</a> |
        <a href="#" onclick="window.open('https://youtu.be/0Om2qO-zZfM?si=XnLKJ_SfyKqqUI-g', '_blank')">Learn how the EBOSS® works</a>
    </span>
</div>
""", unsafe_allow_html=True)

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
        align-items: center;
        width: 100%;
        text-align: center;
        margin: 0 auto;
        max-width: 840px;   /* tightened center column */
        gap: 12px;
    }}

    .sidebar .sidebar-content {{
        background-color: {COLORS['Asphalt']};
        color: {COLORS['Alpine White']};
    }}

    /* Buttons */
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

    /* Three-button row perfectly centered */
    .button-row-wrap {{
        width: 100%;
        display: flex;
        justify-content: center;   /* centers the inner row */
    }}
    .button-row-inner {{
        display: inline-flex;      /* shrink to content width */
        gap: 10px;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
        max-width: 100%;
    }}
    .button-row-inner .button-block {{
        min-width: 220px;
        max-width: 300px;
        flex: 0 0 auto;            /* don’t stretch */
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

    /* Enter Data button container */
    .centered-button {{ width: 100%; }}

    /* Footer centered */
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
        .button-row-inner .button-block {{ min-width: 180px; }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)
.main-center-stack { max-width: 840px; }
.button-row-wrap {
  width: 100%;
  display: flex;
  justify-content: center;      
}
.button-row-inner {
  display: inline-flex;        
  gap: 10px;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;             
  max-width: 100%;
}
.button-row-inner .button-block {
  min-width: 220px;
  max-width: 300px;
  flex: 0 0 auto;              
}
@media (max-width: 768px) (
    .button-row-inner .button-block { min-width: 180px; }
}}
   </style>
    """ 
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

# ===== MAIN CENTER STACK (keeps everything on the same center axis) =====
st.markdown("<div class='main-center-stack'>", unsafe_allow_html=True)

# Logo
st.markdown("<div class='logo-container'>", unsafe_allow_html=True)
try:
    st.image(
        "https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/logo.png",
        use_container_width=False,
        width=200,
        output_format="PNG",
    )
except Exception as e:
    st.error(f"Logo failed to load: {e}. Please verify the file at https://github.com/TimBuffington/Eboss-tool-V2/tree/main/assets/logo.png.")
st.markdown("</div>", unsafe_allow_html=True)

# Title
st.markdown("<h1>EBOSS® Size & Spec Tool</h1>", unsafe_allow_html=True)

# Three link buttons row
# --- Three link buttons row (perfectly centered) ---
st.markdown("<div class='button-row-wrap'><div class='button-row-inner'>", unsafe_allow_html=True)
b1, b2, b3 = st.columns([1, 1, 1], gap="small")
with b1:
    st.markdown("<div class='button-block'>", unsafe_allow_html=True)
    st.link_button("Request Demo", url="https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform?usp=header")
    st.markdown("</div>", unsafe_allow_html=True)
with b2:
    st.markdown("<div class='button-block'>", unsafe_allow_html=True)
    st.link_button("Request Training", url="https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform?usp=header")
    st.markdown("</div>", unsafe_allow_html=True)
with b3:
    st.markdown("<div class='button-block'>", unsafe_allow_html=True)
    st.link_button("Learn how the EBOSS® works", url="https://youtu.be/0Om2qO-zZfM?si=XnLKJ_SfyKqqUI-g")
    st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div></div>", unsafe_allow_html=True)


# Message row
st.markdown("<div class='message-text'>Please Select a Configuration</div>", unsafe_allow_html=True)

# Radio buttons (centered as a group)
st.markdown("<div class='centered-radio'>", unsafe_allow_html=True)
selected_option = st.radio(" ", ("Select a EBOSS® Model", "Use Load Based Suggested EBOSS® Model"), horizontal=True)
st.session_state.selected_option = selected_option
st.markdown("</div>", unsafe_allow_html=True)

# Enter Data button (centered)
st.markdown("<div class='centered-button'>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    enter_clicked = st.button("Enter Data", key="enter_data_button")
st.markdown("</div>", unsafe_allow_html=True)

# ===== Dialog handling (correct st.dialog usage) =====
if enter_clicked:
    try:
        print("Entering dialog...")
        if st.session_state.selected_option == "Use Load Based Suggested EBOSS® Model":
            st.session_state.recommended_model = "EB 70 kVA"  # Placeholder

            @st.dialog("Recommended EBOSS® Configuration")
            def show_recommended_dialog():
                st.markdown(f"**Recommended EBOSS® Model:** {st.session_state.recommended_model}")
                col1, col2, col3 = st.columns(3)
                with col2:
                    st.number_input("Max Continuous Load", min_value=0.0, step=0.1, key="max_continuous_load_input")
                    st.number_input("Max Peak Load", min_value=0.0, step=0.1, key="max_peak_load_input")
                    st.selectbox("Units", options=["kW", "Amps"], key="units_input")
                    st.selectbox("Voltage", options=["120", "240", "208", "480"], key="voltage_input")

                if st.button("Launch Tool", key="launch_tool_recommended"):
                    max_continuous_load = float(st.session_state.get("max_continuous_load_input", 0.0))
                    max_peak_load = float(st.session_state.get("max_peak_load_input", 0.0))
                    units = st.session_state.get("units_input", "kW")
                    voltage = st.session_state.get("voltage_input", "480")

                    if units == "Amps":
                        pf = 0.8
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
                    st.rerun()  # closes dialog

            show_recommended_dialog()

        else:
            @st.dialog("EBOSS® Configuration")
            def show_config_dialog():
                st.markdown("Enter your EBOSS® configuration:")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.selectbox("EBOSS® Model", options=["EB 25 kVA", "EB 70 kVA", "EB 125 kVA", "EB 220 kVA", "EB 400 kVA"], key="eboss_model_input")
                    st.selectbox("EBOSS® Type", options=["Full Hybrid", "Power Module"], key="eboss_type_input")
                    if st.session_state.get("eboss_type_input", "") == "Power Module":
                        st.selectbox("Power Module Generator Size", options=["25 kVA", "70 kVA", "125 kVA", "220 kVA", "400 kVA"], key="power_module_gen_size_input")
                with col2:
                    st.number_input("Max Continuous Load", min_value=0.0, step=0.1, key="max_continuous_load_input")
                    st.number_input("Max Peak Load", min_value=0.0, step=0.1, key="max_peak_load_input")
                with col3:
                    st.selectbox("Units", options=["kW", "Amps"], key="units_input")
                    st.selectbox("Voltage", options=["120", "240", "208", "480"], key="voltage_input")

                if st.button("Launch Tool", key="launch_tool_select"):
                    st.session_state.user_inputs["eboss_model"] = st.session_state.get("eboss_model_input", "")
                    st.session_state.user_inputs["eboss_type"] = st.session_state.get("eboss_type_input", "")
                    st.session_state.user_inputs["power_module_gen_size"] = st.session_state.get("power_module_gen_size_input", "")
                    st.session_state.user_inputs["max_continuous_load"] = st.session_state.get("max_continuous_load_input", 0.0)
                    st.session_state.user_inputs["max_peak_load"] = st.session_state.get("max_peak_load_input", 0.0)
                    st.session_state.user_inputs["units"] = st.session_state.get("units_input", "kW")
                    st.session_state.user_inputs["voltage"] = st.session_state.get("voltage_input", "480")

                    if st.session_state.user_inputs["units"] == "Amps":
                        pf = 0.8
                        st.session_state.user_inputs["actual_continuous_load"] = (st.session_state.user_inputs["max_continuous_load"] * float(st.session_state.user_inputs["voltage"]) * 1.732 * pf) / 1000
                        st.session_state.user_inputs["actual_peak_load"] = (st.session_state.user_inputs["max_peak_load"] * float(st.session_state.user_inputs["voltage"]) * 1.732 * pf) / 1000
                    else:
                        st.session_state.user_inputs["actual_continuous_load"] = st.session_state.user_inputs["max_continuous_load"]
                        st.session_state.user_inputs["actual_peak_load"] = st.session_state.user_inputs["max_peak_load"]

                    st.session_state.show_calculator = True
                    st.session_state.page = "Tool Selection"
                    st.rerun()  # closes dialog

            show_config_dialog()

    except Exception as e:
        print(f"Error in modal: {e}")
        st.error(f"Error in modal: {str(e)}. Please check the console output.")

# Close the center stack wrapper
st.markdown("</div>", unsafe_allow_html=True)

# Page routes (placeholders for now)
if st.session_state.page == "Tool Selection":
    st.header("Tool Selection")
elif st.session_state.page == "Technical Specs":
    st.header("Technical Specs")
elif st.session_state.page == "Load Based Specs":
    st.header("Load Based Specs")
elif st.session_state.page == "EBOSS® to Standard Comparison":
    st.header("EBOSS® to Standard Comparison")
elif st.session_state.page == "Cost Analysis":
    st.header("Cost Analysis")
elif st.session_state.page == "Parallel Calculator":
    st.header("Parallel Calculator")

# Footer (centered)
st.markdown(f"""
<div class="footer">
  <div class="footer-inner">
    <span>EBOSS® Size & Spec Tool</span>
    <span>|</span>
    <a href="#" onclick="window.open('https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform?usp=header', '_blank')">Request Demo</a>
    <span>|</span>
    <a href="#" onclick="window.open('https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform?usp=header', '_blank')">Request Training</a>
    <span>|</span>
    <a href="#" onclick="window.open('https://youtu.be/0Om2qO-zZfM?si=XnLKJ_SfyKqqUI-g', '_blank')">Learn how the EBOSS® works</a>
  </div>
</div>
""", unsafe_allow_html=True)

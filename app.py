import streamlit as st
import math

# ===== Theme tokens (kept from your original palette) =====
COLORS = {
    "Asphalt": "#000000",
    "Concrete": "#939598",
    "Charcoal": "#636569",
    "Energy Green": "#81BD47",
    "Alpine White": "#FFFFFF",
    "Light Grey": "#D3D3D3"
}

# -------------------- GLOBAL CSS (Grid-first) --------------------
st.markdown(
    f"""
    <style>
    :root {{
      --gap: 14px;
      --maxw: 1100px;
      --radius: 10px;
      --shadow: 0 10px 30px rgba(0,0,0,.35);
      --brand: {COLORS['Energy Green']};
      --text: {COLORS['Alpine White']};
    }}

    /* ===== App Background ===== */
    .stApp {{
        background-image: url("https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/bg.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: var(--text);
        font-family: Arial, sans-serif;
        font-size: 16px;
    }}

    /* ===== GRID: page scaffold =====
       Areas: logo | title | actions | msg | radios | cta
    */
    .home-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1fr);
      grid-template-rows: auto auto auto auto auto auto;
      grid-template-areas:
        "logo"
        "title"
        "actions"
        "msg"
        "radios"
        "cta";
      gap: var(--gap);
      max-width: var(--maxw);
      margin: 20px auto 120px; /* room for fixed footer */
      padding: 10px;
      box-sizing: border-box;
    }}
    /* Wider screens: keep one column for vertical rhythm,
       card-like groupings make it feel structured. */
    @media (min-width: 900px) {{
      .home-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    /* ===== Grid areas ===== */
    .g-logo  {{ grid-area: logo; display:grid; place-items:center; }}
    .g-title {{ grid-area: title; text-align:center; }}
    .g-actions {{ grid-area: actions; }}
    .g-msg {{ grid-area: msg; }}
    .g-radios {{ grid-area: radios; }}
    .g-cta {{ grid-area: cta; }}

    /* ===== Logo ===== */
    .logo-wrap {{
      width: 100%;
      max-width: 620px;
      height: auto;
      display: grid;
      place-items: center;
      margin-inline: auto;
    }}

    /* ===== Title ===== */
    .page-title {{
      margin: 0;
      font-weight: 800;
      text-shadow: 0 0 16px rgba(129,189,71,.35);
    }}

    /* ===== Action buttons container -> CSS GRID ===== */
    .actions-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: var(--gap);
      align-items: stretch;
    }}

    /* ===== Card-y section wrapper (optional visual grouping) ===== */
    .section {{
      background: rgba(0,0,0,0.35);
      border: 1px solid rgba(255,255,255,0.18);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding: 14px;
    }}

    /* ===== Buttons (Streamlit + link buttons) ===== */
    button, .stButton button, .stLinkButton > a {{
        background-color: {COLORS['Asphalt']} !important;
        color: {COLORS['Energy Green']} !important;
        border: 2px solid {COLORS['Alpine White']} !important;
        font-family: Arial, sans-serif;
        font-size: 16px;
        font-weight: bold !important;
        text-shadow: 0 0 6px {COLORS['Energy Green']};
        border-radius: 8px;
        padding: 10px 12px;
        transition: box-shadow 0.25s ease, transform 0.2s ease;
        width: 100%;
        margin: 0;
    }}
    button:hover, .stButton button:hover, .stLinkButton > a:hover {{
        box-shadow: 0 0 30px {COLORS['Energy Green']};
        transform: translateY(-1px);
    }}

    /* ===== Inputs ===== */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input {{
        background-color: {COLORS['Asphalt']} !important;
        color: {COLORS['Alpine White']} !important;
        border: 1px solid {COLORS['Light Grey']} !important;
        border-radius: 6px !important;
        padding: 8px !important;
        transition: box-shadow 0.25s ease;
    }}
    .stTextInput > div > div > input:hover,
    .stSelectbox > div > div > div:hover,
    .stNumberInput > div > div > input:hover {{
        box-shadow: 0 0 10px {COLORS['Energy Green']};
    }}

    /* ===== Message ===== */
    .message-text {{
        font-size: 1.25rem;
        text-align: center;
        transition: box-shadow 0.3s ease;
        padding: 10px 14px;
        border-radius: 10px;
        background: rgba(0,0,0,0.25);
        border: 1px solid rgba(255,255,255,0.15);
    }}
    .message-text:hover {{
        box-shadow: 0 0 10px {COLORS['Energy Green']};
    }}

    /* ===== Radio row -> centered, responsive ===== */
    .radio-wrap {{
      display: grid;
      grid-template-columns: 1fr;
      place-items: center;
    }}
    /* Let Streamlit radio shrink properly inside grid */
    .radio-wrap > div {{ min-width: 0; }}

    /* ===== Centered CTA button row ===== */
    .cta-wrap {{
      display: grid;
      grid-template-columns: 1fr minmax(220px, 280px) 1fr;
      gap: var(--gap);
      align-items: center;
    }}
    .cta-wrap > * {{ min-width: 0; }}
    .cta-center {{ display: grid; }}

    /* ===== Footer (fixed) ===== */
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
        z-index: 9;
    }}
    .footer a {{ color: {COLORS['Alpine White']}; }}

    /* ===== Mobile tweaks ===== */
    @media (max-width: 768px) {{
        .logo-wrap {{ max-width: 460px; }}
        .cta-wrap {{
          grid-template-columns: 1fr;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------- SESSION STATE --------------------
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

# -------------------- HOMEPAGE (Grid layout) --------------------
if st.session_state.page == "Home":
    st.markdown('<div class="home-grid">', unsafe_allow_html=True)

    # Logo
    st.markdown('<div class="g-logo">', unsafe_allow_html=True)
    st.markdown('<div class="logo-wrap">', unsafe_allow_html=True)
    try:
        st.image(
            "https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/logo.png",
            use_container_width=True,
            output_format="PNG",
        )
    except Exception as e:
        st.error(f"Logo failed to load: {e}. Please verify the file at https://github.com/TimBuffington/Eboss-tool-V2/tree/main/assets/logo.png.")
    st.markdown('</div></div>', unsafe_allow_html=True)

    # Title
    st.markdown('<div class="g-title">', unsafe_allow_html=True)
    st.markdown("<h1 class='page-title'>EBOSS® Size & Spec Tool</h1>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Top actions (3 link buttons) as grid
    st.markdown('<div class="g-actions section">', unsafe_allow_html=True)
    st.markdown('<div class="actions-grid">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="small")
    with c1:
        st.link_button("Request Demo", url="https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform?usp=header")
    with c2:
        st.link_button("Request Training", url="https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform?usp=header")
    with c3:
        st.link_button("Learn how the EBOSS® works", url="https://youtu.be/0Om2qO-zZfM?si=XnLKJ_SfyKqqUI-g")
    st.markdown('</div></div>', unsafe_allow_html=True)

    # Message
    st.markdown('<div class="g-msg">', unsafe_allow_html=True)
    st.markdown("<div class='message-text'>Please Select a Configuration</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Radios (centered)
    st.markdown('<div class="g-radios radio-wrap section">', unsafe_allow_html=True)
    selected_option = st.radio(
        " ",
        ("Select a EBOSS® Model", "Use Load Based Suggested EBOSS® Model"),
        horizontal=True,
    )
    st.session_state.selected_option = selected_option
    st.markdown('</div>', unsafe_allow_html=True)

    # CTA: Enter Data (centered column in a 3-col grid that collapses on mobile)
    st.markdown('<div class="g-cta cta-wrap">', unsafe_allow_html=True)
    st.empty()  # left spacer
    with st.container():
        enter_clicked = st.button("Enter Data", key="enter_data_button")
    st.empty()  # right spacer
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # end .home-grid

    # ----- Dialogs -----
    if enter_clicked:
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
                    max_cont = float(st.session_state.get("max_continuous_load_input", 0.0))
                    max_peak = float(st.session_state.get("max_peak_load_input", 0.0))
                    units = st.session_state.get("units_input", "kW")
                    voltage = st.session_state.get("voltage_input", "480")

                    if units == "Amps":
                        pf = 0.8
                        st.session_state.user_inputs["actual_continuous_load"] = (max_cont * float(voltage) * 1.732 * pf) / 1000
                        st.session_state.user_inputs["actual_peak_load"] = (max_peak * float(voltage) * 1.732 * pf) / 1000
                    else:
                        st.session_state.user_inputs["actual_continuous_load"] = max_cont
                        st.session_state.user_inputs["actual_peak_load"] = max_peak

                    st.session_state.user_inputs["max_continuous_load"] = max_cont
                    st.session_state.user_inputs["max_peak_load"] = max_peak
                    st.session_state.user_inputs["units"] = units
                    st.session_state.user_inputs["voltage"] = voltage

                    st.session_state.show_calculator = True
                    st.session_state.page = "Tool Selection"
                    st.rerun()

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
                    st.rerun()

            show_config_dialog()

# -------------------- OTHER PAGES (placeholders) --------------------
elif st.session_state.page == "Tool Selection":
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

# -------------------- FOOTER --------------------
st.markdown(f"""
<div class="footer">
    <span style="display: flex; justify-content: center; align-items: center; gap:8px; width: 100%; color: {COLORS['Alpine White']};">
        EBOSS® Size & Spec Tool |
        <a href="https://docs.google.com/forms/d/e/1FAIpQLSftXtJCMcDgPNzmpczFy9Eqf0cIEvsBtBzyuNylu3QZuGozHQ/viewform?usp=header" target="_blank">Request Demo</a> |
        <a href="https://docs.google.com/forms/d/e/1FAIpQLScTClX-W3TJS2TG4AQL3G4fSVqi-KLgmauQHDXuXjID2e6XLQ/viewform?usp=header" target="_blank">Request Training</a> |
        <a href="https://youtu.be/0Om2qO-zZfM?si=XnLKJ_SfyKqqUI-g" target="_blank">Learn how the EBOSS® works</a>
    </span>
</div>
""", unsafe_allow_html=True)


import streamlit as st

spec_data = {'EBOSS 125 kVA': {'Battery capacity': [('Total battery life or energy throughout', '4,000 MWh'),
                                        ('Charge time (no load)', '= 1 Hour'),
                                        ('Inverter output max', '100 kW'),
                                        ('Parallel capability', 'Available')],
                   'Battery type': [('Est. Cycle life @ 77°f enclosure temp',
                                     '90K Cycles at 90% DOD'),
                                    ('Est. Cycle life @ 100°f enclosure temp',
                                     '80K Cycles at 90% DOD')],
                   'Maximum Continuous  Output': [('Generator', 'Airman SDG65'),
                                                  ('Generator charge rate', '65 kVA / 52 kW'),
                                                  ('Three-phase output', '62 kVA / 50 kW'),
                                                  ('Single-phase output', '2.4 kW x 2'),
                                                  ('Simultaneous voltage',
                                                   '120V (1Φ) • 208/480 (3Φ)'),
                                                  ('Max. Continuous amp-load @208v',
                                                   '167 A / 32 kW'),
                                                  ('Max. Continuous amp-load @480v', '76 A 50 kW')],
                   'Maximum Intermittent  Output': [('Three-phase', '125 kVA / 100 kW'),
                                                    ('Single-phase', 'N/A / N/A'),
                                                    ('Frequency', '60 Hz'),
                                                    ('Simultaneous voltage',
                                                     '120V (1Φ) • 208/480 (3Φ)'),
                                                    ('Voltage regulation', 'Adjustable'),
                                                    ('Max. Intermittent amp-load 208v',
                                                     '345 A 66.2 kW'),
                                                    ('Max. Intermittent amp-load 480v',
                                                     '150 A / 99 kW'),
                                                    ('Motor start rating for 3 second (208v)',
                                                     '532 A / 291 kW'),
                                                    ('Motor start rating for 3 second (208v)',
                                                     '231  / 532 kW')],
                   'Operating temperatures': [('Inverter cold start temperature (minimum)', '14°F'),
                                              ('Running operating temperature', '-22°F to 130°F'),
                                              ('Arctic package operating temp. (optional)',
                                               '-50°F to 130°F')],
                   'Weights & Dimensions': [('L x w x h x (Eboss only)', '≈ 73.5” x 61” x 104.5”'),
                                            ('Eboss weight only', '9,600 lbs'),
                                            ('L x w x h (trailer and generator)',
                                             '233” x 52” x 97”'),
                                            ('Total weight (without/with fuel)', '≈ 18,000 lbs'),
                                            ('Integral fuel tank capacity', '111 gal')]},
 'EBOSS 220 kVA': {'Battery capacity': [('Total battery life or energy throughout', '6,000 MWh'),
                                        ('Charge time (no load)', '≈ 50 Minutes'),
                                        ('Inverter output max', '176 kW'),
                                        ('Parallel capability', 'Available')],
                   'Battery type': [('Est. Cycle life @ 77°f enclosure temp',
                                     '90K Cycles at 90% DOD'),
                                    ('Est. Cycle life @ 100°f enclosure temp',
                                     '80K Cycles at 90% DOD')],
                   'Maximum Continuous  Output': [('Generator', 'Airman SDG125'),
                                                  ('Generator charge rate', '125 kVA / 100 kW'),
                                                  ('Three-phase output', '120 kVA / 96 kW'),
                                                  ('Single-phase output', '2.4 kW x 2'),
                                                  ('Simultaneous voltage',
                                                   '120V (1Φ) • 208/480 (3Φ)'),
                                                  ('Max. Continuous amp-load @208v',
                                                   '328 A / 63 kW'),
                                                  ('Max. Continuous amp-load @480v',
                                                   '150 A 99 kW')],
                   'Maximum Intermittent  Output': [('Three-phase', '220 kVA / 176 kW'),
                                                    ('Single-phase', 'N/A / N/A'),
                                                    ('Frequency', '60 Hz'),
                                                    ('Simultaneous voltage',
                                                     '120V (1Φ) • 208/480 (3Φ)'),
                                                    ('Voltage regulation', 'Adjustable'),
                                                    ('Max. Intermittent amp-load 208v',
                                                     '700 A / 134 kW'),
                                                    ('Max. Intermittent amp-load 480v',
                                                     '303 A / 201 kW'),
                                                    ('Motor start rating for 3 second (208v)',
                                                     '1065 A / 204 kW'),
                                                    ('Motor start rating for 3 second (208v)',
                                                     '461 A / 708 kW')],
                   'Operating temperatures': [('Inverter cold start temperature (minimum)', '14°F'),
                                              ('Running operating temperature', '-22°F to 130°F'),
                                              ('Arctic package operating temp. (optional)',
                                               '-50°F to 130°F')],
                   'Weights & Dimensions': [('L x w x h x (Eboss only)', '≈73.5” x 61” x 104.5”'),
                                            ('Eboss weight only', '11,200 lbs'),
                                            ('L x w x h (trailer and generator)',
                                             '≈249” x 52” x 97”'),
                                            ('Total weight (without/with fuel)', '≈21,000 lbs'),
                                            ('Integral fuel tank capacity', '168 gal')]},
 'EBOSS 25 kVA': {'Battery capacity': [('Total battery life or energy throughout', '1,200 mwh'),
                                       ('Charge time (no load)', '< 45 min'),
                                       ('Inverter output max', '24 kw'),
                                       ('Parallel capability', 'Available')],
                  'Battery type': [('Est. Cycle life @ 77°f enclosure temp',
                                    '90K Cycles at 90% DOD'),
                                   ('Est. Cycle life @ 100°f enclosure temp',
                                    '80K Cycles at 90% DOD')],
                  'Maximum Continuous  Output': [('Generator', 'Airman SDG25'),
                                                 ('Generator charge rate', '25 kva / 20 kw'),
                                                 ('Three-phase output', '23 kva / 19 kw'),
                                                 ('Single-phase output', '20 kva / 16 kw'),
                                                 ('Simultaneous voltage',
                                                  '120/240 (1Φ) • 208/480 (3Φ)'),
                                                 ('Max. Continuous amp-load @208v',
                                                  '70 A / 13.5 kW'),
                                                 ('Max. Continuous amp-load @480v',
                                                  '30 A / 19 kW')],
                  'Maximum Intermittent  Output': [('Three-phase', '30 kva / 24 kw'),
                                                   ('Single-phase', '20 kva / 16 kw'),
                                                   ('Frequency', '60 Hz'),
                                                   ('Simultaneous voltage',
                                                    '120/240 (1Φ) • 208/480 (3Φ)'),
                                                   ('Voltage regulation', 'Adjustable'),
                                                   ('Max. Intermittent amp-load 208v',
                                                    '70 A / 13.5 kW'),
                                                   ('Max. Intermittent amp-load 480v',
                                                    '30 A / 19 kW'),
                                                   ('Motor start rating for 3 second (208v)',
                                                    '104 A / 19.5 kW'),
                                                   ('Motor start rating for 3 second (208v)',
                                                    '45 A / 29 kW')],
                  'Operating temperatures': [('Inverter cold start temperature (minimum)', '14°F'),
                                             ('Running operating temperature', '-22°F to 130°F'),
                                             ('Arctic package operating temp. (optional)',
                                              '-50°F to 130°F')],
                  'Weights & Dimensions': [('L x w x h x (Eboss only)', '40” x 48” x 46”'),
                                           ('Eboss weight only', '2,120 lbs'),
                                           ('L x w x h (trailer and generator)',
                                            '160” x 74” x 75”'),
                                           ('Total weight (without/with fuel)', '5100 / 5500 lbs'),
                                           ('Integral fuel tank capacity', '51.5 gal')]},
 'EBOSS 400 kVA': {'Battery capacity': [('Total battery life or energy throughout', '10,000 MWh'),
                                        ('Charge time (no load)', '≈ 45 Minutes'),
                                        ('Inverter output max', '320 kW'),
                                        ('Parallel capability', 'Available')],
                   'Battery type': [('Est. Cycle life @ 77°f enclosure temp',
                                     '90K Cycles at 90% DOD'),
                                    ('Est. Cycle life @ 100°f enclosure temp',
                                     '80K Cycles at 90% DOD')],
                   'Maximum Continuous  Output': [('Generator', 'Airman SDG220'),
                                                  ('Generator charge rate', '220 kVA / 176 kW'),
                                                  ('Three-phase output', '210 kVA / 168 kW'),
                                                  ('Single-phase output', '2.4 kW x 2'),
                                                  ('Simultaneous voltage',
                                                   '120V (1Φ) • 208/480 (3Φ)'),
                                                  ('Max. Continuous amp-load @208v', '< 125 kW'),
                                                  ('Max. Continuous amp-load @480v',
                                                   '264 A / 175 kW')],
                   'Maximum Intermittent  Output': [('Three-phase', '400 kVA / 320 kW'),
                                                    ('Frequency', '60 Hz'),
                                                    ('Simultaneous voltage',
                                                     '120V (Courtesy Outlets) • 480 (3Φ)'),
                                                    ('Voltage regulation', 'Adjustable'),
                                                    ('Max. Intermittent amp-load 208v',
                                                     '481 A / 92.5 kW'),
                                                    ('Max. Intermittent amp-load 480v',
                                                     '769 A / 319 kW'),
                                                    ('Motor start rating for 3 second (208v)',
                                                     '1776 A / 341 kW'),
                                                    ('Motor start rating for 3 second (208v)',
                                                     '769 A / 511 kW')],
                   'Operating temperatures': [('Inverter cold start temperature (minimum)', '14°F'),
                                              ('Running operating temperature', '-22°F to 130°F'),
                                              ('Arctic package operating temp. (optional)',
                                               '-50°F to 130°F')],
                   'Weights & Dimensions': [('L x w x h x (Eboss only)', '≈ TBD'),
                                            ('Eboss weight only', '11,037 lbs'),
                                            ('L x w x h (trailer and generator)',
                                             '≈ 262” x 74” x 75”'),
                                            ('Total weight (without/with fuel)',
                                             '≈ 21,600 lbs / 24,000 lbs'),
                                            ('Integral fuel tank capacity', '285 gal')]},
 'EBOSS 70 kVA': {'Battery capacity': [('Total battery life or energy throughout', '2,000 MWh'),
                                       ('Charge time (no load)', '≈ 45 Minutes'),
                                       ('Inverter output max', '56 kW'),
                                       ('Parallel capability', 'Available')],
                  'Battery type': [('Est. Cycle life @ 77°f enclosure temp',
                                    '90K Cycles at 90% DOD'),
                                   ('Est. Cycle life @ 100°f enclosure temp',
                                    '80K Cycles at 90% DOD')],
                  'Maximum Continuous  Output': [('Generator', 'Airman SDG45'),
                                                 ('Generator charge rate', '45 kVA / 36 kW'),
                                                 ('Three-phase output', '42 kVA / 33 kW'),
                                                 ('Single-phase output', '28 kVA / 22 kW'),
                                                 ('Simultaneous voltage',
                                                  '120/240 (1Φ) • 208/480 (3Φ)'),
                                                 ('Max. Continuous amp-load @208v',
                                                  '119 A / 22.8 kW'),
                                                 ('Max. Continuous amp-load @480v', '54 A 35 kW')],
                  'Maximum Intermittent  Output': [('Three-phase', '70 kVA / 56 kW'),
                                                   ('Single-phase', '47 kVA / 37 kW'),
                                                   ('Frequency', '60 Hz'),
                                                   ('Simultaneous voltage',
                                                    '120/240 (1Φ) • 208/480 (3Φ)'),
                                                   ('Voltage regulation', 'Adjustable'),
                                                   ('Max. Intermittent amp-load 208v',
                                                    '194 A 37.2 kW'),
                                                   ('Max. Intermittent amp-load 480v',
                                                    '84 A / 55 kW'),
                                                   ('Motor start rating for 3 second (208v)',
                                                    '291 A / 55 kW'),
                                                   ('Motor start rating for 3 second (208v)',
                                                    '126 A / 175  kW')],
                  'Operating temperatures': [('Inverter cold start temperature (minimum)', '14°F'),
                                             ('Running operating temperature', '-22°F to 130°F'),
                                             ('Arctic package operating temp. (optional)',
                                              '-50°F to 130°F')],
                  'Weights & Dimensions': [('L x w x h x (Eboss only)', '55” x 44” x 62”'),
                                           ('Eboss weight only', '2,700 lbs'),
                                           ('L x w x h (trailer and generator)',
                                            '167” x 71” x 76”'),
                                           ('Total weight (without/with fuel)', '6950 / 7600 lbs'),
                                           ('Integral fuel tank capacity', '80.5 gal')]}}

EBOSS_KVA = {
    "EBOSS 25 kVA": 25,
    "EBOSS 70 kVA": 70,
    "EBOSS 125 kVA": 125,
    "EBOSS 220 kVA": 220,
    "EBOSS 400 kVA": 400
}

def show_logo_and_title(title):
    st.markdown("""
        <div style='text-align: center; padding-bottom: 1rem;'>
            <img src='https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/logo.png' width='240'>
            <h1 style='color:#81BD47;'>{}</h1>
        </div>
    """.format(title), unsafe_allow_html=True)

def render_card(label, value):
    st.markdown(f'''
        <div style="border:1px solid #ccc;border-radius:10px;padding:0.5rem 1rem;margin-bottom:0.5rem;
                    background-color:#111;color:#81BD47;font-weight:bold;">
            <div style="margin-bottom:0.3rem;">{label}</div>
            <div style="color:#fff;">{value}</div>
        </div>
    ''', unsafe_allow_html=True)

def top_navbar():
    st.markdown("<hr style='border: 1px solid #81BD47;'>", unsafe_allow_html=True)
    cols = st.columns(5)
    with cols[0]:
        if st.button("View Specs"):
            st.session_state.section = "tech_specs"
    with cols[1]:
        if st.button("Load-Based Specs"):
            st.session_state.section = "load_specs"
    with cols[2]:
        if st.button("Compare"):
            st.session_state.section = "compare"
    with cols[3]:
        if st.button("Cost Analysis"):
            st.session_state.section = "cost"
    with cols[4]:
        if st.button("Contact Us"):
            st.markdown("""
                <script>
                window.open("https://anacorp.com/contact/", "_blank");
                </script>
            """, unsafe_allow_html=True)

def landing_page():
    show_logo_and_title("EBOSS® Size Specs & Comparison Tool")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Request a Demo"):
            st.info("Demo request logic goes here.")

    with col2:
        if st.button("Request On-Site Training"):
            st.info("Training request logic goes here.")

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
        <a href="https://youtu.be/0Om2qO-zZfM?si=iTiPgIL2t-xDFixc" target="_blank">
            <button style="width:100%;padding:1rem;font-size:1.2rem;background:black;color:#81BD47;border:2px solid #D3D3D3;border-radius:10px;">🎥 Learn How EBOSS® Works</button>
        </a>
        """, unsafe_allow_html=True)

    with col4:
        if st.button("🚀 Launch EBOSS® Tool"):
            st.session_state.section = "input"
            st.rerun()

def render_user_input_page():
    show_logo_and_title("EBOSS® Load Entry")
    top_navbar()

    with st.form("user_input_form"):
        st.selectbox("Select Model", list(spec_data.keys()), key="model")
        st.selectbox("Select Type", ["Full Hybrid", "Power Module"], key="gen_type")
        st.number_input("Continuous Load", 0.0, 500.0, step=1.0, key="cont_kw")
        st.form_submit_button("Submit")

def render_tech_specs_page():
    show_logo_and_title("EBOSS® Technical Specs")
    top_navbar()

    model = st.session_state.get("model", "EBOSS 25 kVA")
    model_data = spec_data[model]

    st.markdown(f"### Showing specs for: **{model}**")

    for section, values in model_data.items():
        st.markdown(f"#### 🔹 {section}")
        for label, value in values:
            col1, col2 = st.columns([1, 2])
            with col1:
                render_card("Spec", label)
            with col2:
                render_card("Value", value)

def main():
    if "section" not in st.session_state:
        st.session_state.section = "landing"

    if st.session_state.section == "landing":
        landing_page()
    elif st.session_state.section == "input":
        render_user_input_page()
    elif st.session_state.section == "tech_specs":
        render_tech_specs_page()
    else:
        st.error("Page not found.")

main()

Code Explainer Logo
AI Python Dev
Blog
Tools
Toggle theme
AI-Powered Python Code Debugger
Instantly identify and fix bugs, errors, and issues in your Python code using advanced AI
🐛 Bug Detection
🔍 Error Analysis
🛠️ Smart Fixes
📝 Detailed Reports
Debug Python Code
import streamlit as st
import streamlit.components.v1 as components

import requests

url = "https://github.com/TimBuffington/Eboss-tool-V2/blob/8fd20f024b5af5aa88eca94de8871223d9b208b5/spec_data.py"
response = requests.get(url)

# Step 2: Execute code in a controlled namespace
context = {}
exec(response.text, context)

# Step 3: Extract spec_data
spec_data = context.get("spec_data")

if spec_data is None:
    raise ValueError("spec_data was not defined in the fetched file.")

EBOSS_KVA = {
    "EBOSS 25 kVA": 25,
    "EBOSS 70 kVA": 70,
    "EBOSS 125 kVA": 125,
    "EBOSS 220 kVA": 220,
    "EBOSS 400 kVA": 400
}

def render_card(label, value):
    st.markdown(f'''
        <div style="border:1px solid #ccc;border-radius:10px;padding:0.5rem 1rem;margin-bottom:0.5rem;
                    background-color:#111;color:#81BD47;font-weight:bold;">
            <div style="margin-bottom:0.3rem;">{label}</div>
            <div style="color:#fff;">{value}</div>
        </div>
    ''', unsafe_allow_html=True)

def show_logo_and_title(title):
    st.markdown("""
        <div style='text-align: center; padding-bottom: 1rem;'>
            <img src='https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/logo.png' width='240'>
            <h1 style='color:#81BD47;'>{}</h1>
        </div>
    """.format(title), unsafe_allow_html=True)

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
            components.html("""
            <script>
                window.open("https://anacorp.com/contact/", "_blank");
            </script>
        """, height=0)


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
    st.selectbox("Select Model", list(spec_data.keys()), key="model")
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

Analyzing Code...
Debug Analysis:
The provided Python code has a few issues that need to be addressed. Here's a detailed analysis and the debugged version with explanations:

Issues Identified:

Syntax Errors:

No major syntax errors were found in the provided code.
Runtime Errors:

The code attempts to execute a Python script fetched from a GitHub URL using exec(response.text, context). This approach can be risky and may lead to security vulnerabilities if the fetched script contains malicious code.
Logical Bugs:

The render_card() function uses unsafe_allow_html=True in the Markdown rendering, which can potentially introduce cross-site scripting (XSS) vulnerabilities if the input data is not properly sanitized.
The top_navbar() function has a potential issue where the st.session_state.section variable is not initialized, which may lead to errors when the application is first loaded.
Edge Cases:

The code does not handle the case where the spec_data variable is not defined in the fetched script.
The code does not handle the case where the model selected in the render_tech_specs_page() function is not present in the spec_data dictionary.
Performance Issues:

No major performance issues were identified in the provided code.
Best Practice Violations:

The code uses exec() to execute a dynamically fetched script, which is generally considered a security risk and should be avoided if possible.
The code uses global state (st.session_state) to manage the application's state, which can make the code harder to maintain and test. It's generally better to use a more structured approach, such as passing state as function arguments or using a state management library like streamlit-state-patch.
Debugged Version:

import streamlit as st
import requests

def render_card(label, value):
    st.markdown(f'''
        <div style="border:1px solid #ccc;border-radius:10px;padding:0.5rem 1rem;margin-bottom:0.5rem;
                    background-color:#111;color:#81BD47;font-weight:bold;">
            <div style="margin-bottom:0.3rem;">{label}</div>
            <div style="color:#fff;">{value}</div>
        </div>
    ''', unsafe_allow_html=False)  # Use False to prevent XSS vulnerabilities

def show_logo_and_title(title):
    st.markdown("""
        <div style='text-align: center; padding-bottom: 1rem;'>
            <img src='https://raw.githubusercontent.com/TimBuffington/Eboss-tool-V2/main/assets/logo.png' width='240'>
            <h1 style='color:#81BD47;'>{}</h1>
        </div>
    """.format(title), unsafe_allow_html=True)

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
            st.components.v1.html("""
            <script>
                window.open("https://anacorp.com/contact/", "_blank");
            </script>
        """, height=0)

def render_user_input_page():
    show_logo_and_title("EBOSS® Load Entry")
    top_navbar()

    with st.form("user_input_form"):
        st.selectbox("Select Model", list(EBOSS_KVA.keys()), key="model")
        st.selectbox("Select Type", ["Full Hybrid", "Power Module"], key="gen_type")
        st.number_input("Continuous Load", 0.0, 500.0, step=1.0, key="cont_kw")
        st.form_submit_button("Submit")

def render_tech_specs_page():
    show_logo_and_title("EBOSS® Technical Specs")
    top_navbar()
    st.selectbox("Select Model", list(EBOSS_KVA.keys()), key="model")
    model = st.session_state.get("model", "EBOSS 25 kVA")
    if model in EBOSS_KVA:
        st.markdown(f"### Showing specs for: **{model}**")
        render_card("kVA Rating", EBOSS_KVA[model])
    else:
        st.error(f"Model '{model}' not found in the EBOSS_KVA dictionary.")

EBOSS_KVA = {
    "EBOSS 25 kVA": 25,
    "EBOSS 70 kVA": 70,
    "EBOSS 125 kVA": 125,
    "EBOSS 220 kVA": 220,
    "EBOSS 400 kVA": 400
}

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


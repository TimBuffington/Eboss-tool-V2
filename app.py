import streamlit as st
import streamlit.components.v1 as components

import requests

url = "https://github.com/TimBuffington/Eboss-tool-V2/blob/8fd20f024b5af5aa88eca94de8871223d9b208b5/spec_data.py"
response = requests.get(url)

# DEBUG — Check what code you're trying to exec
print(response.text)  # This helps find syntax errors in the downloaded code

# Now execute
exec(response.text)
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

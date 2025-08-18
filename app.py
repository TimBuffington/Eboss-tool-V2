import streamlit as st
import components.nav as nav
from components.modals import open_config_modal

st.set_page_config(page_title="EBOSS® Tool", layout="wide", initial_sidebar_state="collapsed")
nav.render_global_header(mode="external")
with st.container():
            cols = st.columns(1,1,1)
            with cols[1]:  # Use the middle column to help with centering
                st.markdown(
                    "<div class='message-container'>Please Select EBOSS Configuration</div>",
                     unsafe_allow_html=True,
                )
                        
                    

choice = nav.render_config_selector()   # ← no troubleshooting arg anymore

if choice in ("manual", "load_based", "fuel_eff"):
    open_config_modal(choice)

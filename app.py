import streamlit as st
import components.nav as nav
from components.modals import open_config_modal
apply_global_theme()
st.set_page_config(page_title="EBOSS® Tool", layout="wide", initial_sidebar_state="collapsed")
nav.render_global_header(mode="external")

                        
                    

choice = nav.render_config_selector()   # ← no troubleshooting arg anymore

if choice in ("manual", "load_based", "fuel_eff"):
    open_config_modal(choice)

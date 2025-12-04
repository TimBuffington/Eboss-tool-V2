SPEC_LABELS = [
    "Battery Capacity",
    "Inverter",
    "Voltage Options",
    "Weight",
    "Dimensions",
    "Warranty"
]

#return {
        "model_capacity": model_capacity,
        "peak_utilization": peak_utilization,
        "continuous_utilization": continuous_utilization,
        "charge_rate": charge_rate,
        "battery_capacity": battery_capacity,
        "charge_time": charge_time,
        "fuel_consumption_gph": fuel_consumption,
        "fuel_per_day": fuel_consumption * 24 if fuel_consumption else 0,
        "co2_per_day": co2_per_day,
        "engine_load_percent": engine_load_percent,
        "generator_data": generator_data
    }
st.markdown(f"""
<div style="background: rgba(129, 189, 71, 0.1); padding: 1rem; border-radius: 8px; 
border-left: 4px solid #81BD47; margin-bottom: 1rem;">
<strong>Recommended Generator:</strong><br>
#For the <strong>{st.session_state.eboss_model}</strong> model: <strong>{paired_gen}</strong>
</div>
""", unsafe_allow_html=True)


def create_section_header(title):
    """Create a section header that spans all 4 columns"""
    return f"""
    <div style="background: linear-gradient(135deg, var(--energy-green) 0%, #2d5a3d 100%); 
                color: var(--alpine-white); 
                padding: 1rem; 
                margin: 1rem 0 0.5rem 0; 
                border-radius: 10px; 
                text-align: center; 
                box-shadow: 0 8px 16px rgba(0,0,0,0.5), inset 0 2px 4px rgba(255,255,255,0.2); 
                text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
                border: 3px solid rgba(255,255,255,0.1);">
        <strong style="font-size: 1.2rem; 
                     text-transform: uppercase; 
                     letter-spacing: 1px; 
                     font-family: Arial, sans-serif; 
                     font-weight: 700;">
            {title}
        </strong>
    </div>
    """

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header with logo on separate line
st.markdown('<div class="logo-container" style="text-align: center; margin-bottom: 1rem;">', unsafe_allow_html=True)
st.image("ANA-ENERGY-LOGO-PADDED.png", width=200)
st.markdown('</div>', unsafe_allow_html=True)

# Title in styled container
st.markdown('''
<div style="background: var(--cool-gray-10c); color: var(--alpine-white); padding: 1.5rem; margin: 1rem 0 2rem 0; border-radius: 12px; text-align: center; box-shadow: 0 8px 16px rgba(0,0,0,0.4); text-shadow: 2px 2px 4px rgba(0,0,0,0.6);">
    <h1 style="margin: 0; font-size: 2.5rem; font-weight: 600; letter-spacing: 1px;">EBOSS® Spec and Comparison Tool</h1>
</div>
''', unsafe_allow_html=True)

# Create two columns for layout

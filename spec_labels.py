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

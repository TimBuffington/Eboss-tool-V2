def Cost_Analysis():
    
    if st.session_state.show_cost_analysis and st.session_state.eboss_model:
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
 
    
    # Get input values from session state with defaults
    local_fuel_price = st.session_state.get('local_fuel_price', 3.50)
    fuel_delivery_fee = st.session_state.get('fuel_delivery_fee', 0.0)
    pm_interval_hrs = st.session_state.get('pm_interval_hrs', 500)
    cost_per_pm = st.session_state.get('cost_per_pm', 0.0) if st.session_state.get('pm_charge_radio') == "Yes" else 0.0
    eboss_weekly_rate = st.session_state.get('eboss_weekly_rate', 0.0)
    eboss_monthly_rate = st.session_state.get('eboss_monthly_rate', 0.0)
    standard_weekly_rate = st.session_state.get('standard_weekly_rate', 0.0)
    standard_monthly_rate = st.session_state.get('standard_monthly_rate', 0.0)
    selected_standard_gen = st.session_state.get('cost_standard_generator', 'N/A')
    
    # Calculate fuel consumption and costs based on load data
    continuous_load = st.session_state.get('continuous_load', 0)
    
    # Get EBOSS® fuel data (from load specs calculations)
    eboss_model = st.session_state.eboss_model
    battery_capacity_kwh = EBOSS_LOAD_REFERENCE["battery_capacities"].get(eboss_model, 0)
    
    # EBOSS® calculations
    if st.session_state.eboss_type == "Full Hybrid":
        generator_kva = EBOSS_LOAD_REFERENCE["generator_kva_hybrid"].get(eboss_model, 0)
    else:
        generator_kva = int(st.session_state.generator_kva.replace('kVA', '')) if st.session_state.generator_kva else 0
    
    generator_kw = generator_kva * 0.8
    charge_rate_kw = EBOSS_LOAD_REFERENCE["generator_sizes"].get(generator_kva, {}).get("fh_charge_rate" if st.session_state.eboss_type == "Full Hybrid" else "pm_charge_rate", 0)
    
    # Calculate EBOSS® fuel consumption
    battery_longevity = (battery_capacity_kwh / continuous_load) if continuous_load > 0 else 0
    charge_time = (battery_capacity_kwh / charge_rate_kw) if charge_rate_kw > 0 else 0
    charges_per_day = 24 / (charge_time + battery_longevity) if (charge_time + battery_longevity) > 0 else 0
    engine_load_percent = (charge_rate_kw / generator_kw * 100) if generator_kw > 0 else 0
    
    # Get authentic GPH data
    def interpolate_gph(generator_kva, load_percent):
        if generator_kva not in EBOSS_LOAD_REFERENCE["gph_interpolation"]:
            return 0
        gph_data = EBOSS_LOAD_REFERENCE["gph_interpolation"][generator_kva]
        if load_percent <= 25: return gph_data["25%"]
        elif load_percent <= 50: return gph_data["50%"]
        elif load_percent <= 75: return gph_data["75%"]
        else: return gph_data["100%"]
    
    eboss_fuel_per_hour = interpolate_gph(generator_kva, engine_load_percent) if engine_load_percent > 0 else 0
    eboss_runtime_per_day = charges_per_day * charge_time if charges_per_day > 0 and charge_time > 0 else 0
    
    # Standard generator calculations
    standard_specs = STANDARD_GENERATOR_DATA.get(selected_standard_gen, {})
    standard_fuel_gph = standard_specs.get('fuel_consumption_gph', {}).get('50%', 0)  # Use 50% load as baseline
    standard_runtime_per_day = 24  # Assume continuous operation
    
    # Cost calculations
    def calculate_costs(fuel_per_hour, runtime_per_day, rental_weekly, rental_monthly):
        # Weekly calculations
        weekly_fuel_gal = fuel_per_hour * runtime_per_day * 7
        weekly_fuel_cost = weekly_fuel_gal * local_fuel_price
        weekly_pm_cost = (runtime_per_day * 7 / pm_interval_hrs) * cost_per_pm if pm_interval_hrs > 0 else 0
        weekly_total = rental_weekly + weekly_fuel_cost + fuel_delivery_fee + weekly_pm_cost
        
        # Monthly calculations (30 days)
        monthly_fuel_gal = fuel_per_hour * runtime_per_day * 30
        monthly_fuel_cost = monthly_fuel_gal * local_fuel_price
        monthly_pm_cost = (runtime_per_day * 30 / pm_interval_hrs) * cost_per_pm if pm_interval_hrs > 0 else 0
        monthly_total = rental_monthly + monthly_fuel_cost + (fuel_delivery_fee * 4.3) + monthly_pm_cost  # 4.3 weeks per month
        
        return {
            'weekly': {
                'rental': rental_weekly,
                'runtime_hours': runtime_per_day * 7,
                'pm_services': runtime_per_day * 7 / pm_interval_hrs if pm_interval_hrs > 0 else 0,
                'pm_cost': weekly_pm_cost,
                'diesel_qty': weekly_fuel_gal,
                'diesel_cost': weekly_fuel_cost,
                'fuel_delivery': fuel_delivery_fee,
                'total': weekly_total
            },
            'monthly': {
                'rental': rental_monthly,
                'runtime_hours': runtime_per_day * 30,
                'pm_services': runtime_per_day * 30 / pm_interval_hrs if pm_interval_hrs > 0 else 0,
                'pm_cost': monthly_pm_cost,
                'diesel_qty': monthly_fuel_gal,
                'diesel_cost': monthly_fuel_cost,
                'fuel_delivery': fuel_delivery_fee * 4.3,
                'total': monthly_total
            }
        }
    
    # Debug information (temporary)
    st.write(f"Debug - EBOSS® Model: {eboss_model}")
    st.write(f"Debug - Continuous Load: {continuous_load}")
    st.write(f"Debug - Generator kVA: {generator_kva}")
    st.write(f"Debug - Battery Capacity: {battery_capacity_kwh}")
    st.write(f"Debug - Charge Rate kW: {charge_rate_kw}")
    st.write(f"Debug - Engine Load %: {engine_load_percent}")
    st.write(f"Debug - EBOSS® Fuel GPH: {eboss_fuel_per_hour}")
    st.write(f"Debug - Standard Generator: {selected_standard_gen}")
    st.write(f"Debug - Standard Fuel GPH: {standard_fuel_gph}")
    
    # Calculate costs for both systems
    eboss_costs = calculate_costs(eboss_fuel_per_hour, eboss_runtime_per_day, eboss_weekly_rate, eboss_monthly_rate)
    standard_costs = calculate_costs(standard_fuel_gph, standard_runtime_per_day, standard_weekly_rate, standard_monthly_rate)
    
    # Display the cost analysis table
    st.markdown('<br>', unsafe_allow_html=True)
    
    # Create the table structure using HTML
    st.markdown(f"""
    <div style="background: var(--alpine-white); padding: 1rem; border-radius: 8px; margin: 1rem 0; 
                box-shadow: 0 8px 16px rgba(0,0,0,0.3); border: 2px solid var(--charcoal);">
        <table style="width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; font-size: 0.9rem; 
                      box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            <thead>
                <tr style="background: var(--energy-green); color: var(--alpine-white); 
                          border: 2px solid var(--charcoal); box-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                    <th style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: left; font-weight: bold; 
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">Item</th>
                    <th colspan="2" style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: center; font-weight: bold;
                                         text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">Weekly</th>
                    <th colspan="2" style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: center; font-weight: bold;
                                         text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">Monthly</th>
                </tr>
                <tr style="background: var(--energy-green); color: var(--alpine-white); 
                          border: 2px solid var(--charcoal); box-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                    <th style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: left; font-size: 0.8rem;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.7);"></th>
                    <th style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: center; font-size: 0.8rem;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.7);">EBOSS® Hybrid</th>
                    <th style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: center; font-size: 0.8rem;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.7);">Standard Generator</th>
                    <th style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: center; font-size: 0.8rem;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.7);">EBOSS® Hybrid</th>
                    <th style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: center; font-size: 0.8rem;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.7);">Standard Generator</th>
                </tr>
            </thead>
            <tbody style="background: var(--alpine-white); color: var(--black-asphalt);">
                <tr style="box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); font-weight: bold;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">Rental Rate</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${eboss_costs['weekly']['rental']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${standard_costs['weekly']['rental']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${eboss_costs['monthly']['rental']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${standard_costs['monthly']['rental']:,.2f}</td>
                </tr>
                <tr style="background: #f9f9f9; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); font-weight: bold;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">Runtime Hours</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{eboss_costs['weekly']['runtime_hours']:.1f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{standard_costs['weekly']['runtime_hours']:.1f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{eboss_costs['monthly']['runtime_hours']:.1f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{standard_costs['monthly']['runtime_hours']:.1f}</td>
                </tr>
                <tr style="box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); font-weight: bold;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">PM Services</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{eboss_costs['weekly']['pm_services']:.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{standard_costs['weekly']['pm_services']:.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{eboss_costs['monthly']['pm_services']:.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{standard_costs['monthly']['pm_services']:.2f}</td>
                </tr>
                <tr style="background: #f9f9f9; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); font-weight: bold;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">PM Service Cost</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${eboss_costs['weekly']['pm_cost']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${standard_costs['weekly']['pm_cost']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${eboss_costs['monthly']['pm_cost']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${standard_costs['monthly']['pm_cost']:,.2f}</td>
                </tr>
                <tr style="box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); font-weight: bold;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">Diesel Qty (gal)</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{eboss_costs['weekly']['diesel_qty']:.1f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{standard_costs['weekly']['diesel_qty']:.1f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{eboss_costs['monthly']['diesel_qty']:.1f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{standard_costs['monthly']['diesel_qty']:.1f}</td>
                </tr>
                <tr style="background: #f9f9f9; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); font-weight: bold;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">Diesel Cost</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${eboss_costs['weekly']['diesel_cost']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${standard_costs['weekly']['diesel_cost']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${eboss_costs['monthly']['diesel_cost']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${standard_costs['monthly']['diesel_cost']:,.2f}</td>
                </tr>
                <tr style="box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); font-weight: bold;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">Fuel Delivery Cost</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${eboss_costs['weekly']['fuel_delivery']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${standard_costs['weekly']['fuel_delivery']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${eboss_costs['monthly']['fuel_delivery']:,.2f}</td>
                    <td style="padding: 0.5rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">${standard_costs['monthly']['fuel_delivery']:,.2f}</td>
                </tr>
                <tr style="background: var(--energy-green); color: var(--alpine-white); font-weight: bold;
                          border: 2px solid var(--charcoal); box-shadow: 0 4px 8px rgba(0,0,0,0.4);">
                    <td style="padding: 0.75rem; border: 1px solid var(--charcoal); font-weight: bold;
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">Total Cost</td>
                    <td style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">${eboss_costs['weekly']['total']:,.2f}</td>
                    <td style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">${standard_costs['weekly']['total']:,.2f}</td>
                    <td style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">${eboss_costs['monthly']['total']:,.2f}</td>
                    <td style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">${standard_costs['monthly']['total']:,.2f}</td>
                </tr>
                <tr style="background: var(--energy-green); color: var(--alpine-white); font-weight: bold;
                          border: 2px solid var(--charcoal); box-shadow: 0 4px 8px rgba(0,0,0,0.4);">
                    <td style="padding: 0.75rem; border: 1px solid var(--charcoal); font-weight: bold;
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">EBOSS® Savings</td>
                    <td style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">${(standard_costs['weekly']['total'] - eboss_costs['weekly']['total']):,.2f}</td>
                    <td style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">-</td>
                    <td style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">${(standard_costs['monthly']['total'] - eboss_costs['monthly']['total']):,.2f}</td>
                    <td style="padding: 0.75rem; border: 1px solid var(--charcoal); text-align: right;
                              text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">-</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    # Cost savings summary
    weekly_savings = standard_costs['weekly']['total'] - eboss_costs['weekly']['total']
    monthly_savings = standard_costs['monthly']['total'] - eboss_costs['monthly']['total']
    yearly_savings = monthly_savings * 12  # Calculate yearly savings
    
    savings_color = "var(--energy-green)" if weekly_savings > 0 else "#FF6B6B"
    savings_text = "SAVINGS" if weekly_savings > 0 else "ADDITIONAL COST"
    
    st.markdown(f"""
    <div style="background: {savings_color}; color: white; padding: 1rem; border-radius: 8px; margin: 1rem 0; 
                text-align: center; font-weight: bold; border: 2px solid var(--charcoal); 
                box-shadow: 0 6px 12px rgba(0,0,0,0.4);">
        <h4 style="margin: 0; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">EBOSS® {savings_text}</h4>
        <p style="margin: 0.5rem 0; font-size: 1.1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">
            Weekly: ${abs(weekly_savings):,.2f} | Monthly: ${abs(monthly_savings):,.2f} | Yearly: ${abs(yearly_savings):,.2f}
        </p>
    </div>
    """, unsafe_allow_html=True)
    

    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<br><br>', unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align: center; color: var(--cool-gray-8c); font-size: 0.9rem; padding: 1rem;">
    EBOSS® Model Selection Tool | Powered by Advanced Energy Solutions
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

















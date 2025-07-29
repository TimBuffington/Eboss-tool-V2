import streamlit as st

# 1. Styling
def apply_custom_css():
    st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("app://./AdobeStock_209254754.jpeg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .form-container {{
            background: rgba(0,0,0,0.75);
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            color: #fff;
        }}
        .form-section-title {{
            font-size: 1.3rem;
            font-weight: bold;
            color: #81BD47;
            margin-bottom: 1rem;
        }}
        .info-box {{
            background-color: #81BD47;
            padding: 0.8rem;
            margin: 1rem 0;
            border-radius: 8px;
            color: #fff;
        }}
        .warning-box {{
            background-color: #FF6B6B;
            padding: 0.8rem;
            margin: 1rem 0;
            border-radius: 8px;
            color: #fff;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 0.5rem;
            border-bottom: 1px solid #444;
        }}
        th {{
            color: #81BD47;
        }}
    </style>
    """, unsafe_allow_html=True)

# 2. EBOSS Reference Data
EBOSS_KVA = {
    "EB25 kVA": 25,
    "EB70 kVA": 45,
    "EB125 kVA": 65,
    "EB220 kVA": 125,
    "EB400 kVA": 220
}
STANDARD_GENERATORS = {
    "25 kVA / 20 kW": 1.8,
    "45 kVA / 36 kW": 2.7,
    "65 kVA / 52 kW": 3.5,
    "125 kVA / 100 kW": 6.5,
    "220 kVA / 176 kW": 12.5
}

# 3. Render cost table
def render_cost_comparison(eboss_model, eboss_gen_size, std_gen_label, fuel_price, delivery_fee, pm_interval, pm_cost, eboss_monthly, std_monthly, eboss_runtime, std_runtime, eboss_gph, std_gph):
    eboss_gal = eboss_gph * eboss_runtime
    std_gal = std_gph * std_runtime
    eboss_fuel_cost = eboss_gal * fuel_price
    std_fuel_cost = std_gal * fuel_price
    eboss_pms = eboss_runtime / pm_interval if pm_interval else 0
    std_pms = std_runtime / pm_interval if pm_interval else 0
    eboss_pm_total = eboss_pms * pm_cost
    std_pm_total = std_pms * pm_cost
    eboss_co2 = eboss_gal * 22.4
    std_co2 = std_gal * 22.4
    eboss_total = eboss_monthly + eboss_fuel_cost + delivery_fee + eboss_pm_total
    std_total = std_monthly + std_fuel_cost + delivery_fee + std_pm_total
    diff = std_total - eboss_total

    rows = [
        ("Generator Size", eboss_gen_size, std_gen_label, ""),
        ("Rental Cost ($)", eboss_monthly, std_monthly, std_monthly - eboss_monthly),
        ("Fuel Used (gal)", eboss_gal, std_gal, std_gal - eboss_gal),
        ("Fuel Cost ($)", eboss_fuel_cost, std_fuel_cost, std_fuel_cost - eboss_fuel_cost),
        ("PM Services", eboss_pms, std_pms, std_pms - eboss_pms),
        ("PM Cost ($)", eboss_pm_total, std_pm_total, std_pm_total - eboss_pm_total),
        ("CO₂ Emissions (lbs)", eboss_co2, std_co2, std_co2 - eboss_co2),
        ("Delivery Fee ($)", delivery_fee, delivery_fee, 0),
        ("Total Monthly Cost ($)", eboss_total, std_total, diff)
    ]

    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown(f"<h3 class='form-section-title'>📊 Monthly Cost Comparison</h3>", unsafe_allow_html=True)
    st.markdown(f"""
    <table>
        <thead>
            <tr>
                <th>Metric</th>
                <th>EBOSS® Model<br>{eboss_model}</th>
                <th>Standard Generator<br>{std_gen_label}</th>
                <th>Difference</th>
            </tr>
        </thead>
        <tbody>
    """, unsafe_allow_html=True)

    for label, e_val, s_val, d_val in rows:
        def fmt(x): return f"{x:,.2f}" if isinstance(x, (int, float)) else x
        st.markdown(f"""
            <tr>
                <td>{label}</td>
                <td>{fmt(e_val)}</td>
                <td>{fmt(s_val)}</td>
                <td><strong>{fmt(d_val)}</strong></td>
            </tr>
        """, unsafe_allow_html=True)
    st.markdown("</tbody></table></div>", unsafe_allow_html=True)

# 🏁 Start App
apply_custom_css()
st.markdown("<h1 style='text-align:center;'>EBOSS® Model Selection Tool</h1>", unsafe_allow_html=True)

# Step 1: EBOSS config
st.markdown('<div class="form-container">', unsafe_allow_html=True)
st.markdown('<h3 class="form-section-title">⚙️ System Configuration</h3>', unsafe_allow_html=True)
model = st.selectbox("EBOSS® Model", list(EBOSS_KVA.keys()))
gen_type = st.selectbox("EBOSS® Type", ["Full Hybrid", "Power Module"])
cont_kw = st.number_input("Continuous Load (kW)", min_value=0.0, max_value=500.0, step=1.0)
peak_kw = st.number_input("Peak Load (kW)", min_value=0.0, max_value=500.0, step=1.0)
st.markdown('</div>', unsafe_allow_html=True)

# Validate
if cont_kw > peak_kw > 0:
    st.markdown("<div class='warning-box'>⚠️ Continuous load cannot exceed peak load.</div>", unsafe_allow_html=True)

# Step 2: Trigger cost analysis input
if st.button("📊 Run Cost Analysis"):
    st.session_state["show_cost"] = True

# Step 3: Cost Input Section
if st.session_state.get("show_cost", False):
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="form-section-title">💰 Cost Inputs</h3>', unsafe_allow_html=True)

    fuel_price = st.number_input("Fuel Price ($/gal)", 0.0, 100.0, 3.50, 0.01)
    delivery_fee = st.number_input("Delivery Fee ($)", 0.0, 500.0, 75.0, 1.0)
    pm_interval = st.number_input("PM Interval (hours)", 10.0, 1000.0, 500.0, 10.0)
    pm_cost = st.number_input("Cost per PM ($)", 0.0, 5000.0, 150.0, 10.0)
    eboss_monthly = st.number_input("EBOSS® Monthly Rental ($)", 0.0, 100000.0, 3800.0, 50.0)
    std_monthly = st.number_input("Standard Gen Monthly Rental ($)", 0.0, 100000.0, 3500.0, 50.0)
    std_gen = st.selectbox("Standard Generator Size", list(STANDARD_GENERATORS.keys()))
    st.markdown('</div>', unsafe_allow_html=True)

    # Step 4: Run comparison
    if st.button("✅ Compare"):
        # Runtime & GPH assumptions
        eboss_runtime = 300  # hours per month (estimate)
        std_runtime = 720    # 24/7 gen
        eboss_gph = 1.6      # assumed interpolated
        std_gph = STANDARD_GENERATORS[std_gen]

        render_cost_comparison(
            eboss_model=model,
            eboss_generator_label=f"{EBOSS_KVA[model]} kVA / {int(EBOSS_KVA[model]*0.8)} kW",
            standard_generator_label=std_gen,
            fuel_price=fuel_price,
            delivery_fee=delivery_fee,
            pm_interval=pm_interval,
            cost_per_pm=pm_cost,
            eboss_monthly=eboss_monthly,
            standard_monthly=std_monthly,
            eboss_runtime_hours=eboss_runtime,
            standard_runtime_hours=std_runtime,
            eboss_fuel_gph=eboss_gph,
            standard_fuel_gph=std_gph
        )

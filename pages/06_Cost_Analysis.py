import streamlit as st
from utils.theme import apply_theme, render_logo
from utils.state import ensure_state
from utils.sizing import calculate_load_specs
from utils.cost import monthly_costs

apply_theme(); ensure_state(); render_logo()
st.header("Cost Analysis")

ui = st.session_state.user_inputs
eboss_model = ui.get("eboss_model", "EB125 kVA")
eboss_type  = ui.get("eboss_type",  "Full Hybrid")
cont_kw     = float(ui.get("actual_continuous_load", 0.0))
peak_kw     = float(ui.get("actual_peak_load", 0.0))
gen_kva     = ui.get("power_module_gen_size", None)

with st.form("cost_input_form", clear_on_submit=False):
    st.subheader("Enter Cost Inputs")
    rental    = st.number_input("Monthly Rental Rate ($)",  min_value=0.0, step=10.0,  format="%g")
    fuel_cost = st.number_input("Fuel Cost per Gallon ($)", min_value=0.0, step=0.01, format="%g", value=3.50)
    delivery  = st.number_input("Delivery Fee ($)",         min_value=0.0, step=10.0,  format="%g")
    pm_cost   = st.number_input("PM Service Cost ($/mo)",   min_value=0.0, step=10.0,  format="%g")
    days      = st.number_input("Days in Month",            min_value=1, max_value=31, value=30, step=1)
    submit    = st.form_submit_button("Calculate")

if submit:
    specs = calculate_load_specs(eboss_model, eboss_type, cont_kw, peak_kw, gen_kva)
    if "error" in specs:
        st.error(specs["error"])
    else:
        rt_day = specs.get("engine_run_per_day", 0.0)
        gph    = specs.get("fuel_consumption_gph", 0.0)

        if rt_day <= 0 or gph <= 0:
            st.warning("Runtime or fuel burn not available. Configure a model and run sizing first.")
        else:
            res = monthly_costs(rt_day, gph, fuel_cost, rental, delivery, pm_cost, days)
            st.subheader("Monthly Cost Breakdown")
            st.markdown(
                f"""
                <table style='width:100%; border:1px solid #444; border-collapse:collapse;'>
                  <tr><th style='text-align:left;padding:6px;border:1px solid #444;'>Metric</th>
                      <th style='text-align:right;padding:6px;border:1px solid #444;'>Value</th></tr>
                  <tr><td style='padding:6px;border:1px solid #444;'>Rental</td>
                      <td style='text-align:right;padding:6px;border:1px solid #444;'>${rental:,.2f}</td></tr>
                  <tr><td style='padding:6px;border:1px solid #444;'>Fuel</td>
                      <td style='text-align:right;padding:6px;border:1px solid #444;'>${res['fuel_total']:,.2f}</td></tr>
                  <tr><td style='padding:6px;border:1px solid #444;'>Delivery</td>
                      <td style='text-align:right;padding:6px;border:1px solid #444;'>${delivery:,.2f}</td></tr>
                  <tr><td style='padding:6px;border:1px solid #444;'>PM Service</td>
                      <td style='text-align:right;padding:6px;border:1px solid #444;'>${pm_cost:,.2f}</td></tr>
                  <tr><td style='padding:6px;border:1px solid #444;'><strong>Total Monthly</strong></td>
                      <td style='text-align:right;padding:6px;border:1px solid #444;'><strong>${res['total_cost']:,.2f}</strong></td></tr>
                  <tr><td style='padding:6px;border:1px solid #444;'>Est. CO₂ Emissions (tons)</td>
                      <td style='text-align:right;padding:6px;border:1px solid #444;'>{res['co2_tons']:,.2f}</td></tr>
                  <tr><td style='padding:6px;border:1px solid #444;'>Monthly Runtime (hours)</td>
                      <td style='text-align:right;padding:6px;border:1px solid #444;'>{res['monthly_hours']:,.1f}</td></tr>
                  <tr><td style='padding:6px;border:1px solid #444;'>Fuel Used (gal)</td>
                      <td style='text-align:right;padding:6px;border:1px solid #444;'>{res['gallons']:,.1f}</td></tr>
                </table>
                """,
                unsafe_allow_html=True
            )

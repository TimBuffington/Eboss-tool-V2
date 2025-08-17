def monthly_costs(daily_runtime_hr: float,
                  fuel_gph: float,
                  fuel_cost_per_gal: float,
                  rental: float,
                  delivery: float,
                  pm_cost: float,
                  days_in_month: int):
    monthly_hours = float(daily_runtime_hr) * float(days_in_month)
    gallons = monthly_hours * float(fuel_gph)
    fuel_total = gallons * float(fuel_cost_per_gal)
    total_cost = float(rental) + float(delivery) + float(pm_cost) + fuel_total
    CO2_LB_PER_GAL = 22.4  # diesel approx
    co2_tons = (gallons * CO2_LB_PER_GAL) / 2000.0
    return dict(
        monthly_hours=monthly_hours,
        gallons=gallons,
        fuel_total=fuel_total,
        total_cost=total_cost,
        co2_tons=co2_tons,
    )


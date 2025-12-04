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

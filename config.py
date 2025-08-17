# config.py

SPECS = {
    25:  {"eboss_model": "EB25 kVA",  "pm_charge_rate": 18.5, "fh_charge_rate": 19.5, "max_charge_rate": 20,  "kwh": 15,  "gen_kw": 20,  "max_cont_kw": 18,  "max_peak_kw": 20},
    45:  {"eboss_model": "EB70 kVA",  "pm_charge_rate": 33.0, "fh_charge_rate": 36.0, "max_charge_rate": 45,  "kwh": 25,  "gen_kw": 36,  "max_cont_kw": 40,  "max_peak_kw": 56},
    65:  {"eboss_model": "EB125 kVA", "pm_charge_rate": 48.0, "fh_charge_rate": 52.0, "max_charge_rate": 65,  "kwh": 50,  "gen_kw": 52,  "max_cont_kw": 58,  "max_peak_kw": 125},
    125: {"eboss_model": "EB220 kVA", "pm_charge_rate": 96.0, "fh_charge_rate": 100.0,"max_charge_rate": 125, "kwh": 75,  "gen_kw": 100, "max_cont_kw": 112, "max_peak_kw": 252},
    220: {"eboss_model": "EB400 kVA", "pm_charge_rate": 166.0,"fh_charge_rate": 176.0,"max_charge_rate": 220, "kwh": 125, "gen_kw": 176, "max_cont_kw": 198, "max_peak_kw": 639},
}

    },
    "gph_interpolation": {
        25: {"25%": 0.67, "50%": 0.94, "75%": 1.26, "100%": 1.62},
        45: {"25%": 1.04, "50%": 1.60, "75%": 2.20, "100%": 2.03},
        70: {"25%": 1.70, "50%": 2.60, "75%": 3.50, "100%": 4.40},
        125: {"25%": 2.60, "50%": 4.10, "75%": 5.60, "100%": 7.10},
        220: {"25%": 4.60, "50%": 6.90, "75%": 9.40, "100%": 12.00},
        400: {"25%": 7.70, "50%": 12.20, "75%": 17.30, "100%": 22.50}
    }
}

STANDARD_GENERATOR_DATA = {
    "25 kVA / 20 kW": {
        "kw": 20,
        "fuel_consumption_gph": {"50%": 1.2, "75%": 1.7, "100%": 2.3},
        "fuel_tank_gal": 38,
        "co2_per_gal": 22.4,
        "noise_level_db": 75,
        "dimensions": "60\" x 24\" x 36\"",
        "weight_lbs": 1850
    },
    "45 kVA / 36 kW": {
        "kw": 36,
        "fuel_consumption_gph": {"50%": 2.1, "75%": 3.0, "100%": 4.1},
        "fuel_tank_gal": 60,
        "co2_per_gal": 22.4,
        "noise_level_db": 78,
        "dimensions": "72\" x 30\" x 42\"",
        "weight_lbs": 2850
    },
    "65 kVA / 52 kW": {
        "kw": 52,
        "fuel_consumption_gph": {"50%": 2.8, "75%": 4.2, "100%": 5.8},
        "fuel_tank_gal": 80,
        "co2_per_gal": 22.4,
        "noise_level_db": 80,
        "dimensions": "84\" x 36\" x 48\"",
        "weight_lbs": 4200
    },
    "125 kVA / 100 kW": {
        "kw": 100,
        "fuel_consumption_gph": {"50%": 5.2, "75%": 7.8, "100%": 10.5},
        "fuel_tank_gal": 120,
        "co2_per_gal": 22.4,
        "noise_level_db": 82,
        "dimensions": "120\" x 48\" x 60\"",
        "weight_lbs": 8500
    },
    "220 kVA / 176 kW": {
        "kw": 176,
        "fuel_consumption_gph": {"50%": 9.1, "75%": 13.7, "100%": 18.2},
        "fuel_tank_gal": 200,
        "co2_per_gal": 22.4,
        "noise_level_db": 85,
        "dimensions": "144\" x 60\" x 72\"",
        "weight_lbs": 15000
    },
    "400 kVA / 320 kW": {
        "kw": 320,
        "fuel_consumption_gph": {"50%": 16.8, "75%": 25.2, "100%": 33.6},
        "fuel_tank_gal": 350,
        "co2_per_gal": 22.4,
        "noise_level_db": 88,
        "dimensions": "180\" x 72\" x 84\"",
        "weight_lbs": 28000
    }
}


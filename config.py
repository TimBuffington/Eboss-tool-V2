# config.py

EBOSS_LOAD_REFERENCE = {
    "battery_capacities": {
        "EB25 kVA": 15,
        "EB70 kVA": 25,
        "EB125 kVA": 50,
        "EB220 kVA": 75,
        "EB400 kVA": 125
    },
    "generator_kva_hybrid": {
        "EB25 kVA": 25,
        "EB70 kVA": 45,
        "EB125 kVA": 65,
        "EB220 kVA": 125,
        "EB400 kVA": 220
    },
    "generator_sizes": {
        25: {"eboss_model": "EB25 kVA", "pm_charge_rate": 18.5, "fh_charge_rate": 19.5, "max_charge_rate": 20, "kwh": 15, "gen_kw": 20},
        45: {"eboss_model": "EB70 kVA", "pm_charge_rate": 33, "fh_charge_rate": 36, "max_charge_rate": 45, "kwh": 25, "gen_kw": 36},
        65: {"eboss_model": "EB125 kVA", "pm_charge_rate": 48, "fh_charge_rate": 52, "max_charge_rate": 65, "kwh": 50, "gen_kw": 52},
        125: {"eboss_model": "EB220 kVA", "pm_charge_rate": 96, "fh_charge_rate": 100, "max_charge_rate_

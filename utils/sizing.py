from utils.data import SPECS

def calculate_load_specs(eboss_model: str, eboss_type: str, cont_kw: float, peak_kw: float, gen_kva=None):
    """
    Return a dict including runtime/fuel burn keys used by Cost Analysis page.
    Replace internals with your real interpolation/logic.
    """
    # Pick a record by eboss_model (e.g., "EB125 kVA")
    rec = next((v for v in SPECS.values() if v["eboss_model"] == eboss_model), None)
    if not rec:
        return {"error": f"Unknown model: {eboss_model}"}

    # Minimal example outputs so pages run:
    # (Replace these with your computed values)
    engine_run_per_day = 6.0              # hours/day (example)
    fuel_consumption_gph = 1.5            # gallons/hour at charge (example)

    return {
        "model": eboss_model,
        "type": eboss_type,
        "max_cont_kw": rec["max_cont_kw"],
        "max_peak_kw": rec["max_peak_kw"],
        "engine_run_per_day": engine_run_per_day,
        "fuel_consumption_gph": fuel_consumption_gph,
    }


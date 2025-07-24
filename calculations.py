# calculations.py

from config import EBOSS_LOAD_REFERENCE

def interpolate_gph(generator_kva, load_percent):
    if load_percent > 1:
        load_percent = load_percent / 100

    gph_map = EBOSS_LOAD_REFERENCE["gph_interpolation"]
    if generator_kva not in gph_map:
        closest = min(gph_map.keys(), key=lambda x: abs(x - generator_kva))
        gph_data = gph_map[closest]
    else:
        gph_data = gph_map[generator_kva]

    points = [0.25, 0.50, 0.75, 1.00]
    values = [gph_data["25%"], gph_data["50%"], gph_data["75%"], gph_data["100%"]]
    load_percent = max(0.25, min(1.00, load_percent))

    for i in range(len(points) - 1):
        if points[i] <= load_percent <= points[i + 1]:
            x1, x2 = points[i], points[i + 1]
            y1, y2 = values[i], values[i + 1]
            return round(y1 + (load_percent - x1) * (y2 - y1) / (x2 - x1), 4)
    return values[0]

def calculate_charge_rate(eboss_model, eboss_type, generator_kva=None, custom_rate=None):
    if custom_rate:
        return custom_rate

    generator_kw = 0
    if eboss_type == "Full Hybrid":
        kva = EBOSS_LOAD_REFERENCE["generator_kva_hybrid"].get(eboss_model, 0)
        generator_kw = kva * 0.8
        return round(generator_kw * 0.98, 1)
    
    elif eboss_type == "Power Module" and generator_kva:
        try:
            kva = float(generator_kva.replace("kVA", ""))
            generator_kw = kva * 0.8
            return round(generator_kw * 0.90 * 0.98, 1)
        except ValueError:
            return 0.0

    return 0.0

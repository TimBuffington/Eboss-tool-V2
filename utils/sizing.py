# utils/sizing.py
from __future__ import annotations
from typing import Dict, List, Tuple
from utils.data import FUEL_BURN_CURVES as FUEL_CURVES

def _interp(x0: float, y0: float, x1: float, y1: float, x: float) -> float:
    if x1 == x0:
        return y0
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)

def fuel_gph_at_load(gen_kva: int, load_fraction: float) -> float:
    """
    Linear interpolation of GPH for a given generator size and load fraction ∈ [0, 1].
    - If load_fraction is outside the table range, we clamp to endpoints.
    - If gen_kva isn't present, we use the nearest available curve.
    """
    if not FUEL_CURVES:
        raise RuntimeError("Fuel curves missing.")

    # pick the nearest available size if exact not present
    if gen_kva not in FUEL_CURVES:
        sizes = sorted(FUEL_CURVES.keys())
        gen_kva = min(sizes, key=lambda s: abs(s - gen_kva))

    points: List[Tuple[float, float]] = sorted(FUEL_CURVES[gen_kva], key=lambda p: p[0])

    # clamp
    x = max(points[0][0], min(points[-1][0], float(load_fraction)))

    # find bracketing points
    for i in range(1, len(points)):
        x0, y0 = points[i - 1]
        x1, y1 = points[i]
        if x0 <= x <= x1:
            return _interp(x0, y0, x1, y1, x)

    # fallback (shouldn't hit with clamp)
    return points[-1][1]

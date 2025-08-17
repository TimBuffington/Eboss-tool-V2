# EBOSS unit specs (all powers in kW, battery in kWh, sizes in kVA)
EBOSS_UNITS = {
    "EB25 kVA": {
        "cont_capacity_kw": 14.0,
        "peak_capacity_kw": 20.0,
        "fh_gen_size_kva": 25,
        "pm_charge_rate_kw": 18.5,
        "fh_charge_rate_kw": 19.5,
        "max_charge_rate_kw": 20.0,
        "battery_kwh": 15,
        "gen_kw": 20.0,
    },
    "EB70 kVA": {
        "cont_capacity_kw": 24.5,
        "peak_capacity_kw": 56.0,
        "fh_gen_size_kva": 45,
        "pm_charge_rate_kw": 33.0,
        "fh_charge_rate_kw": 36.0,
        "max_charge_rate_kw": 45.0,
        "battery_kwh": 25,
        "gen_kw": 36.0,
    },
    "EB125 kVA": {
        "cont_capacity_kw": 49.0,
        "peak_capacity_kw": 100.0,
        "fh_gen_size_kva": 65,
        "pm_charge_rate_kw": 48.0,
        "fh_charge_rate_kw": 52.0,
        "max_charge_rate_kw": 65.0,
        "battery_kwh": 50,
        "gen_kw": 52.0,
    },
    "EB220 kVA": {
        "cont_capacity_kw": 74.0,
        "peak_capacity_kw": 176.0,
        "fh_gen_size_kva": 125,
        "pm_charge_rate_kw": 96.0,
        "fh_charge_rate_kw": 100.0,
        "max_charge_rate_kw": 125.0,
        "battery_kwh": 75,
        "gen_kw": 100.0,
    },
    "EB400 kVA": {
        "cont_capacity_kw": 125.0,
        "peak_capacity_kw": 320.0,
        "fh_gen_size_kva": 220,
        "pm_charge_rate_kw": 166.0,
        "fh_charge_rate_kw": 176.0,
        "max_charge_rate_kw": 220.0,
        "battery_kwh": 125,
        "gen_kw": 176.0,
    },
}


import streamlit as st
import math

MODEL_ORDER = ["EB25 kVA", "EB70 kVA", "EB125 kVA", "EB220 kVA", "EB400 kVA"]
# --- EBOSS Inputs (example) ---
eboss_model = st.selectbox("EBOSS Model", ["EB25 kVA","EB70 kVA","EB125 kVA","EB220 kVA","EB400 kVA"], key="eboss_model")
eboss_type  = st.selectbox("EBOSS Type", ["Full Hybrid", "Power Module"], key="eboss_type")

# Power Module generator size (only when PM selected)
pm_gen = None
if eboss_type == "Power Module":
    pm_gen = st.selectbox(
        "Generator Size (kVA)",
        [25, 45, 65, 125, 220],
        key="power_module_gen_size"  # <-- canon key used everywhere
    )

# Optional: mirror into session (if you prefer to read from S later)
S = st.session_state.setdefault("user_inputs", {})
if pm_gen is not None:
    S["power_module_gen_size"] = pm_gen

# ---------- parsing & conversions ----------
def _parse_kva(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).lower().replace("kva", "").strip()
    try:
        return float(s)
    except ValueError:
        return None

def _gen_kw_from_kva(kva):
    return 0.8 * float(kva)

def _to_kw_480(value, units, voltage, pf=0.8):
    """Normalize a single input to kW (baseline 3φ 480V)."""
    if units == "kW":
        return float(value or 0.0)
    v = float(voltage); i = float(value or 0.0)
    if str(voltage) in {"208", "480"}:           # 3φ
        return (1.732 * v * i * pf) / 1000.0
    return (v * i * pf) / 1000.0                 # 1φ (120/240)

# ---------- loads: compute + store ----------
def compute_and_store_loads(*, continuous_value, peak_value, units, voltage, pf=0.8):
    st.session_state.setdefault("user_inputs", {})
    S = st.session_state.user_inputs

    # raw UI
    S["raw_input_units"] = units
    S["raw_input_voltage"] = str(voltage)
    S["raw_input_continuous"] = float(continuous_value or 0.0)
    S["raw_input_peak"] = float(peak_value or 0.0)

    # normalized
    cont_kw = _to_kw_480(continuous_value, units, voltage, pf)
    peak_kw = _to_kw_480(peak_value,       units, voltage, pf)
    S["actual_continuous_load"] = cont_kw
    S["actual_peak_load"] = peak_kw
    return cont_kw, peak_kw

# ---------- UI panel for adjusted loads ----------
def render_adjusted_load_panel(cont_kw, peak_kw):
    st.markdown(
        f"""
        <div style="border:1px solid #939598;border-radius:10px;padding:12px 14px;
                    background:rgba(0,0,0,.55);box-shadow:0 0 12px rgba(129,189,71,.35);">
          <div style="font-weight:800;letter-spacing:.4px;margin-bottom:6px;">
            Adjusted Load (kW @ 3φ 480V)
          </div>
          <div>Continuous: <b>{cont_kw:.2f} kW</b></div>
          <div>Peak: <b>{peak_kw:.2f} kW</b></div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------- unified charge rate ----------
def render_charge_rate(eboss_model, eboss_type, *, generator_kva=None, custom_rate=None,
                       store_to_session=True, session_key="charge_rate_kw"):
    """
    One call to determine charge rate (kW, rounded 0.1).
    - Default to model FH/PM rate from EBOSS_UNITS.
    - custom_rate overrides.
    - PM: if gen is provided and gen_kW < desired → warn & let user:
        • proceed (set to 98% of gen kW), or
        • select larger gen (stop)
    """
    spec = EBOSS_UNITS.get(eboss_model)
    if not spec:
        return None

    # desired rate
    if custom_rate is not None:
        try:
            desired = float(custom_rate)
        except (TypeError, ValueError):
            return None
    else:
        if eboss_type == "Full Hybrid":
            desired = float(spec.get("fh_charge_rate_kw", 0.0))
        elif eboss_type == "Power Module":
            desired = float(spec.get("pm_charge_rate_kw", 0.0))
        else:
            return None

    # FH: use as-is
    if eboss_type == "Full Hybrid":
        rate = round(desired, 1)
        if store_to_session:
            st.session_state.setdefault("user_inputs", {})
            st.session_state.user_inputs[session_key] = rate
            st.session_state.user_inputs["charge_rate_source"] = "custom" if custom_rate is not None else "fh_default"
        return rate

    # PM: check gen if provided
    pm_gen = _parse_kva(generator_kva)
    if pm_gen is None or pm_gen <= 0:
        rate = round(desired, 1)
        if store_to_session:
            st.session_state.setdefault("user_inputs", {})
            st.session_state.user_inputs[session_key] = rate
            st.session_state.user_inputs["charge_rate_source"] = "custom" if custom_rate is not None else "pm_default"
        return rate

    gen_kw = _gen_kw_from_kva()
    if gen_kw >= desired:
        rate = round(desired, 1)
        if store_to_session:
            st.session_state.user_inputs[session_key] = rate
            st.session_state.user_inputs["charge_rate_source"] = "custom" if custom_rate is not None else "pm_default"
        return rate

    # undersized → prompt
    st.warning(
        f"Selected generator is **{gen_kw:.1f} kW**, which is **below** the desired charge rate "
        f"(**{desired:.1f} kW**) for **{eboss_model}**."
    )
    c1, c2 = st.columns(2)
    proceed = c1.button(
        "Proceed: adjust charge rate to 98% of generator kW",
        key=f"pm_adjust_{eboss_model}_{pm_gen}_{desired}"
    )
    choose_larger = c2.button(
        "Select a larger generator",
        key=f"pm_larger_{eboss_model}_{pm_gen}_{desired}"
    )

    if proceed:
        adjusted = round(0.98 * gen_kw, 1)
        st.success(f"Charge rate adjusted to **{adjusted:.1f} kW** (98% of generator kW).")
        if store_to_session:
            st.session_state.user_inputs[session_key] = adjusted
            st.session_state.user_inputs["charge_rate_source"] = "pm_adjusted_to_98pct_gen"
        return adjusted

    if choose_larger:
        st.info("Please select a larger generator size.")
        st.stop()

    st.stop()
    return None

# alias (if you prefer PascalCase calls in other places)
render_Charge_Rate = render_charge_rate

# ---------- pick model by load ----------
def determine_model_by_load(cont_kw, peak_kw):
    for model in MODEL_ORDER:
        spec = EBOSS_UNITS.get(model, {})
        if not spec:
            continue
        if cont_kw <= float(spec.get("cont_capacity_kw", 0)) and peak_kw <= float(spec.get("peak_capacity_kw", 0)):
            return model
    return None

#import math
import streamlit as st

def _set_if_missing(S: dict, key: str, value):
    """Set only if missing/None; return final value."""
    if key not in S or S.get(key) is None:
        S[key] = value
    return S[key]

import math
import streamlit as st

def store_derived_metrics(
    *,
    eboss_model: str,
    eboss_type: str,
    cont_kw: float,
    peak_kw: float,
    charge_rate_kw: float,
    generator_kva=None,
    hours_per_day: float = 24.0,   # default duty time
):
    """
    Persist derived values for other pages. Fuel uses interpolation only.
    Assumes 100% of battery_kwh is usable.
    Does not overwrite existing keys already set in st.session_state.user_inputs.
    """
st.session_state.setdefault("user_inputs", {})
    S = st.session_state.user_inputs

    # ---- Specs ----
    spec = EBOSS_UNITS.get(eboss_model, {}) or {}
    battery_kwh = float(spec.get("battery_kwh", 0) or 0)
    cont_capacity_kw_spec = float(spec.get("cont_capacity_kw", 0) or 0)
    peak_capacity_kw_spec = float(spec.get("peak_capacity_kw", 0) or 0)
    pm_charge_rate_spec   = float(spec.get("pm_charge_rate_kw", 0) or 0)
    fh_charge_rate_spec   = float(spec.get("fh_charge_rate_kw", 0) or 0)
    max_charge_rate_spec  = float(spec.get("max_charge_rate_kw", 0) or 0)

    # ---- Determine generator sizing (kVA → kW) ----
    if eboss_type == "Full Hybrid":
        pm_gen_for_interp = spec.get("fh_gen_size_kva")
        if not pm_gen_for_interp:
            st.warning("Full Hybrid generator size (kVA) missing from specs; cannot interpolate fuel.")
            st.stop()
        pm_gen_for_interp = int(pm_gen_for_interp)
        gen_kw = _gen_kw_from_kva(pm_gen_for_interp)
   else:
    pm_gen_for_interp = spec.get("pm_gen_size_kva")
    if not pm_gen_for_interp:
        st.warning("PM generator size (kVA) missing from specs; cannot interpolate fuel.")
        st.stop()
    pm_gen_for_interp = int(pm_gen_for_interp)
    gen_kw = _gen_kw_from_kva(pm_gen_for_interp)


    # ---- Engine load & fuel (INTERPOLATION ONLY) ----
    load_frac = (charge_rate_kw / gen_kw) if gen_kw > 0 else 0.0
    load_frac = max(0.0, min(1.0, load_frac))

    fuel_gph = interpolate_gph(pm_gen_for_interp, load_frac)
    if fuel_gph == 0.0:
        st.warning("No interpolation row for this generator size; use one of: 25, 45, 65, 125, 220 kVA.")
        st.stop()

    # ---- Battery & charge math ----
    usable_kwh = battery_kwh   # 100% usable
    runtime_h_at_cont = (usable_kwh / cont_kw) if cont_kw > 0 else math.inf

    net_charge_kw = max((charge_rate_kw - cont_kw), 0.01)
    charge_time_h_full = usable_kwh / net_charge_kw if net_charge_kw > 0 else math.inf

    # ---- Daily estimates ----
    
    cycles_per_day = (daily_energy_kwh / usable_kwh) if usable_kwh > 0 else math.inf
    engine_run_h_day = cycles_per_day * charge_time_h_full if math.isfinite(cycles_per_day) else math.inf
    daily_fuel_gal = engine_run_h_day * fuel_gph if math.isfinite(engine_run_h_day) else math.inf

    # ---- Persist (only if missing) ----
    def _set_if_missing(d, k, v):
        if k not in d or d[k] in (None, ""):
            d[k] = v

    _set_if_missing(S, "eboss_model", eboss_model)
    _set_if_missing(S, "eboss_type", eboss_type)
    _set_if_missing(S, "power_module_gen_size", (str(generator_kva) if generator_kva else S.get("power_module_gen_size","")))
    _set_if_missing(S, "battery_kwh", round(battery_kwh, 2))
    _set_if_missing(S, "usable_battery_kwh", round(usable_kwh, 2))

    _set_if_missing(S, "gen_kw", round(gen_kw, 2))
    _set_if_missing(S, "engine_load_pct", round(load_frac * 100.0, 2))
    _set_if_missing(S, "fuel_gph_at_charge", round(fuel_gph, 3))

    _set_if_missing(S, "cont_capacity_kw", round(cont_capacity_kw_spec, 2))
    _set_if_missing(S, "peak_capacity_kw", round(peak_capacity_kw_spec, 2))
    _set_if_missing(S, "pm_charge_rate_kw_spec", round(pm_charge_rate_spec, 2))
    _set_if_missing(S, "fh_charge_rate_kw_spec", round(fh_charge_rate_spec, 2))
    _set_if_missing(S, "max_charge_rate_kw_spec", round(max_charge_rate_spec, 2))

    _set_if_missing(S, "actual_continuous_load", round(cont_kw, 2))
    _set_if_missing(S, "actual_peak_load", round(peak_kw, 2))
    _set_if_missing(S, "charge_rate_kw", round(charge_rate_kw, 2))

    _set_if_missing(S, "battery_runtime_hours_at_cont", round(runtime_h_at_cont, 2) if math.isfinite(runtime_h_at_cont) else runtime_h_at_cont)
    _set_if_missing(S, "charge_time_hours_full", round(charge_time_h_full, 2) if math.isfinite(charge_time_h_full) else charge_time_h_full)

    _set_if_missing(S, "daily_energy_kwh", round(daily_energy_kwh, 2))
    _set_if_missing(S, "daily_cycles", round(cycles_per_day, 3) if math.isfinite(cycles_per_day) else cycles_per_day)
    _set_if_missing(S, "engine_run_hours_per_day", round(engine_run_h_day, 2) if math.isfinite(engine_run_h_day) else engine_run_h_day)
    _set_if_missing(S, "daily_fuel_gal", round(daily_fuel_gal, 2) if math.isfinite(daily_fuel_gal) else daily_fuel_gal)

    return S
S = st.session_state.setdefault("user_inputs", {})
store_derived_metrics(
    eboss_model=S.get("eboss_model",""),
    eboss_type=S.get("eboss_type",""),
    cont_kw=float(S.get("actual_continuous_load", 0) or 0),
    peak_kw=float(S.get("actual_peak_load", 0) or 0),
    charge_rate_kw=float(S.get("charge_rate_kw", 0) or 0),
    generator_kva=S.get("power_module_gen_size"),
)

if manual_select_clicked:
    try:
        @st.dialog("EBOSS® Configuration")
        def show_manual_config_dialog():
            st.markdown("Enter your EBOSS® configuration:")

            col1, col2, col3 = st.columns(3)

            # A) Model / Type / PM gen
            with col1:
                eboss_model = st.selectbox("EBOSS® Model", list(EBOSS_UNITS.keys()), key="eboss_model_input")
                eboss_type = st.selectbox("EBOSS® Type", ["Full Hybrid", "Power Module"], key="eboss_type_input")
                generator_kva = None
                if eboss_type == "Power Module":
                    generator_kva = st.selectbox(
                        "Power Module Generator Size",
                        ["", "25 kVA", "45 kVA", "65 kVA", "125 kVA", "220 kVA"],
                        index=0, key="power_module_gen_size_input"
                    ) or None

            # B) Loads
            with col2:
                max_continuous_load = st.number_input("Max Continuous Load", min_value=0.0, step=0.1, format="%g")
                max_peak_load = st.number_input("Max Peak Load", min_value=0.0, step=0.1, format="%g")

            # C) Units & Voltage with placeholders (gate)
            with col3:
                units = st.selectbox("Units", ["kW", "Amps"], index=None, placeholder="Select units")
                voltage = st.selectbox("Voltage", ["120", "240", "208", "480"], index=None, placeholder="Select voltage")

            if units is None or voltage is None:
                st.warning("Please select **Units** and **Voltage** to continue.")
                st.stop()

            # Normalize + panel
            cont_kw, peak_kw = compute_and_store_loads(
                continuous_value=max_continuous_load,
                peak_value=max_peak_load,
                units=units, voltage=voltage, pf=0.8
            )
            render_adjusted_load_panel(cont_kw, peak_kw)

            # Validate (use your existing validator)
            errors = validate_inputs(
                eboss_model, eboss_type,
                max_continuous_load, max_peak_load,
                generator_kva, units, voltage
            )
            if errors:
                for e in errors: st.error(e)
                st.stop()

            # Charge rate (FH/PM unified)
            charge_rate_kw = render_charge_rate(
                eboss_model=eboss_model,
                eboss_type=eboss_type,
                generator_kva=generator_kva
            )

            # Store a rich set of derived values for downstream pages
            store_derived_metrics(
                eboss_model=eboss_model,
                eboss_type=eboss_type,
                cont_kw=cont_kw,
                peak_kw=peak_kw,
                charge_rate_kw=charge_rate_kw or 0.0,
                generator_kva=generator_kva
            )

            st.session_state.show_calculator = True
            st.success("Configuration validated and stored.")

        show_manual_config_dialog()
    except Exception as e:
        st.error(f"Error in modal: {str(e)}.")


if load_based_clicked:
    try:
        @st.dialog("Load Based Suggested EBOSS® Configuration")
        def show_load_based_dialog():
            st.markdown("Enter raw load inputs; we’ll auto-select the EBOSS® model:")

            col1, col2, col3 = st.columns(3)

            # A) Type fixed
            with col1:
                st.selectbox("EBOSS® Type", ["Full Hybrid"], index=0, disabled=True, key="eboss_type_lb_fixed")

            # B) Loads
            with col2:
                max_continuous_load = st.number_input("Max Continuous Load", min_value=0.0, step=0.1, format="%g")
                max_peak_load = st.number_input("Max Peak Load", min_value=0.0, step=0.1, format="%g")

            # C) Units & Voltage (gate)
            with col3:
                units = st.selectbox("Units", ["kW", "Amps"], index=None, placeholder="Select units")
                voltage = st.selectbox("Voltage", ["120", "240", "208", "480"], index=None, placeholder="Select voltage")

            if units is None or voltage is None:
                st.warning("Please select **Units** and **Voltage** to continue.")
                st.stop()

            # Normalize + panel
            cont_kw, peak_kw = compute_and_store_loads(
                continuous_value=max_continuous_load,
                peak_value=max_peak_load,
                units=units, voltage=voltage, pf=0.8
            )
            render_adjusted_load_panel(cont_kw, peak_kw)

            # Basic structure validation
            errors = validate_inputs("EB25 kVA", "Full Hybrid", max_continuous_load, max_peak_load, None, units, voltage)
            if errors:
                for e in errors: st.error(e)
                st.stop()

            # Auto-pick smallest model meeting cont & peak
            chosen_model = determine_model_by_load(cont_kw, peak_kw)
            if not chosen_model:
                st.error("No EBOSS® model can satisfy these loads. Please adjust inputs.")
                st.stop()

            st.session_state.setdefault("user_inputs", {})
            st.session_state.user_inputs.update({
                "eboss_type": "Full Hybrid",
                "power_module_gen_size": "",
                "eboss_model": chosen_model
            })

            st.markdown(
                f"""
                <div style="margin-top:10px;">
                  <div style="font-weight:700; margin-bottom:4px;">EBOSS® Model Based on Load</div>
                  <div style="border:1px solid #939598;border-radius:8px;padding:10px;background:rgba(0,0,0,.35);">
                    {chosen_model}
                  </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Charge rate (FH)
            charge_rate_kw = render_charge_rate(chosen_model, "Full Hybrid")

            # Store derived values
            store_derived_metrics(
                eboss_model=chosen_model,
                eboss_type="Full Hybrid",
                cont_kw=cont_kw,
                peak_kw=peak_kw,
                charge_rate_kw=charge_rate_kw or 0.0,
                generator_kva=None
            )

            st.session_state.show_calculator = True
            st.success("Configuration validated and stored.")

        show_load_based_dialog()
    except Exception as e:
        st.error(f"Error in modal: {str(e)}.")

# ================================
# Modal: EBOSS® Model Based on Max Fuel Efficiency (full pack usable)
# ================================
import streamlit as st
import math

MODEL_ORDER = ["EB25 kVA", "EB70 kVA", "EB125 kVA", "EB220 kVA", "EB400 kVA"]

def _eligible_efficiency(model: str, cont_kw: float, peak_kw: float) -> bool:
    spec = EBOSS_UNITS.get(model, {})
    if not spec: return False
    battery_kwh = float(spec.get("battery_kwh", 0) or 0)
    peak_cap_kw = float(spec.get("peak_capacity_kw", 0) or 0)
    # Rule: cont_kW ≤ (2/3)*battery_kWh  AND  peak_kW ≤ peak capacity
    return (cont_kw <= (2.0/3.0)*battery_kwh) and (peak_kw <= peak_cap_kw)

def _simulate_day_for_model_fullpack(model: str, cont_kw: float, peak_kw: float, charge_efficiency: float = 0.90):
    """
    Pure calc (no session writes). Uses full battery_kWh, net charge (charge_rate - cont).
    Returns dict with runtime, charge_time, cycles/day, engine_run/day, fuel (gpd/gpw/gpm), etc.
    Fuel is interpolation-only (no BSFC).
    """
    spec = EBOSS_UNITS.get(model, {})
    if not spec: return None

    battery_kwh = float(spec.get("battery_kwh", 0) or 0)
    peak_cap_kw = float(spec.get("peak_capacity_kw", 0) or 0)
    charge_rate = float(spec.get("fh_charge_rate_kw", 0) or 0)
    pm_gen     = int(float(spec.get("fh_gen_size_kva", 0) or 0))
    gen_kw      = 0.8 * pm_gen if pm_gen > 0 else 0.0

    if peak_kw > peak_cap_kw or battery_kwh <= 0 or charge_rate <= 0 or gen_kw <= 0:
        return None

    # Battery runtime at continuous load (full pack usable)
    battery_runtime_h = (battery_kwh / cont_kw) if cont_kw > 0 else math.inf

    # Net charge while load persists
    net_charge_kw = max(charge_rate - cont_kw, 0.01)
    charge_time_h = (battery_kwh / charge_efficiency) / net_charge_kw

    # Cycles & engine run per day
    total_cycle_h = battery_runtime_h + charge_time_h
    cycles_per_day = (24.0 / total_cycle_h) if total_cycle_h > 0 else 0.0
    engine_run_h_day = cycles_per_day * charge_time_h

    # Engine load during charge for interpolation
    load_frac = max(0.0, min(1.0, charge_rate / gen_kw))
    gph = interpolate_gph(pm_gen, load_frac)
    if gph <= 0:
        return None

    daily_fuel_gal  = engine_run_h_day * gph
    fuel_week_gal   = daily_fuel_gal * 7.0
    fuel_month_gal  = daily_fuel_gal * 30.0

    return {
        "battery_kwh": battery_kwh,
        "fh_charge_rate_kw": charge_rate,
        "fh_gen_size_kva": pm_gen,
        "gen_kw": gen_kw,
        "engine_load_frac": load_frac,
        "fuel_gph_at_charge": gph,
        "battery_runtime_hours_at_cont": battery_runtime_h,
        "charge_time_hours_full": charge_time_h,
        "cycles_per_day": cycles_per_day,
        "engine_run_hours_per_day": engine_run_h_day,
        "daily_fuel_gal": daily_fuel_gal,
        "fuel_gal_per_week": fuel_week_gal,
        "fuel_gal_per_month": fuel_month_gal,
    }

def _best_fuel_model_fullpack(cont_kw: float, peak_kw: float):
    """Pick the eligible (or larger) model with the lowest daily fuel (gal/day)."""
    eligible_idx = [i for i, m in enumerate(MODEL_ORDER) if _eligible_efficiency(m, cont_kw, peak_kw)]
    if not eligible_idx:
        return None, None
    start = min(eligible_idx)

    best_model, best_metrics = None, None
    best_gpd = float("inf")
    for m in MODEL_ORDER[start:]:
        mets = _simulate_day_for_model_fullpack(m, cont_kw, peak_kw)
        if not mets: continue
        gpd = mets["daily_fuel_gal"]
        if math.isfinite(gpd) and gpd < best_gpd:
            best_model, best_metrics, best_gpd = m, mets, gpd
    return best_model, best_metrics


# ==== Show modal (Homepage) ====
if st.session_state.get("fuel_efficiency_clicked"):
    try:
        @st.dialog("EBOSS® Model Based on Max Fuel Efficiency")
        def show_fuel_efficiency_dialog():
            st.markdown("We’ll suggest the **most fuel-efficient Full Hybrid EBOSS®** for your loads.")

            c1, c2, c3 = st.columns(3)
            with c1:
                st.selectbox("EBOSS® Type", ["Full Hybrid"], index=0, disabled=True, key="eff_eb_type_fixed")
            with c2:
                cont_raw = st.number_input("Max Continuous Load", min_value=0.0, step=0.1, format="%g",
                                           key="eff_max_continuous_load_input")
                peak_raw = st.number_input("Max Peak Load", min_value=0.0, step=0.1, format="%g",
                                           key="eff_max_peak_load_input")
            with c3:
                units   = st.selectbox("Units",   ["kW", "Amps"], index=None, placeholder="Select units",   key="eff_units_input")
                voltage = st.selectbox("Voltage", ["120", "240", "208", "480"], index=None, placeholder="Select voltage", key="eff_voltage_input")

            if units is None or voltage is None:
                st.warning("Please select **Units** and **Voltage** to continue.")
                st.stop()

            # Normalize to kW @ 3φ 480V and show panel
            cont_kw, peak_kw = compute_and_store_loads(
                continuous_value=cont_raw, peak_value=peak_raw, units=units, voltage=voltage, pf=0.8
            )
            render_adjusted_load_panel(cont_kw, peak_kw)

            # Find the most fuel-efficient eligible model (and larger)
            best_model, best_metrics = _best_fuel_model_fullpack(cont_kw, peak_kw)
            if not best_model:
                st.error("No EBOSS® model satisfies: cont_kW ≤ 2/3·battery_kWh and peak ≤ model peak capacity.")
                st.stop()

            # Persist choice
            S = st.session_state.user_inputs
            S.update({"eboss_type": "Full Hybrid", "power_module_gen_size": "", "eboss_model": best_model})

            # Show chosen model
            st.markdown(
                f"""
                <div style="margin-top:10px;">
                  <div style="font-weight:700; margin-bottom:4px;">Most Fuel-Efficient EBOSS® Model</div>
                  <div style="border:1px solid #939598;border-radius:8px;padding:10px;background:rgba(0,0,0,.35);">
                    {best_model}
                  </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Ensure charge rate is stored for this model (FH)
            charge_rate_kw = render_charge_rate(best_model, "Full Hybrid")

            # Store core/derived metrics using full pack (no usable_kwh). We update with our exact calcs.
            # First call your session helper (it won't overwrite), then set precise values from best_metrics.
            store_derived_metrics(
                eboss_model=best_model,
                eboss_type="Full Hybrid",
                cont_kw=cont_kw,
                peak_kw=peak_kw,
                charge_rate_kw=charge_rate_kw or float(best_metrics["fh_charge_rate_kw"]),
                generator_kva=None,
                usable_soc_frac=1.0  # full pack usable
            )

            # Overwrite/ensure keys match our full-pack & net-charge calcs
            S["battery_runtime_hours_at_cont"] = round(best_metrics["battery_runtime_hours_at_cont"], 2)
            S["charge_time_hours_full"]        = round(best_metrics["charge_time_hours_full"], 2)
            S["cycles_per_day"]                = round(best_metrics["cycles_per_day"], 3)
            S["engine_run_hours_per_day"]      = round(best_metrics["engine_run_hours_per_day"], 2)
            S["fuel_gph_at_charge"]            = round(best_metrics["fuel_gph_at_charge"], 3)
            S["daily_fuel_gal"]                = round(best_metrics["daily_fuel_gal"], 2)
            S["fuel_gal_per_week"]             = round(best_metrics["fuel_gal_per_week"], 2)
            S["fuel_gal_per_month"]            = round(best_metrics["fuel_gal_per_month"], 2)

            # Quick summary
            st.success(
                f"Daily fuel: **{S['daily_fuel_gal']:.2f} gal/day** · "
                f"Battery runtime: **{S['battery_runtime_hours_at_cont']:.2f} h** · "
                f"Charge time (net): **{S['charge_time_hours_full']:.2f} h** · "
                f"Cycles/day: **{S['cycles_per_day']:.2f}**"
            )

        show_fuel_efficiency_dialog()
    except Exception as e:
        st.error(f"Error in modal: {str(e)}.")


# ==========================================================================

def interpolate_gph(pm_gen: int, load_pct: float) -> float:
    """
    Piecewise-linear interpolation for GPH at given load fraction (0..1) using your table.
    """
    gph_table = {
        25:  [0.67, 0.94, 1.26, 1.62],
        45:  [1.04, 1.60, 2.20, 2.03],
        65:  [1.70, 2.60, 3.50, 4.40],
        125: [2.60, 4.10, 5.60, 7.10],
        220: [4.60, 6.90, 9.40, 12.0],
        400: [7.70, 12.2, 17.3, 22.5],
    }
    if pm_gen not in gph_table:
        return 0.0

    pts = gph_table[pm_gen]
    x = max(0.0, min(1.0, float(load_pct or 0.0)))
    if x <= 0.25:
        return pts[0]
    if x <= 0.50:
        t = (x - 0.25) / 0.25
        return pts[0] + t * (pts[1] - pts[0])
    if x <= 0.75:
        t = (x - 0.50) / 0.25
        return pts[1] + t * (pts[2] - pts[1])
    t = (x - 0.75) / 0.25
    return pts[2] + t * (pts[3] - pts[2])
import streamlit as st
import math

def _parse_kva(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).lower().replace("kva", "").strip()
    try:
        return float(s)
    except ValueError:
        return None

def _set_if_missing(S: dict, key: str, value):
    if key not in S or S.get(key) is None:
        S[key] = value
    return S[key]

def fill_runtime_and_fuel_if_missing(
    *, eboss_model: str, eboss_type: str, cont_kw: float, generator_kva=None
):
    """
    Computes runtime/charge/fuel using ONLY interpolation.
    Writes keys only if they are missing.
    Requires:
      - st.session_state.user_inputs['charge_rate_kw'] already set (via render_charge_rate)
      - EBOSS_UNITS with 'battery_kwh' and 'fh_gen_size_kva' (for FH)
    """
    st.session_state.setdefault("user_inputs", {})
    S = st.session_state.user_inputs

    # Required inputs
    charge_kw = float(S.get("charge_rate_kw") or 0.0)
    if charge_kw <= 0:
        st.warning("Charge rate not set yet; cannot compute runtime/fuel.")
        st.stop()

    spec = EBOSS_UNITS.get(eboss_model, {})
    battery_kwh = float(spec.get("battery_kwh", 0) or 0)

    # Determine generator kVA / kW for interpolation & % load
    if eboss_type == "Full Hybrid":
        pm_gen_for_interp = spec.get("fh_gen_size_kva")
        if not pm_gen_for_interp:
            st.warning("FH generator size (kVA) missing from specs; cannot interpolate fuel.")
            st.stop()
        pm_gen_for_interp = int(pm_gen_for_interp)
        gen_kw = 0.8 * pm_gen_for_interp
    else:
        gkva = _parse_kva(generator_kva)
        if not gkva:
            st.warning("Power Module generator size required to interpolate fuel.")
            st.stop()
        pm_gen_for_interp = int(gkva)
        gen_kw = 0.8 * gkva

    # Engine load fraction during charging (cap 0..1 for interpolation)
    load_frac = charge_kw / gen_kw if gen_kw > 0 else 0.0
    load_frac = max(0.0, min(1.0, load_frac))

    # --- Set core metrics if missing ---
    _set_if_missing(S, "gen_kw", round(gen_kw, 2))
    _set_if_missing(S, "engine_load_pct", round(load_frac * 100.0, 2))

    # Battery-only runtime at continuous load
    if cont_kw > 0:
        _set_if_missing(S, "battery_runtime_hours_at_cont", round(battery_kwh / cont_kw, 2))
    else:
        _set_if_missing(S, "battery_runtime_hours_at_cont", math.inf)

    # Net charge power into battery (keep >0 to avoid /0)
    net_charge_kw = max(charge_kw - cont_kw, 0.01)
    _set_if_missing(S, "net_charge_kw", round(net_charge_kw, 2))

    # Full charge time (from 0 to full battery_kwh; if you use usable SoC elsewhere, swap in)
    _set_if_missing(S, "charge_time_hours_full", round(battery_kwh / net_charge_kw, 2))

    # Cycles/day & engine run-time/day
    battery_life_hr = float(S.get("battery_runtime_hours_at_cont") or 0.0)
    charge_time_hr = float(S.get("charge_time_hours_full") or 0.0)
    total_cycle_hr = (battery_life_hr + charge_time_hr) if all(x > 0 for x in [battery_life_hr, charge_time_hr]) else 0
    cycles_per_day = (24.0 / total_cycle_hr) if total_cycle_hr > 0 else 0.0
    _set_if_missing(S, "daily_cycles", round(cycles_per_day, 3) if cycles_per_day else 0.0)

    engine_run_h_per_day = cycles_per_day * charge_time_hr
    _set_if_missing(S, "engine_run_hours_per_day", round(engine_run_h_per_day, 2))

    # 🔹 Fuel at charge (INTERPOLATION ONLY)
    gph = interpolate_gph(pm_gen_for_interp, load_frac)
    if gph == 0.0:
        st.warning("No interpolation row for this generator size; please use one of: 25, 45, 65, 125, 220, 400 kVA.")
        st.stop()

    _set_if_missing(S, "fuel_gph_at_charge", round(gph, 3))  # <- canonical key, interpolation ONLY

    # Daily fuel use (gallons)
    daily_fuel = engine_run_h_per_day * gph
    _set_if_missing(S, "daily_fuel_gal", round(daily_fuel, 2))


def calculate_costs_eboss_if_missing(
    *, fuel_cost_per_gal: float, rental: float = 0, delivery: float = 0, pm_cost: float = 0
):
    """
    Uses ONLY interpolated fuel_gph_at_charge.
    Sets cost/CO2 keys only if missing.
    """
    st.session_state.setdefault("user_inputs", {})
    S = st.session_state.user_inputs

    runtime_hr = float(S.get("engine_run_hours_per_day") or 0.0)
    fuel_gph  = float(S.get("fuel_gph_at_charge") or 0.0)  # interpolation-only

    if fuel_gph <= 0:
        st.warning("Interpolated fuel burn (fuel_gph_at_charge) not available yet.")
        st.stop()

    if S.get("daily_fuel_cost") is None:
        gallons = runtime_hr * fuel_gph
        _set_if_missing(S, "daily_fuel_cost", round(gallons * fuel_cost_per_gal, 2))

    if S.get("daily_total_cost") is None:
        total_cost = float(S.get("daily_fuel_cost") or 0.0) + float(rental) + float(delivery) + float(pm_cost)
        _set_if_missing(S, "daily_total_cost", round(total_cost, 2))

    if S.get("daily_co2_tons") is None:
        gallons = runtime_hr * fuel_gph
        co2_tons = (gallons * 22.4) / 2000.0  # 22.4 lb/gal → tons
        _set_if_missing(S, "daily_co2_tons", round(co2_tons, 4))

# --- name normalization so "EB 25 kVA" still works with EBOSS_UNITS keys ---
_MODEL_KEY_MAP = {
    "EB 25 kVA": "EB25 kVA",
    "EB 70 kVA": "EB70 kVA",
    "EB 125 kVA": "EB125 kVA",
    "EB 220 kVA": "EB220 kVA",
    "EB 400 kVA": "EB400 kVA",
}
def _norm_model(name: str) -> str:
    return _MODEL_KEY_MAP.get(name, name)

# --- UPDATED: get_charge_rate (keeps your name, uses new dict + single entrypoint) ---
def get_charge_rate(model: str, gen_type: str, *, generator_kva=None, custom_rate=None):
    """
    Returns (charge_kw, battery_kwh, max_charge_rate_kw).
    Uses EBOSS_UNITS + render_charge_rate; stores charge rate in session (once).
    """
    model = _norm_model(model)
    spec = EBOSS_UNITS.get(model, {})
    # compute/set charge rate once (handles PM undersized-gen prompt)
    rate_kw = render_charge_rate(
        eboss_model=model,
        eboss_type=gen_type,
        generator_kva=generator_kva,
        custom_rate=custom_rate,
        store_to_session=True,
        session_key="charge_rate_kw",
    )
    return (
        float(rate_kw or 0.0),
        float(spec.get("battery_kwh", 0) or 0),
        float(spec.get("max_charge_rate_kw", 0) or 0),
    )

# --- KEEP (or rename to validate_charge_rate_config) ---
def validate_charge_rate(charge_kw, gen_kw, max_charge):
    if (max_charge > 0) and (charge_kw > max_charge):
        return "❌ Charge rate exceeds EBOSS® capacity"
    if (gen_kw > 0) and (gen_kw < charge_kw):
        return "❌ Generator undersized for Power Module mode"
    if (max_charge > 0) and (gen_kw > max_charge):
        return "⚠️ Generator oversized; reduced efficiency"
    return "✅ Charge config valid"

# --- KEEP: interpolation-only (load_pct fraction 0..1) ---
def interpolate_gph(pm_gen, load_pct):
    table = {
        25:  [0.67, 0.94, 1.26, 1.62],
        45:  [1.04, 1.60, 2.20, 2.03],
        65:  [1.70, 2.60, 3.50, 4.40],
        125: [2.60, 4.10, 5.60, 7.10],
        220: [4.60, 6.90, 9.40, 12.0],
        400: [7.70, 12.2, 17.3, 22.5],
    }
    if pm_gen not in table:
        return 0.0
    pts = table[pm_gen]
    x = max(0.0, min(1.0, float(load_pct or 0.0)))
    if x <= 0.25:
        return pts[0]
    if x <= 0.50:
        t = (x - 0.25) / 0.25
        return pts[0] + t * (pts[1] - pts[0])
    if x <= 0.75:
        t = (x - 0.50) / 0.25
        return pts[1] + t * (pts[2] - pts[1])
    t = (x - 0.75) / 0.25
    return pts[2] + t * (pts[3] - pts[2])

# --- REPLACE: calculate_engine_runtime (FH/PM; interpolation-only; returns dict like your original) ---
def calculate_engine_runtime(model: str, gen_type: str, cont_kw: float, kva):
    """
    Computes charge/runtime/fuel using only interpolation. Returns dict.
    Assumes charge_rate_kw already stored via get_charge_rate/render_charge_rate.
    """
    import math
    model = _norm_model(model)
    spec = EBOSS_UNITS.get(model, {})
    charge_kw = float(st.session_state.user_inputs.get("charge_rate_kw") or 0.0)
    if charge_kw <= 0:
        # compute now if needed
        charge_kw, _, _ = get_charge_rate(model, gen_type, generator_kva=kva)

    # generator kW + %load
    pm_gen = float(str(kva).lower().replace("kva","").strip()) if kva is not None else 0.0
    if gen_type == "Full Hybrid" and pm_gen == 0.0:
        pm_gen = float(spec.get("fh_gen_size_kva", 0) or 0)
    gen_kw = 0.8 * pm_gen if pm_gen > 0 else float(spec.get("gen_kw", 0) or 0)

    engine_load_frac = (charge_kw / gen_kw) if gen_kw > 0 else 0.0
    engine_load_frac = max(0.0, min(1.0, engine_load_frac))
    gph = interpolate_gph(int(pm_gen), engine_load_frac) if pm_gen else 0.0

    battery_kwh = float(spec.get("battery_kwh", 0) or 0)
    battery_life_hr = (battery_kwh / cont_kw) if cont_kw > 0 else math.inf
    net_charge_kw = max(charge_kw - cont_kw, 0.01)
    charge_time_hr = battery_kwh / net_charge_kw
    total_cycle_hr = (battery_life_hr + charge_time_hr) if all(x > 0 for x in [battery_life_hr, charge_time_hr]) else 0
    cycles_per_day = (24.0 / total_cycle_hr) if total_cycle_hr > 0 else 0.0
    daily_runtime = charge_time_hr * cycles_per_day

    return {
        "gen_kw": round(gen_kw, 2),
        "charge_kw": round(charge_kw, 2),
        "battery_life_hr":  round(battery_life_hr, 2) if battery_life_hr != math.inf else math.inf,
        "charge_time_hr":   round(charge_time_hr, 2),
        "cycles_per_day":   round(cycles_per_day, 3),
        "daily_runtime_hr": round(daily_runtime, 2),
        "engine_load_pct":  round(engine_load_frac * 100.0, 2),
        "interpolated_gph": round(gph, 3),
    }

# --- UPDATED: display_load_threshold_check (uses session rate or spec) ---
def display_load_threshold_check(user_inputs):
    import streamlit as st
    model = _norm_model(user_inputs.get("eboss_model") or user_inputs.get("model"))
    gen_type = user_inputs.get("eboss_type") or user_inputs.get("gen_type")
    cont_kw = float(user_inputs.get("actual_continuous_load") or user_inputs.get("cont_kw") or 0.0)

    spec = EBOSS_UNITS.get(model, {})
    # prefer computed rate in session, else spec default
    charge_kw = float(
        st.session_state.user_inputs.get("charge_rate_kw") if "user_inputs" in st.session_state else 0.0
        or (spec.get("fh_charge_rate_kw") if gen_type == "Full Hybrid" else spec.get("pm_charge_rate_kw")) or 0
    )
    battery_kwh = float(spec.get("battery_kwh", 0) or 0)

    if cont_kw > charge_kw:
        msg = "❌ Load exceeds EBOSS® charge rate"
    elif cont_kw > charge_kw * 0.9:
        msg = "⚠️ Load > 90% of charge rate"
    elif battery_kwh and cont_kw > battery_kwh * 0.66:
        msg = "ℹ️ Load exceeds efficient battery range"
    else:
        msg = "✅ Load optimized for EBOSS®"
    st.markdown(f"<div class='eboss-card'>{msg}</div>", unsafe_allow_html=True)

# --- UPDATED: calculate_costs_eboss (uses interpolated GPH only) ---
def calculate_costs_eboss(runtime_hr, fuel_gph, fuel_cost_per_gal, rental=0, delivery=0, pm_cost=0):
    gallons = runtime_hr * fuel_gph
    fuel_total = gallons * fuel_cost_per_gal
    co2 = gallons * 22.4 / 2000.0  # tons
    total_cost = float(rental) + float(delivery) + float(pm_cost) + fuel_total
    return round(fuel_total, 2), round(total_cost, 2), round(co2, 4)


# ===========================
# Compare Page
# ===========================
import streamlit as st

S = st.session_state.setdefault("user_inputs", {})

# Default view
st.session_state.setdefault("view_mode", "spec")

# Current model (from earlier modals)
current_model_key = S.get("eboss_model")  # e.g., "EB125 kVA"
if not current_model_key:
    st.info("Please configure a model first (Manual or Load-Based).")
    st.stop()

# Map EBOSS_UNITS keys -> labels used in the provided spec table
MODEL_LABEL = {
    "EB25 kVA":  "EB 25 kVA",
    "EB70 kVA":  "EB 70 kVA",
    "EB125 kVA": "EB 125 kVA",
    "EB220 kVA": "EB 220 kVA",
    "EB400 kVA": "EB 400 kVA",
}
model_label = MODEL_LABEL.get(current_model_key, current_model_key)

# ───────────── Buttons ─────────────
col_spec, col_cost = st.columns([1, 1])
with col_spec:
    if st.button("📊 Spec Comparison"):
        st.session_state.view_mode = "spec"
with col_cost:
    if st.button("💵 Cost Comparison"):
        st.session_state.view_mode = "cost"

# ───────────── Spec Comparison Table ─────────────
if st.session_state.get("view_mode") == "spec":
    st.markdown(
        "<div class='eboss-card'><strong>EBOSS® vs Standard Generator</strong></div>",
        unsafe_allow_html=True
    )

    # NOTE: keeping your provided values; keys align to model_label above
    spec_table = {
        "EB 25 kVA": [
            ("Three-phase",            "30 kVA / 24 kW",          "27.5 kVA / 22 kW"),
            ("Single-phase",           "20 kVA / 16 kW",          "19.75 kVA / 15.8 kW"),
            ("Frequency",              "60 Hz",                    "60 Hz"),
            ("Simultaneous voltage",   "Yes 120v / 240v / 208v / 480v", "No"),
            ("Voltage regulation",     "Adjustable",               "Adjustable"),
            ("Max Intermittent 208v",  "70 A / 20 kW",             "60 A / 17.29 kW"),
            ("Motor start 208v",       "104 A / 30 kW",            "60 A / 17.3 kW"),
            ("Generator Size",         "25 kVA / 20 kW",           "25 kVA / 20 kW"),
            ("Max Continuous @208v",   "70 A / 20.2 kW",           "60 A"),
        ],
        "EB 70 kVA": [
            ("Three-phase",            "70 kVA / 56 kW",           "77 kVA / 62 kW"),
            ("Single-phase",           "47 kVA / 37 kW",           "N/A"),
            ("Frequency",              "60 Hz",                    "60 Hz"),
            ("Simultaneous voltage",   "Yes 120v / 240v / 208v / 480v", "No"),
            ("Voltage regulation",     "Adjustable",               "Adjustable"),
            ("Max Intermittent 208v",  "194 A / 56 kW",            "168 A / 48 kW"),
            ("Motor start 208v",       "291 A / 84 kW",            "200 A / 57 kW"),
            ("Generator Size",         "45 kVA / 36 kW",           "70 kVA / 56 kW"),
            ("Max Continuous @208v",   "119 A / 34.5 kW",          "168 A"),
        ],
        "EB 125 kVA": [
            ("Three-phase",            "125 kVA / 100 kW",         "137.5 kVA / 110 kW"),
            ("Single-phase",           "N/A",                      "89.8 kVA / 79 kW"),
            ("Frequency",              "60 Hz",                    "60 Hz"),
            ("Simultaneous voltage",   "Yes 208v / 480v",          "No"),
            ("Voltage regulation",     "Adjustable",               "Adjustable"),
            ("Max Intermittent 208v",  "345 A / 99.5 kW",          "300 A / 86 kW"),
            ("Motor start 208v",       "532 A / 153 kW",           "300 A / 86 kW"),
            ("Generator Size",         "70 kVA / 56 kW",           "125 kVA / 100 kW"),
            ("Max Continuous @208v",   "167 A / 48 kW",            "300 A"),
        ],
        "EB 220 kVA": [
            ("Three-phase",            "220 kVA / 176 kW",         "242 kVA / 194 kW"),
            ("Single-phase",           "N/A",                      "N/A"),
            ("Frequency",              "60 Hz",                    "60 Hz"),
            ("Simultaneous voltage",   "Yes 208v / 480v",          "No"),
            ("Voltage regulation",     "Adjustable",               "Adjustable"),
            ("Max Intermittent 208v",  "700 A / 201 kW",           "529 A / 152.5 kW"),
            ("Motor start 208v",       "1065 A / 307 kW",          "600 A / 172.9 kW"),
            ("Generator Size",         "125 kVA / 100 kW",         "220 kVA / 176 kW"),
            ("Max Continuous @208v",   "328 A / 94 kW",            "529 A"),
        ],
        "EB 400 kVA": [
            ("Three-phase",            "400 kVA / 320 kW",         "420 kVA / 336 kW"),
            ("Single-phase",           "N/A",                      "N/A"),
            ("Frequency",              "60 Hz",                    "60 Hz"),
            ("Simultaneous voltage",   "Yes 208v / 480v",          "No"),
            ("Voltage regulation",     "Adjustable",               "Adjustable"),
            ("Max Intermittent 208v",  "481 A / 138.5 kW",         "–"),
            ("Motor start 208v",       "1776 A / 511 kW",          "–"),
            ("Generator Size",         "220 kVA / 176 kW",         "220 kVA / 176 kW"),
            ("Max Continuous @208v",   "481 A",                    "481 A"),
        ],
    }

    model_specs = spec_table.get(model_label, [])
    if not model_specs:
        st.warning(f"No comparison rows found for {model_label}.")
    else:
        col1, col2, col3, col4 = st.columns([2, 3, 3, 1])
        for label, eboss_val, std_val in model_specs:
            with col1:
                st.markdown(f"**{label}**")
            with col2:
                st.markdown(eboss_val)
            with col3:
                st.markdown(std_val)
            with col4:
                st.markdown("✅" if eboss_val != std_val else "–")

# ───────────── Cost Comparison Table ─────────────
elif st.session_state.get("view_mode") == "cost":
    with st.form("cost_input_form", clear_on_submit=False):
        st.markdown(
            "<div class='eboss-card'><strong>Enter Cost Inputs</strong></div>",
            unsafe_allow_html=True
        )
        rental    = st.number_input("Monthly Rental Rate ($)",     min_value=0.0, step=10.0,  key="rental_rate")
        fuel_cost = st.number_input("Fuel Cost per Gallon ($)",    min_value=0.0, step=0.01, key="fuel_cost_per_gal")
        delivery  = st.number_input("Delivery Fee ($)",            min_value=0.0, step=10.0,  key="delivery_fee")
        pm_cost   = st.number_input("PM Service Cost ($/mo)",      min_value=0.0, step=10.0,  key="pm_service_cost")
        days_in_month = st.number_input("Days in Month",           min_value=1,   max_value=31, value=30, step=1)
        submit = st.form_submit_button("Calculate")

    if submit:
        # Pull daily runtime (hours) and interpolated fuel (gph) from session
        daily_runtime_hr = float(S.get("engine_run_hours_per_day") or 0.0)
        fuel_gph         = float(S.get("fuel_gph_at_charge") or 0.0)  # interpolation-only

        if daily_runtime_hr <= 0 or fuel_gph <= 0:
            st.warning("Runtime or fuel burn not available. Configure a model and run the charge/runtime calc first.")
            st.stop()

        # Convert to monthly hours
        monthly_runtime_hr = daily_runtime_hr * float(days_in_month)

        # Use your existing costing helper (returns monthly numbers)
        fuel_total, total_cost, co2_output = calculate_costs_eboss(
            monthly_runtime_hr, fuel_gph, fuel_cost, rental, delivery, pm_cost
        )

        st.markdown("<div class='eboss-card'><strong>Monthly Cost Breakdown</strong></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <table style='width:100%; border: 1px solid #ccc; border-collapse: collapse;'>
              <tr><th style='text-align:left;'>Cost Component</th><th style='text-align:right;'>Amount ($)</th></tr>
              <tr><td>Rental</td><td style='text-align:right;'>{:.2f}</td></tr>
              <tr><td>Fuel</td><td style='text-align:right;'>{:.2f}</td></tr>
              <tr><td>Delivery</td><td style='text-align:right;'>{:.2f}</td></tr>
              <tr><td>PM Service</td><td style='text-align:right;'>{:.2f}</td></tr>
              <tr><td><strong>Total Monthly</strong></td><td style='text-align:right;'><strong>{:.2f}</strong></td></tr>
              <tr><td>Est. CO₂ Emissions (tons)</td><td style='text-align:right;'>{:.2f}</td></tr>
            </table>
            """.format(rental, fuel_total, delivery, pm_cost, total_cost, co2_output),
            unsafe_allow_html=True
        )

# If you had a print/export button defined elsewher
try:
    print_button()
except Exception:
    pass


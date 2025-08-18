# utils/keys.py
CANON = {
    # core inputs / normalized
    "model": "eboss_model",
    "type": "eboss_type",
    "pm_gen": "pm_gen",
    "max_cont": "max_continuous_load",
    "max_peak": "max_peak_load",
    "units": "units",
    "voltage": "voltage",
    "actual_cont_kw": "actual_continuous_load",
    "actual_peak_kw": "actual_peak_load",

    # app flags
    "config_mode": "config_mode",
    "page": "page",
    "show_calc": "show_calculator",
    "launch_modal": "launch_tool_modal",

    # spec cache
    "current_spec": "current_spec",
    "current_spec_key": "current_spec_key",
    "spec_cache": "spec_cache",

    # NEW: battery / cycle model
    "battery_life_hours": "battery_life_hours",
    "charge_time_hours": "charge_time_hours",
    "cycles_per_day": "cycles_per_day",

    # NEW: generator runtime per day
    "eboss_runtime_hours": "eboss_gen_runtime_hours_per_day",
    "std_runtime_hours": "std_gen_runtime_hours_per_day",

    # NEW: engine-load % (for interpolation)
    "eboss_eng_load_pct": "eboss_engine_load_percent_interp",
    "std_eng_load_pct": "std_engine_load_percent_interp",

    # NEW: interpolated fuel and rollups
    "eboss_gph": "eboss_gph_interp",
    "std_gph": "std_gph_interp",
    "eboss_gpd": "eboss_gpd",
    "std_gpd": "std_gpd",
    "eboss_gpw": "eboss_gpw",
    "std_gpw": "std_gpw",
    "eboss_gpm": "eboss_gpm",
    "std_gpm": "std_gpm",

    # Optional: standard gen inputs (needed to compute std_* metrics)
    "std_gen_kw": "std_gen_kw_rating",
    "std_gen_kva": "std_gen_kva",
}

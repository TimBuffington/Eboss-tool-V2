# components/modals.py
from __future__ import annotations
import streamlit as st

# Keep this file import-safe; only Streamlit at top level.

PAGE_MAP = {
    "Technical Specs": "pages/01_Tech_Specs.py",
    "Load Based Specs": "pages/02_Load_Based_Specs.py",
    "Compare": "pages/03_Compare.py",
    "Cost Analysis": "pages/05_Cost_Analysis.py",
    "Paralleling": "pages/04_Parallel.py",
}

def _nav_to(page_label: str, *, mode_key: str) -> None:
    """Close modal & navigate."""
    st.session_state["launch_tool_modal"] = False
    target = PAGE_MAP.get(page_label)
    if target and hasattr(st, "switch_page"):
        st.switch_page(target)
    else:
        st.session_state["page"] = page_label
        st.rerun()

def render_modal_nav_grid(*, mode_key: str) -> None:
    """2 columns × 3 rows; last right cell blank (no Troubleshooting)."""
    st.markdown("<div class='cta-scope' style='margin-top:.75rem;'>", unsafe_allow_html=True)
    rows = [
        ("Technical Specs", "Load Based Specs"),
        ("Compare",         "Cost Analysis"),
        ("Paralleling",     None),
    ]
    for left, right in rows:
        c1, c2 = st.columns(2, gap="small")
        with c1:
            st.button(
                left,
                key=f"nav_{left.replace(' ', '_').lower()}_{mode_key}",
                on_click=_nav_to,
                kwargs={"page_label": left, "mode_key": mode_key},
                line
            )
        with c2:
            if right:
                st.button(
                    right,
                    key=f"nav_{right.replace(' ', '_').lower()}_{mode_key}",
                    on_click=_nav_to,
                    kwargs={"page_label": right, "mode_key": mode_key},
                )
            else:
                st.markdown("&nbsp;", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def open_config_modal(mode: str) -> None:
    """Unified configuration modal with strict sizing validation and requested layout."""
    title = f"EBOSS Configuration — {mode.title()}"

    def _body() -> None:
        # Lazy imports (keeps this file import-safe)
        try:
            from utils.data import SPECS
        except Exception:
            st.error("Static specs (SPECS) not available.")
            return
        try:
            from utils.spec_store import compute_and_store_spec
        except Exception:
            compute_and_store_spec = None

        # ---------- helpers ----------
        kva_sizes = sorted(SPECS.keys())
        model_by_kva = {kva: rec.get("eboss_model") for kva, rec in SPECS.items()}
        kva_by_model = {rec.get("eboss_model"): kva for kva, rec in SPECS.items()}
        all_models = [model_by_kva[k] for k in kva_sizes if model_by_kva.get(k)]

        def allowed_models_for(cont_kw: float, peak_kw: float) -> list[str]:
            """Models where cont<=98% of max_cont and peak<=max_peak."""
            ok = []
            for kva in kva_sizes:
                rec = SPECS[kva]
                max_cont = float(rec.get("max_cont_kw", 0))
                max_peak = float(rec.get("max_peak_kw", 0))
                if (cont_kw <= 0.98 * max_cont) and (peak_kw <= max_peak):
                    ok.append(rec.get("eboss_model"))
            return ok

        # ---------- layout: 3 columns ----------
        col1, col2, col3 = st.columns(3)

        # Defaults / current state
        units_default = st.session_state.get("units", "kW")
        voltage_default = st.session_state.get("voltage", "480")
        eboss_type_default = st.session_state.get("eboss_type", "Full Hybrid")
        eboss_model_default = st.session_state.get("eboss_model", all_models[0] if all_models else "")
        pm_gen_default = st.session_state.get("pm_gen")

        # --------- Column 2 (loads) so we can filter models right away ---------
        with col2:
            cont = st.number_input(
                "Max Continuous Load (kW)",
                min_value=0.0, step=1.0, format="%g",
                key="max_continuous_load",
            )
            peak = st.number_input(
                "Max Peak Load (kW)",
                min_value=0.0, step=1.0, format="%g",
                key="max_peak_load",
            )

        # --------- Column 3 (units/voltage) ----------
        with col3:
            units = st.selectbox("Units", options=["kW", "Amps"], index=0 if units_default=="kW" else 1, key="units")
            voltage = st.selectbox("Voltage", options=["120", "208", "240", "480"], index=["120","208","240","480"].index(voltage_default) if voltage_default in ["120","208","240","480"] else 3, key="voltage")

        # Convert amps→kW if needed (use PF=0.8 by default; adjust if you later expose it)
        sqrt3 = 1.732
        pf = 0.8
        try:
            v = float(voltage)
        except Exception:
            v = 0.0

        if units == "Amps" and v > 0:
            actual_cont_kw = (float(cont) * v * sqrt3 * pf) / 1000.0
            actual_peak_kw = (float(peak) * v * sqrt3 * pf) / 1000.0
        else:
            actual_cont_kw = float(cont)
            actual_peak_kw = float(peak)

        st.session_state["actual_continuous_load"] = actual_cont_kw
        st.session_state["actual_peak_load"] = actual_peak_kw

        # Determine which models are allowed for current loads (for filtering)
        allowed_models = allowed_models_for(actual_cont_kw, actual_peak_kw) if (actual_cont_kw > 0 or actual_peak_kw > 0) else all_models

        # --------- Column 1 (model/type/pm_gen) ----------
        with col1:
            # EBOSS Model (Row 1) — filtered by loads
            if not allowed_models:
                st.error("No EBOSS model can meet the entered continuous/peak load. Lower the load or parallel units.")
                # keep a disabled field with previous or first model just for UI stability
                st.selectbox("EBOSS® Model", options=all_models, index=all_models.index(eboss_model_default) if eboss_model_default in all_models else 0, key="eboss_model", disabled=True)
                eboss_model = st.session_state["eboss_model"]
            else:
                # If current selection is invalid, auto-correct to the first valid model
                if eboss_model_default not in allowed_models:
                    if eboss_model_default:
                        st.info(f"Selected model **{eboss_model_default}** does not meet the entered load. Adjusted to **{allowed_models[0]}**.")
                    eboss_model_default = allowed_models[0]
                eboss_model = st.selectbox(
                    "EBOSS® Model",
                    options=allowed_models,
                    index=allowed_models.index(eboss_model_default) if eboss_model_default in allowed_models else 0,
                    key="eboss_model",
                )

            # EBOSS Type (Row 2)
            if mode == "manual":
                eboss_type = st.selectbox(
                    "EBOSS® Type",
                    options=["Full Hybrid", "Power Module"],
                    index=0 if eboss_type_default == "Full Hybrid" else 1,
                    key="eboss_type",
                )
            else:
                eboss_type = "Full Hybrid"
                st.selectbox("EBOSS® Type", options=["Full Hybrid"], index=0, key="eboss_type", disabled=True)

            # PM Gen (Row 3) — only if Power Module
            if st.session_state.get("eboss_type") == "Power Module":
                pm_options = kva_sizes
                st.selectbox(
                    "Power Module — Generator Size (kVA)",
                    options=pm_options,
                    index=pm_options.index(pm_gen_default) if pm_gen_default in pm_options else 0,
                    key="pm_gen",
                )
            else:
                # clear any legacy value to avoid accidental use downstream
                st.session_state["pm_gen"] = None
                st.text_input("Power Module — Generator Size (kVA)", value="", key="pm_gen_display", disabled=True)

        # -------- validation: hard block undersized picks --------
        if eboss_model:
            rec = SPECS.get(kva_by_model.get(eboss_model, -1), {})
            max_cont = float(rec.get("max_cont_kw", 0))
            max_peak = float(rec.get("max_peak_kw", 0))

            cont_ok = actual_cont_kw <= 0.98 * max_cont if max_cont > 0 else True
            peak_ok = actual_peak_kw <= max_peak if max_peak > 0 else True

            if not cont_ok or not peak_ok:
                st.error(
                    f"**{eboss_model}** cannot support the entered load. "
                    f"(Max continuous ≤ **{0.98*max_cont:.1f} kW**, Max peak ≤ **{max_peak:.1f} kW**)"
                )
                render_modal_nav_grid(mode_key=mode)
                return

        # -------- compute + cache spec --------
        if compute_and_store_spec and eboss_model and st.session_state.get("eboss_type"):
            try:
                compute_and_store_spec(
                    model=eboss_model,
                    type=st.session_state["eboss_type"],
                    cont_kw=actual_cont_kw,
                    gen_kw=None,
                    size_kva=None,
                    pm_gen=st.session_state.get("pm_gen"),
                )
                st.success(f"Configured: {eboss_model} ({st.session_state['eboss_type']}) — {actual_cont_kw:g} kW")
            except Exception as e:
                st.error(f"Failed to compute spec: {e}")

        # -------- bottom nav --------
        render_modal_nav_grid(mode_key=mode)

    # modal/dialog fallback for version compatibility
    if hasattr(st, "modal"):
        with st.modal(title, key=f"cfg_modal_{mode}"):
            _body()
    elif hasattr(st, "dialog"):
        @st.dialog(title)
        def _dlg():
            _body()
        _dlg()
    else:
        st.warning("Your Streamlit version lacks modal/dialog; rendering inline.")
        _body()


    def _body() -> None:
        """
        Full UI for Manual / Load-Based / Fuel-Efficient.
        - No submit button: as soon as Units AND Voltage are set, we validate & compute.
        - Keys are identical across modes.
        """
        # ---- Lazy imports (avoid import-time crashes) ------------------------
        try:
            from utils.data import SPECS  # keyed by kVA -> dict(rec)
        except Exception:
            SPECS = {}
        try:
            from utils.sizing import gph_for, eboss_defined_charge_rate_kw
        except Exception:
            gph_for = None
            eboss_defined_charge_rate_kw = None
        try:
            from utils.spec_store import compute_and_store_spec
        except Exception:
            compute_and_store_spec = None

        # ---- Helpers bound to current data -----------------------------------
        # Lists/models (sorted by kVA)
        kva_sizes = sorted(SPECS.keys())
        model_by_kva = {kva: rec.get("eboss_model") for kva, rec in SPECS.items()}
        kva_by_model = {rec.get("eboss_model"): kva for kva, rec in SPECS.items()}
        model_list = [model_by_kva[k] for k in kva_sizes if model_by_kva.get(k)]

        def _auto_pick_model_for_load(cont_kw: float, peak_kw: float) -> str | None:
            # Find first model that satisfies 98% continuous and peak constraints
            for kva in kva_sizes:
                rec = SPECS[kva]
                max_cont = float(rec.get("max_cont_kw", 0))
                max_peak = float(rec.get("max_peak_kw", 0))
                if cont_kw <= 0.98 * max_cont and peak_kw <= max_peak:
                    return rec.get("eboss_model")
            return None

        def _auto_pick_model_by_efficiency(cont_kw: float) -> str | None:
            """
            Choose the smallest model where battery_kwh >= cont_kw * 1.33,
            then among that model and larger ones, compute daily GPD using
            EBOSS runtime math, pick the minimum.
            """
            if cont_kw <= 0:
                return None
            candidates = []
            for kva in kva_sizes:
                rec = SPECS[kva]
                kwh = float(rec.get("kwh", 0))
                if kwh >= cont_kw * 1.33:
                    candidates.append(rec.get("eboss_model"))
            if not candidates:
                return None

            best_model = None
            best_gpd = None

            for m in candidates:
                # charge rate & gph
                charge_kw = float(eboss_defined_charge_rate_kw(m, "Full Hybrid") or 0.0) if eboss_defined_charge_rate_kw else 0.0
                if charge_kw <= 0:
                    continue
                # EBOSS rule for GPH
                gph_tuple = gph_for(model=m, type="Full Hybrid", cont_kw=cont_kw) if gph_for else (0.0, 0.0, 0)
                gph = float(gph_tuple[0])

                # Runtime math
                kwh = float(SPECS[kva_by_model[m]].get("kwh", 0))
                if kwh <= 0:
                    continue
                battery_life = kwh / cont_kw
                charge_time = kwh / charge_kw
                if battery_life + charge_time <= 0:
                    continue
                cycles_per_day = 24.0 / (battery_life + charge_time)
                runtime_hrs = charge_time * cycles_per_day  # gen runtime
                gpd = gph * runtime_hrs

                if best_gpd is None or gpd < best_gpd:
                    best_gpd = gpd
                    best_model = m

            return best_model

        # ---- Shared UI fields (identical keys across modes) ------------------
        st.markdown("<div class='cta-scope'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)

        # EBOSS Type (locked for auto modes)
        with c1:
            if mode == "manual":
                eboss_type = st.selectbox(
                    "EBOSS® Type",
                    options=["Full Hybrid", "Power Module"],
                    index=0 if st.session_state.get("eboss_type") == "Full Hybrid" else 1 if st.session_state.get("eboss_type") == "Power Module" else 0,
                    key="eboss_type",
                )
            else:
                eboss_type = "Full Hybrid"
                st.selectbox("EBOSS® Type", options=["Full Hybrid"], index=0, key="eboss_type", disabled=True)

        # EBOSS Model (manual select or auto-filled)
        with c2:
            if mode == "manual":
                st.selectbox(
                    "EBOSS® Model",
                    options=model_list,
                    index=model_list.index(st.session_state["eboss_model"]) if st.session_state.get("eboss_model") in model_list else 0,
                    key="eboss_model",
                )
            else:
                # placeholder; will fill once cont/peak compute
                st.text_input("EBOSS® Model (auto)", value=st.session_state.get("eboss_model", ""), key="eboss_model", disabled=True)

        # PM Generator kVA (only visible when Power Module)
        with c3:
            if st.session_state.get("eboss_type") == "Power Module":
                pm_options = kva_sizes  # e.g., [25,45,65,125,220]
                st.selectbox(
                    "Power Module — Generator Size (kVA)",
                    options=pm_options,
                    index=pm_options.index(st.session_state["pm_gen"]) if st.session_state.get("pm_gen") in pm_options else 0,
                    key="pm_gen",
                )
            else:
                st.text_input("Power Module — Generator Size (kVA)", value="", key="pm_gen_display", disabled=True)
                # clear any old pm_gen if switching away
                st.session_state["pm_gen"] = st.session_state.get("pm_gen", None)

        st.markdown("</div>", unsafe_allow_html=True)

        # Units / Voltage / Loads
        st.markdown("<div class='cta-scope'>", unsafe_allow_html=True)
        u1, u2, u3 = st.columns(3)
        with u1:
            units = st.selectbox("Units", options=["kW", "Amps"], key="units")
        with u2:
            voltage = st.selectbox("Voltage", options=["120", "208", "240", "480"], key="voltage")
        with u3:
            pf = st.number_input("Power Factor (Amps→kW)", min_value=0.1, max_value=1.0, value=0.8, step=0.05, key="power_factor")

        l1, l2 = st.columns(2)
        with l1:
            st.number_input(
                "Max Continuous Load",
                min_value=0.0, step=1.0, format="%g",
                key="max_continuous_load"
            )
        with l2:
            st.number_input(
                "Max Peak Load",
                min_value=0.0, step=1.0, format="%g",
                key="max_peak_load"
            )
        st.markdown("</div>", unsafe_allow_html=True)

        # ---- Reactive computation gates --------------------------------------
        # Require Units AND Voltage to be present
        ready = bool(units and voltage)

        # Convert Amps to kW if needed (3φ default: *sqrt(3))
        try:
            v = float(voltage)
        except Exception:
            v = 0.0
        sqrt3 = 1.732

        max_cont = float(st.session_state.get("max_continuous_load") or 0.0)
        max_peak = float(st.session_state.get("max_peak_load") or 0.0)

        if units == "Amps" and v > 0:
            pf_val = float(pf or 0.8)
            actual_cont_kw = (max_cont * v * sqrt3 * pf_val) / 1000.0
            actual_peak_kw = (max_peak * v * sqrt3 * pf_val) / 1000.0
        else:
            actual_cont_kw = max_cont
            actual_peak_kw = max_peak

        st.session_state["actual_continuous_load"] = actual_cont_kw
        st.session_state["actual_peak_load"] = actual_peak_kw

        # Show a gentle hint until ready
        if not ready:
            st.info("Select **Units** and **Voltage** to enable sizing and calculations.")
            render_modal_nav_grid(mode_key=mode)
            return

        # Require a positive load to proceed
        if actual_cont_kw <= 0:
            st.warning("Enter a **Max Continuous Load** > 0 to run sizing and fuel math.")
            render_modal_nav_grid(mode_key=mode)
            return

        # ---- Auto model selection for non-manual modes -----------------------
        if mode == "load_based":
            picked = _auto_pick_model_for_load(actual_cont_kw, actual_peak_kw)
            if picked:
                st.session_state["eboss_model"] = picked
            else:
                st.error("No EBOSS model meets the continuous/peak constraints. Adjust the load or try Manual.")
        elif mode == "fuel_eff":
            picked = _auto_pick_model_by_efficiency(actual_cont_kw)
            if picked:
                st.session_state["eboss_model"] = picked
            else:
                st.error("No EBOSS model satisfies the battery ≥ 1/3 continuous rule. Try Manual.")

        # ---- Compute & cache merged spec (incl. interpolated GPH) ------------
        model = st.session_state.get("eboss_model")
        eboss_type = st.session_state.get("eboss_type")
        pm_gen_val = st.session_state.get("pm_gen") if eboss_type == "Power Module" else None

        if not model or not eboss_type:
            st.warning("Select an EBOSS **Type** and **Model** to continue.")
            render_modal_nav_grid(mode_key=mode)
            return

        try:
            if compute_and_store_spec:
                compute_and_store_spec(
                    model=model,
                    type=eboss_type,
                    cont_kw=actual_cont_kw,
                    gen_kw=None,
                    size_kva=None,
                    pm_gen=pm_gen_val,
                )
                st.success(f"Configured: {model} ({eboss_type}) — {actual_cont_kw:g} kW")
        except Exception as e:
            st.error(f"Failed to compute spec: {e}")

        # ---- Bottom nav grid --------------------------------------------------
        render_modal_nav_grid(mode_key=mode)

    # Version-safe modal
    if hasattr(st, "modal"):
        with st.modal(title, key=f"cfg_modal_{mode}"):
            _body()
    elif hasattr(st, "dialog"):
        @st.dialog(title)
        def _dlg():
            _body()
        _dlg()
    else:
        st.warning("Your Streamlit version lacks modal/dialog; rendering inline.")
        _body()

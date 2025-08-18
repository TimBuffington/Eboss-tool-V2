# pages/01_Tech_Specs.py
import streamlit as st
from utils.data import EBOSS_SPECS          # your dict by model → {label: value}
from utils.spec_store import compute_and_store_spec

# ------ Section headers you gave ------
SPEC_LABELS = [
    "Battery Capacity",
    "Inverter",
    "Voltage Options",
    "Weight",
    "Dimensions",
    "Warranty",
]

# ------ Map spec labels (left text) → sections (adjust as needed) ------
SECTION_MAP = {
    # Battery Capacity
    "Battery capacity": "Battery Capacity",
    "Battery chemistry": "Battery Capacity",
    "Battery type": "Battery Capacity",
    "Energy throughput": "Battery Capacity",
    "Cycle life @ 77°F": "Battery Capacity",
    "Cycle life @ 100°F": "Battery Capacity",
    "Life @ 3kW load (100°F)": "Battery Capacity",

    # Inverter
    "Inverter output max": "Inverter",
    "Inverter cold start (min)": "Inverter",
    "Parallel capability": "Inverter",
    "Charge time (no load)": "Inverter",

    # Voltage Options
    "Frequency": "Voltage Options",
    "Simultaneous voltage": "Voltage Options",
    "Voltage regulation": "Voltage Options",
    "Three-phase": "Voltage Options",
    "Single-phase": "Voltage Options",
    "Three-phase output": "Voltage Options",
    "Single-phase output": "Voltage Options",
    "Amp-load @ 208V": "Voltage Options",
    "Amp-load @ 480V": "Voltage Options",
    "Motor start (3 sec @ 208V)": "Voltage Options",
    "Motor start (3 sec @ 480V)": "Voltage Options",

    # Weight
    "EBOSS weight only": "Weight",
    "Total weight (no fuel / full)": "Weight",

    # Dimensions
    "EBOSS only (L×W×H)": "Dimensions",
    "With trailer & generator": "Dimensions",
    "Fuel tank capacity": "Dimensions",   # grouped here

    # Warranty (placeholder below)
}

# ------ Styling (mobile-friendly) ------
st.markdown("""
<style>
.spec-title { text-align:center; margin: .25rem 0 1rem; }
.spec-title h2 { margin:.1rem 0; }
.spec-title .sub { opacity:.85; }

.spec-section { margin: 18px 0 10px; padding: 8px 12px; border-radius: 10px;
  background: rgba(0,0,0,.35); border: 1px solid rgba(255,255,255,.12); }
.spec-section h3 { margin: 0; font-size: 1.05rem; letter-spacing: .5px; }

.specs-col { display:flex; flex-direction:column; gap:8px; }
.spec-item { display:flex; justify-content:space-between; gap:16px;
  padding:10px 12px; border-radius:10px; background: rgba(0,0,0,.25);
  border: 1px solid rgba(255,255,255,.08); }
.spec-item .label { opacity:.9; }
.spec-item .value { font-weight:700; text-align:right; }
</style>
""", unsafe_allow_html=True)

def _bucket_by_section(model_specs: dict):
    buckets = {sec: [] for sec in SPEC_LABELS}
    for label, value in model_specs.items():
        sec = SECTION_MAP.get(label)
        if sec:
            buckets[sec].append((label, value))
    for sec in buckets:
        buckets[sec].sort(key=lambda x: x[0])
    return buckets

def _render_two_col_section(section_name: str, items):
    import math
    anchor = "sec-" + section_name.lower().replace(" ", "-")
    st.markdown(f"<div id='{anchor}' class='spec-section'><h3>{section_name}</h3></div>", unsafe_allow_html=True)
    mid = math.ceil(len(items)/2) if items else 0
    left_items, right_items = items[:mid], items[mid:]
    colL, colR = st.columns(2, gap="large")
    with colL:
        st.markdown("<div class='specs-col'>", unsafe_allow_html=True)
        for label, value in left_items:
            st.markdown(f"<div class='spec-item'><span class='label'>{label}</span><span class='value'>{value}</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with colR:
        st.markdown("<div class='specs-col'>", unsafe_allow_html=True)
        for label, value in right_items:
            st.markdown(f"<div class='spec-item'><span class='label'>{label}</span><span class='value'>{value}</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

def _open_change_model_modal(models):
    with st.modal("Change EBOSS Model", key="change_model_modal"):
        cols = st.columns(3)
        for i, name in enumerate(models):
            with cols[i % 3]:
                if st.button(name, key=f"pick_{name}"):
                    # update model selection
                    st.session_state["eboss_model"] = name
                    # OPTIONAL: recompute merged spec with current load/type if present
                    cont_kw = float(st.session_state.get("actual_continuous_load") or 0)
                    eb_type = st.session_state.get("eboss_type", "Full Hybrid")
                    pm_gen  = st.session_state.get("pm_gen")
                    if cont_kw > 0:
                        compute_and_store_spec(
                            model=name, type=eb_type, cont_kw=cont_kw,
                            pm_gen=pm_gen,
                            size_kva=pm_gen if eb_type == "Power Module" else None,
                            gen_kw=None,
                        )
                    st.rerun()  # closes modal & refreshes page

# ===== Page render =====
model = st.session_state.get("eboss_model")
eboss_type = st.session_state.get("eboss_type")

if not model or model not in EBOSS_SPECS:
    st.warning("Select an EBOSS configuration from the modal to view Technical Specs.")
else:
    # Top: model & type (centered)
    st.markdown(
        f"<div class='spec-title'><h2>{model}</h2><div class='sub'>{eboss_type or ''}</div></div>",
        unsafe_allow_html=True
    )

    # Row: Jump-to (left) + Change Model (right)
    c1, c2 = st.columns([2,1])
    with c1:
        jump = st.selectbox("Jump to", SPEC_LABELS, index=0, key="tech_jump")
        if jump:
            anchor = "sec-" + jump.lower().replace(" ", "-")
            st.markdown(
                f"<script>var el=document.getElementById('{anchor}'); if(el) el.scrollIntoView({{behavior:'smooth'}});</script>",
                unsafe_allow_html=True
            )
    with c2:
        if st.button("Change EBOSS Model", key="btn_change_model"):
            _open_change_model_modal(list(EBOSS_SPECS.keys()))

    # Sections: labels fixed, values per selected model
    buckets = _bucket_by_section(EBOSS_SPECS[model])
    for sec in SPEC_LABELS:
        items = buckets.get(sec, [])
        if sec == "Warranty" and not items:
            items = [("Warranty", "Contact ANA Energy for current warranty terms")]
        _render_two_col_section(sec, items)

import io, json, re, requests, streamlit as st
from pathlib import Path
from typing import Optional, Tuple, List, Dict

# ---- (copy these from your app; unchanged) ----
UI_EQUIPMENTS = ["AFE", "DC-DC", "Grid"]
EQUIP_NAME_MAP = {"AFE Inverter":"AFE","DC-DC Converter":"DC-DC","Grid Inverter":"Grid"}

LOCAL_CANDIDATES = [
    Path.cwd() / "inverter_fault_codes_formatted.json",
    Path.cwd() / "data" / "inverter_fault_codes_formatted.json",
    Path.cwd() / "inverter_fault_codes.json",
    Path.cwd() / "data" / "inverter_fault_codes.json",
]
REMOTE_CANDIDATES = [
    "https://raw.githubusercontent.com/TimBuffington/troubleshooting/refs/heads/main/inverter_fault_codes_formatted.json",
    "https://raw.githubusercontent.com/TimBuffington/troubleshooting/main/inverter_fault_codes_formatted.json",
    "https://raw.githubusercontent.com/TimBuffington/troubleshooting/refs/heads/main/inverter_fault_codes.json",
    "https://raw.githubusercontent.com/TimBuffington/troubleshooting/main/inverter_fault_codes.json",
]

def parse_to_code_only(text: Optional[str]) -> Optional[str]:
    if not text: return None
    m = re.findall(r"\bF\d+\b", text.upper())
    return m[-1] if m else None

def normalize_user_input_code(s: str) -> Optional[str]:
    if not s: return None
    s = s.strip().upper()
    code = parse_to_code_only(s)
    if code: return code
    if s.isdigit(): return f"F{s}"
    return s

def bullets_from_text(s: str) -> List[str]:
    if not s: return []
    parts = re.split(r"[;\.\n]+", s)
    out = []
    for p in parts:
        t = " ".join(p.strip().split())
        if t: out.append(re.sub(r"\b(\w+)\s+\1\b", r"\1", t, flags=re.IGNORECASE))
    return out

def try_load_local() -> Optional[List[dict]]:
    for p in LOCAL_CANDIDATES:
        try:
            if p.exists():
                return json.loads(Path(p).read_text(encoding="utf-8"))
        except Exception:
            pass
    return None

def try_load_remote() -> Optional[List[dict]]:
    for url in REMOTE_CANDIDATES:
        try:
            r = requests.get(url, timeout=10)
            if r.ok: return r.json()
        except Exception:
            pass
    return None

def parse_rows_to_faults(rows: List[dict]) -> Dict[str, Dict[str, dict]]:
    faults: Dict[str, Dict[str, dict]] = {"AFE": {}, "DC-DC": {}, "Grid": {}}
    for r in rows:
        inv = (r.get("Inverter_Name") or "").strip()
        fc  = (r.get("Fault_Code") or "").strip()
        if inv and fc:
            ui = EQUIP_NAME_MAP.get(inv); code = parse_to_code_only(fc)
            if ui and code:
                faults[ui][code] = {
                    "equipment": ui, "code": code, "fault_code_full": fc,
                    "description": (r.get("Description") or "").strip(),
                    "causes": (r.get("Possible_Causes") or "").strip(),
                    "fixes": (r.get("Recommended_Fixes") or "").strip(),
                }
            continue
        fc = (r.get("Fault Code") or "").strip()
        if fc:
            code = parse_to_code_only(fc)
            if not code: continue
            if fc.startswith("AFE"): ui="AFE"
            elif fc.startswith("DC-DC"): ui="DC-DC"
            elif fc.startswith("Grid Inverter"): ui="Grid"
            else: continue
            desc = (r.get("Description") or "").strip()
            faults[ui][code] = {"equipment": ui, "code": code, "fault_code_full": fc,
                                "description": desc, "causes": "", "fixes": ""}
    return faults

def load_faults_with_fallback():
    rows = try_load_local()
    if rows is None: rows = try_load_remote()
    return (parse_rows_to_faults(rows), ("local" if rows else "missing")) if rows else (None, "missing")

def find_fault(faults, selected_equip, code):
    primary = faults.get(selected_equip, {}).get(code)
    alts = [] if primary else [t[code] for k,t in faults.items() if k!=selected_equip and code in t]
    return primary, alts

# ---- inline renderer (no page_config, no global background CSS) ----
def render_fault_code_lookup_inline():
    faults, origin = load_faults_with_fallback()
    st.markdown("""
    <style>
      .fc-card {border:1px solid #939598;border-radius:10px;padding:12px;background:rgba(0,0,0,.35);}
    </style>""", unsafe_allow_html=True)

    st.markdown("### 🔎 EBOSS® Fault Code Lookup")
    if not faults:
        st.error("Fault code data file not found.")
        up = st.file_uploader("Upload inverter fault JSON", type=["json"], key="fc_upload_inline")
        if up:
            try:
                rows = json.load(io.StringIO(up.getvalue().decode("utf-8")))
                faults = parse_rows_to_faults(rows)
                st.success("Loaded data from uploaded file.")
            except Exception as e:
                st.exception(e)
        if not faults: return

    with st.form("fc_form_inline", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            selected = st.selectbox("Equipment", UI_EQUIPMENTS, key="fc_equipment_inline")
        with c2:
            user_code_raw = st.text_input("Fault Code", placeholder="e.g., F91", key="fc_code_raw_inline")
        submitted = st.form_submit_button("Search")

    if not submitted:
        return

    code = normalize_user_input_code(user_code_raw)
    if not code:
        st.error("Please enter a fault code (e.g., F91)."); return

    primary, alts = find_fault(faults, selected, code)
    if primary:
        _render_result_inline(primary)
    elif alts:
        st.info(f"Not in {selected}, but found in: {', '.join(sorted({a['equipment'] for a in alts}))}. Showing first match.")
        _render_result_inline(alts[0])
    else:
        st.warning(f"No results found for {code} in any dictionary.")

def _render_result_inline(entry: dict):
    st.success(f"Found {entry['code']} in {entry['equipment']}")
    if entry.get("description"):
        st.markdown(f"<div class='fc-card'><b>Description</b>: {entry['description']}</div>", unsafe_allow_html=True)
    causes = bullets_from_text(entry.get("causes", ""))
    fixes  = bullets_from_text(entry.get("fixes", ""))
    if causes:
        st.markdown("**Possible causes:**")
        for c in causes: st.markdown(f"- {c}")
    if fixes:
        st.markdown("**Recommended fixes:**")
        for f in fixes: st.markdown(f"- {f}")


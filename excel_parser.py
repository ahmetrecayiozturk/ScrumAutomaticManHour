import re
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple

ALIASES = {
    "task_key": ["taskkey", "task_key", "id", "issuekey", "jirakey", "key", "task id"],
    "module": ["modul", "module", "modül", "feature", "area", "modulfeature", "modülfeature"],
    "entity_name": ["entityadi", "entity_adı", "entity", "entity name", "tablo", "table", "model"],
    "related_entity_count": ["iliskilientitysayisi", "relatedentitycount", "related_entity_count", "entity sayısı", "entity sayisi"],
    "relation_count": ["iliskisayisi", "relationcount", "relation_count", "iliski", "ilişki", "relations", "ilişki sayısı", "iliski sayisi"],
    "custom_endpoint_count": ["cruddisiozelendpointsayisi", "customendpointcount", "custom_endpoint_count", "crud dısı ozel endpoint sayisi", "crud dışı özel endpoint sayısı"],
    "screen_count": ["ekransayisi", "screencount", "screen_count", "sayfa", "page count", "ekransayfasayisi", "ekran/sayfa sayısı", "ekran/sayfa sayisi"],
    "crud_screen_hours": ["crud_ekransaat", "crud_ekran_saat", "crud_screen_hours", "crud ekran/sayfa için adam/saat", "crud ekran/sayfa icin adam/saat", "crud ekran/sayfa için adamsaat"],
    "api_integration_hours": ["api_integration", "api integration", "integration", "api_hours", "api entegrasyon (frontend)", "api entegrasyon frontend", "api entegrasyon"],
    "ui_test_hours": ["ui_test", "ui test", "ui_test_hours", "responsive & ui testleri", "responsive ui testleri"],
    "complexity_factor": ["karmasiklikfaktoru", "complexity", "complexity_factor", "zorluk", "difficulty", "karmaşıklık faktörü", "karmasiklik faktorü", "karmasiklik faktoru"],
}

PREFERRED_SHEETS = ["Calculations", "Calculation", "Tasks", "Backlog"]

def _normalize_col(c: str) -> str:
    c = str(c).strip().lower()
    c = re.sub(r"[^a-z0-9_çğıöşü]+", "", c)
    c = c.replace("ı", "i").replace("ğ", "g").replace("ş", "s").replace("ü", "u").replace("ö", "o").replace("ç", "c")
    return c

def detect_columns(df: pd.DataFrame) -> Dict[str, str]:
    if not hasattr(df, "columns"):
        raise TypeError(f"detect_columns expected DataFrame, got {type(df)}")
    norm_cols = {_normalize_col(c): c for c in df.columns}
    detected: Dict[str, str] = {}
    for canonical, alias_list in ALIASES.items():
        found = None
        for a in alias_list:
            na = _normalize_col(a)
            if na in norm_cols:
                found = norm_cols[na]
                break
            for ncol, orig in norm_cols.items():
                if na and (na in ncol or ncol in na):
                    found = orig
                    break
            if found:
                break
        if found:
            detected[canonical] = found
    return detected

def _to_int(x, default=0) -> int:
    if pd.isna(x) or x == "":
        return default
    try:
        s = str(x).strip().replace(",", ".")
        return int(float(s))
    except Exception:
        return default

def _to_float(x, default=None):
    if pd.isna(x) or x == "":
        return default
    try:
        s = str(x).strip().replace(",", ".")
        return float(s)
    except Exception:
        return default

def _to_str(x, default="") -> str:
    if pd.isna(x) or x == "":
        return default
    return str(x).strip()

def _select_sheet(excel_path: str, sheet_name: Optional[str]) -> Optional[str]:
    if sheet_name:
        return sheet_name
    xls = pd.ExcelFile(excel_path, engine="openpyxl")
    for s in PREFERRED_SHEETS:
        if s in xls.sheet_names:
            return s
    return xls.sheet_names[0] if xls.sheet_names else None

def read_excel_to_normalized_json(excel_path: str, sheet_name: Optional[str] = None) -> Tuple[List[Dict[str, Any]], pd.DataFrame, Dict[str, str]]:
    chosen_sheet = _select_sheet(excel_path, sheet_name)
    df = pd.read_excel(excel_path, sheet_name=chosen_sheet, engine="openpyxl")
    
    if isinstance(df, dict):
        if chosen_sheet and chosen_sheet in df:
            df = df[chosen_sheet]
        else:
            df = df[list(df.keys())[0]]

    colmap = detect_columns(df)

    def get(row, canonical, default=None):
        if canonical not in colmap:
            return default
        return row[colmap[canonical]]

    rows: List[Dict[str, Any]] = []
    for _, r in df.iterrows():
        item = {
            "task_key": _to_str(get(r, "task_key", ""), ""),
            "module": _to_str(get(r, "module", ""), ""),
            "entity_name": _to_str(get(r, "entity_name", ""), ""),
            "related_entity_count": _to_int(get(r, "related_entity_count", 0), 0),
            "relation_count": _to_int(get(r, "relation_count", 0), 0),
            "custom_endpoint_count": _to_int(get(r, "custom_endpoint_count", 0), 0),
            "screen_count": _to_int(get(r, "screen_count", 0), 0),
            "crud_screen_hours": _to_float(get(r, "crud_screen_hours", None), None),
            "api_integration_hours": _to_float(get(r, "api_integration_hours", None), None),
            "ui_test_hours": _to_float(get(r, "ui_test_hours", None), None),
            "complexity_factor": _to_float(get(r, "complexity_factor", None), None),
            "raw": {k: (None if pd.isna(v) else v) for k, v in r.to_dict().items()}
        }
        if not (item["task_key"] or item["module"] or item["entity_name"] or item["screen_count"] or item["custom_endpoint_count"]):
            continue
        if (item["module"] or "").strip().lower() == "total":
            continue
        rows.append(item)
    return rows, df, colmap
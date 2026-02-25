import json
import pandas as pd
from typing import List, Dict, Any

RENAME_TO_BUSINESS = {
    "task_key": "TaskKey",
    "module": "Modül / Feature",
    "entity_name": "EntityAdı",
    "related_entity_count": "Entity Sayısı",
    "relation_count": "İlişki Sayısı",
    "custom_endpoint_count": "CRUD Dışı Özel Endpoint Sayısı",
    "screen_count": "Ekran/Sayfa Sayısı",
    "crud_screen_hours": "CRUD Ekran/Sayfa için Adam/Saat",
    "api_integration_hours": "API Entegrasyon (Frontend)",
    "ui_test_hours": "Responsive & UI Testleri",
    "complexity_factor": "Karmaşıklık Faktörü",
    "task_type": "Task Type",
    "backend_estimate": "Adam/Saat Tahmini (BE)",
    "frontend_estimate": "Tahmini Adam/Saat (FE)",
    "total_estimate": "Tahmini Adam/Saat",
    "Actual_BE": "Actual_BE",
    "Actual_FE": "Actual_FE",
}

BUSINESS_COLUMNS_ORDER = [
    "TaskKey",
    "Modül / Feature",
    "EntityAdı",
    "Entity Sayısı",
    "İlişki Sayısı",
    "CRUD Dışı Özel Endpoint Sayısı",
    "Ekran/Sayfa Sayısı",
    "Karmaşıklık Faktörü",
    "CRUD Ekran/Sayfa için Adam/Saat",
    "API Entegrasyon (Frontend)",
    "Responsive & UI Testleri",
    "Task Type",
    "Adam/Saat Tahmini (BE)",
    "Tahmini Adam/Saat (FE)",
    "Tahmini Adam/Saat",
    "Actual_BE",
    "Actual_FE",
    "raw_json",
]

def export_excel_and_json(rows: List[Dict[str, Any]], excel_out: str, json_out: str) -> None:
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    prepared = []
    for r in rows:
        x = dict(r)
        x.setdefault("Actual_BE", None)
        x.setdefault("Actual_FE", None)
        x["raw_json"] = json.dumps(x.get("raw", {}), ensure_ascii=False)
        x.pop("raw", None)
        prepared.append(x)

    df = pd.DataFrame(prepared)
    df = df.rename(columns=RENAME_TO_BUSINESS)

    for c in BUSINESS_COLUMNS_ORDER:
        if c not in df.columns:
            df[c] = None

    df = df[BUSINESS_COLUMNS_ORDER]
    df.to_excel(excel_out, index=False, engine="openpyxl")
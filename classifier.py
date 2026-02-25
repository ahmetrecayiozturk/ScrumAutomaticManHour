from typing import Dict, Any

def classify_task(row: Dict[str, Any]) -> Dict[str, Any]:
    entity_name = (row.get("entity_name") or "").strip()
    related_entity_count = int(row.get("related_entity_count") or 0)
    relation_count = int(row.get("relation_count") or 0)
    custom_endpoint_count = int(row.get("custom_endpoint_count") or 0)

    is_entity = bool(entity_name) or (related_entity_count > 0) or (relation_count > 0) or (custom_endpoint_count > 0)

    row = dict(row)
    row["task_type"] = "entity_based" if is_entity else "non_entity_based"
    return row
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional, Tuple
import numpy as np

@dataclass
class EstimationConfig:
    be_crud_base_hours: float = 6.0
    fe_crud_base_hours: float = 8.0
    relation_multiplier: float = 0.5
    custom_endpoint_hours: float = 2.5
    adj_be: float = 1.0
    adj_fe: float = 1.0

def _complexity(row: Dict[str, Any]) -> float:
    cf = row.get("complexity_factor", None)
    if cf is None or cf == "":
        return 1.0
    try:
        return float(np.clip(float(cf), 0.7, 2.5))
    except Exception:
        return 1.0

def estimate_entity_based(row: Dict[str, Any], cfg: EstimationConfig) -> Tuple[float, float]:
    relation_count = int(row.get("relation_count") or 0)
    custom_endpoint_count = int(row.get("custom_endpoint_count") or 0)
    screen_count = int(row.get("screen_count") or 0)

    be = cfg.be_crud_base_hours
    be += relation_count * cfg.relation_multiplier * cfg.be_crud_base_hours
    be += custom_endpoint_count * cfg.custom_endpoint_hours

    fe = screen_count * cfg.fe_crud_base_hours

    if row.get("api_integration_hours") is not None:
        be += float(row["api_integration_hours"])
    if row.get("crud_screen_hours") is not None:
        fe += float(row["crud_screen_hours"])
    if row.get("ui_test_hours") is not None:
        fe += float(row["ui_test_hours"])

    return be, fe

def estimate_non_entity_based(row: Dict[str, Any], cfg: EstimationConfig) -> Tuple[float, float]:
    screen_count = int(row.get("screen_count") or 0)
    custom_endpoint_count = int(row.get("custom_endpoint_count") or 0)

    size = screen_count + custom_endpoint_count
    base = 2.0 if size <= 1 else (6.0 if size <= 3 else 12.0)

    fe = base * (0.55 if screen_count > 0 else 0.35)
    be = base - fe

    if row.get("api_integration_hours") is not None:
        be += float(row["api_integration_hours"])
    if row.get("crud_screen_hours") is not None:
        fe += float(row["crud_screen_hours"])
    if row.get("ui_test_hours") is not None:
        fe += float(row["ui_test_hours"])

    return be, fe

def estimate_row(row: Dict[str, Any], cfg: Optional[EstimationConfig] = None) -> Dict[str, Any]:
    if cfg is None:
        cfg = EstimationConfig()

    task_type = row.get("task_type") or "entity_based"
    if task_type == "non_entity_based":
        be, fe = estimate_non_entity_based(row, cfg)
    else:
        be, fe = estimate_entity_based(row, cfg)

    c = _complexity(row)

    be = be * c * float(getattr(cfg, "adj_be", 1.0))
    fe = fe * c * float(getattr(cfg, "adj_fe", 1.0))

    out = dict(row)
    out["backend_estimate"] = float(round(be, 2))
    out["frontend_estimate"] = float(round(fe, 2))
    out["total_estimate"] = float(round(be + fe, 2))
    return out

def config_from_dict(d: Dict[str, Any]) -> EstimationConfig:
    cfg = EstimationConfig()
    for k, v in (d or {}).items():
        if hasattr(cfg, k):
            setattr(cfg, k, float(v))
    return cfg

def config_to_dict(cfg: EstimationConfig) -> Dict[str, Any]:
    return asdict(cfg)  
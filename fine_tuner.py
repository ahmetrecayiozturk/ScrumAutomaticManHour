import os
import json
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from sklearn.linear_model import LinearRegression

MIN_ROWS = 2

FEATURES = [
    "task_type_entity", "relation_count", "custom_endpoint_count", "screen_count", "complexity_factor"
]

def _row_to_features(r: Dict[str, Any]) -> Dict[str, float]:
    task_type = r.get("task_type", "entity_based")
    return {
        "task_type_entity": 1.0 if task_type == "entity_based" else 0.0,
        "relation_count": float(r.get("relation_count") or 0),
        "custom_endpoint_count": float(r.get("custom_endpoint_count") or 0),
        "screen_count": float(r.get("screen_count") or 0),
        "complexity_factor": float(r.get("complexity_factor") or 1.0),
    }

def append_sprint_history_by_taskkey(
    history_csv: str,
    estimated_rows: List[Dict[str, Any]],
    actual_rows: List[Dict[str, Any]],
    *,
    actual_taskkey_field: str = "TaskKey",
    actual_be_field: str = "Actual_BE",
    actual_fe_field: str = "Actual_FE",
) -> pd.DataFrame:
    est_df = pd.DataFrame([{
        "task_key": (r.get("task_key") or "").strip(),
        **_row_to_features(r),
        "est_backend": float(r.get("backend_estimate") or 0.0),
        "est_frontend": float(r.get("frontend_estimate") or 0.0),
    } for r in estimated_rows])

    act_df = pd.DataFrame([{
        "task_key": (r.get(actual_taskkey_field) or r.get("TaskKey") or r.get("task_key") or "").strip(),
        "act_backend": float(r.get(actual_be_field) or 0.0),
        "act_frontend": float(r.get(actual_fe_field) or 0.0),
    } for r in actual_rows])

    est_df = est_df.replace("", np.nan).dropna(subset=["task_key"])
    act_df = act_df.replace("", np.nan).dropna(subset=["task_key"])

    merged = est_df.merge(act_df, on="task_key", how="inner")

    if os.path.exists(history_csv):
        df_old = pd.read_csv(history_csv)
        df_old["task_key"] = df_old["task_key"].astype(str).str.strip()
        new_keys = set(merged["task_key"].astype(str))
        df_old = df_old[~df_old["task_key"].isin(new_keys)]
        df_all = pd.concat([df_old, merged], ignore_index=True)
    else:
        df_all = merged

    df_all.to_csv(history_csv, index=False)
    return df_all

def train_adjustments(history_csv: str) -> Dict[str, float]:
    df = pd.read_csv(history_csv)
    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    df = df[(df["est_backend"] > 0.01) & (df["est_frontend"] > 0.01)]

    if len(df) < MIN_ROWS:
        return {"adj_be": 1.0, "adj_fe": 1.0}

    reg_be = LinearRegression(fit_intercept=False)
    reg_be.fit(df[["est_backend"]], df["act_backend"])
    adj_be = float(np.clip(reg_be.coef_[0], 0.7, 1.8))

    reg_fe = LinearRegression(fit_intercept=False)
    reg_fe.fit(df[["est_frontend"]], df["act_frontend"])
    adj_fe = float(np.clip(reg_fe.coef_[0], 0.7, 1.8))

    return {"adj_be": adj_be, "adj_fe": adj_fe}

def save_config_updates(config_json_path: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    cfg = {}
    if os.path.exists(config_json_path):
        with open(config_json_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)

    cfg.update({k: v for k, v in updates.items() if k in ["adj_be", "adj_fe"]})
    with open(config_json_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    return cfg
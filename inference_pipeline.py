import os
import json
from typing import Dict, Any, Optional

from excel_parser import read_excel_to_normalized_json
from classifier import classify_task
from estimator import estimate_row, config_from_dict, EstimationConfig
from capacity_checker import TeamConfig, check_capacity
import exporter

def load_estimation_config(config_json_path: str) -> EstimationConfig:
    if os.path.exists(config_json_path):
        with open(config_json_path, "r", encoding="utf-8") as f:
            d = json.load(f)
        return config_from_dict(d)
    return EstimationConfig()

def run_pipeline(
    *,
    excel_path: str,
    sheet_name: Optional[str] = None,
    config_json_path: str = "estimation_config.json",
    export_excel_path: str = "estimated_output.xlsx",
    export_json_path: str = "estimated_output.json",
    team: Optional[TeamConfig] = None,
) -> Dict[str, Any]:
    if team is None:
        team = TeamConfig()

    cfg = load_estimation_config(config_json_path)
    rows, _, colmap = read_excel_to_normalized_json(excel_path, sheet_name=sheet_name)

    estimated = []
    for r in rows:
        if not r.get("task_key"):
            raise ValueError("TaskKey boş olamaz. Her satırda TaskKey olmalı.")
        estimated.append(estimate_row(classify_task(r), cfg))

    sum_be = sum(x["backend_estimate"] for x in estimated)
    sum_fe = sum(x["frontend_estimate"] for x in estimated)
    cap = check_capacity(sum_be, sum_fe, team)

    exporter.export_excel_and_json(estimated, export_excel_path, export_json_path)

    return {
        "colmap": colmap,
        "totals": {"BE": sum_be, "FE": sum_fe, "TOTAL": sum_be + sum_fe},
        "capacity": cap
    }
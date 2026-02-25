from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class TeamConfig:
    backend_developers: int = 3
    frontend_developers: int = 1
    velocity_multiplier: float = 1.15
    hours_per_day: float = 6
    sprint_days: int = 14

def check_capacity(sum_backend: float, sum_frontend: float, team: TeamConfig) -> Dict[str, Any]:
    be_cap = team.backend_developers * team.hours_per_day * team.sprint_days * team.velocity_multiplier
    fe_cap = team.frontend_developers * team.hours_per_day * team.sprint_days * team.velocity_multiplier
    return {
        "backend_estimated": sum_backend,
        "frontend_estimated": sum_frontend,
        "backend_capacity": be_cap,
        "frontend_capacity": fe_cap,
        "total_estimated": sum_backend + sum_frontend,
        "total_capacity": be_cap + fe_cap,
    }
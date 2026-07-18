from __future__ import annotations

import yaml
from pathlib import Path
from typing import Any, Dict, List


class FailureModeEngine:
    def __init__(self, catalog_path: Path = None) -> None:
        path = catalog_path or Path(__file__).with_name("failure_modes.yaml")
        if not path.exists():
            self.modes: List[Dict[str, Any]] = []
            return
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        self.modes = data.get("failure_modes", [])

    def detect(self, metrics_snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
        triggered: List[Dict[str, Any]] = []
        loop_iterations = int(metrics_snapshot.get("loop_iterations") or 0)
        assumption_debt = int(metrics_snapshot.get("assumption_debt") or 0)
        fts = float(metrics_snapshot.get("fts") or 0.0)
        for mode in self.modes:
            mode_id = mode.get("id", "")
            if mode_id == "endless-inversion-loop" and loop_iterations > 5:
                triggered.append(mode)
            elif mode_id == "assumption-debt-overload" and assumption_debt >= 5:
                triggered.append(mode)
            elif mode_id == "confident-hallucination-with-falsification" and fts > 0.7:
                triggered.append(mode)
            elif mode_id == "shared-cognitive-state-corruption" and metrics_snapshot.get("state_corruption"):
                triggered.append(mode)
        return triggered

    def get_recovery(self, failure_id: str) -> str:
        for mode in self.modes:
            if mode.get("id") == failure_id:
                return mode.get("recovery", "No recovery documented.")
        return "No recovery documented."

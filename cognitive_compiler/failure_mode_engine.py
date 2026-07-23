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

    def _check_endless_loop(self, metrics_snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
        triggered: List[Dict[str, Any]] = []
        loop_iterations = int(metrics_snapshot.get("loop_iterations") or 0)
        if loop_iterations > 5:
            for mode in self.modes:
                if mode.get("id") == "endless-inversion-loop":
                    triggered.append(mode)
        return triggered

    def _check_assumption_debt_overload(self, metrics_snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
        triggered: List[Dict[str, Any]] = []
        assumption_debt = int(metrics_snapshot.get("assumption_debt") or 0)
        if assumption_debt >= 5:
            for mode in self.modes:
                if mode.get("id") == "assumption-debt-overload":
                    triggered.append(mode)
        return triggered

    def _check_confident_hallucination(self, metrics_snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
        triggered: List[Dict[str, Any]] = []
        fts = float(metrics_snapshot.get("fts") or 0.0)
        if fts > 0.7:
            for mode in self.modes:
                if mode.get("id") == "confident-hallucination-with-falsification":
                    triggered.append(mode)
        return triggered

    def _check_scs_corruption(self, metrics_snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
        triggered: List[Dict[str, Any]] = []
        if metrics_snapshot.get("state_corruption"):
            for mode in self.modes:
                if mode.get("id") == "shared-cognitive-state-corruption":
                    triggered.append(mode)
        return triggered

    def detect(self, metrics_snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
        triggered: List[Dict[str, Any]] = []
        triggered.extend(self._check_endless_loop(metrics_snapshot))
        triggered.extend(self._check_assumption_debt_overload(metrics_snapshot))
        triggered.extend(self._check_confident_hallucination(metrics_snapshot))
        triggered.extend(self._check_scs_corruption(metrics_snapshot))
        return triggered

    def get_recovery(self, failure_id: str) -> str:
        for mode in self.modes:
            if mode.get("id") == failure_id:
                return mode.get("recovery", "No recovery documented.")
        return "No recovery documented."

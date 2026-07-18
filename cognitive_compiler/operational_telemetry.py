from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import List


@dataclass
class HarnessMetrics:
    harness_name: str
    duration_ms: float
    assumption_debt: int
    falsification_theatricality_score: float
    epistemic_diversity_index: str  # Low | Medium | High
    human_escalation_triggered: bool
    predictions_generated: int
    predictions_tested: int
    errors_corrected: int
    guardrail_violations: List[str] = field(default_factory=list)


class OperationalTelemetry:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.metrics_history: List[HarnessMetrics] = []
        self.alerts: List[str] = []
        self.alert_thresholds = {
            "assumption_debt_high": 5,
            "fts_high": 0.7,
            "edi_low": "Low",
            "response_time_ms_max": 30000,
        }

    def record(self, metrics: HarnessMetrics):
        self.metrics_history.append(metrics)
        self._check_alerts(metrics)

    def _check_alerts(self, metrics: HarnessMetrics):
        alerts = []
        if metrics.assumption_debt > self.alert_thresholds["assumption_debt_high"]:
            alerts.append(f"High assumption debt: {metrics.assumption_debt}")
        if metrics.falsification_theatricality_score > self.alert_thresholds["fts_high"]:
            alerts.append(f"High FTS: {metrics.falsification_theatricality_score:.2f}")
        if metrics.epistemic_diversity_index == self.alert_thresholds["edi_low"]:
            alerts.append("Low epistemic diversity detected")
        if metrics.duration_ms > self.alert_thresholds["response_time_ms_max"]:
            alerts.append(f"Slow response: {metrics.duration_ms}ms")
        self.alerts.extend(alerts)

    def get_dashboard_snapshot(self) -> dict:
        if not self.metrics_history:
            return {}
        return {
            "latest_harness": self.metrics_history[-1].harness_name,
            "avg_assumption_debt": sum(m.assumption_debt for m in self.metrics_history) / len(self.metrics_history),
            "avg_fts": sum(m.falsification_theatricality_score for m in self.metrics_history) / len(self.metrics_history),
            "total_errors_corrected": sum(m.errors_corrected for m in self.metrics_history),
            "active_alerts": self.alerts[-10:],
        }


telemetry = OperationalTelemetry()

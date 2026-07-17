from __future__ import annotations

import dataclasses
import time
from datetime import datetime, timezone
from typing import Any


@dataclasses.dataclass(frozen=True)
class EvaluationMetrics:
    task_id: str
    trace_id: str | None = None
    timestamp: str = dataclasses.field(default_factory=lambda: datetime.now(timezone.utc).isoformat() + "Z")
    reasoning: dict[str, Any] = dataclasses.field(default_factory=dict)
    coding: dict[str, Any] = dataclasses.field(default_factory=dict)
    autonomy: dict[str, Any] = dataclasses.field(default_factory=dict)
    efficiency: dict[str, Any] = dataclasses.field(default_factory=dict)
    overall_score: float | None = None

    def with_reasoning(self, success_rate: float, planning_accuracy: float, contradictions: int) -> "EvaluationMetrics":
        return dataclasses.replace(self, reasoning={
            "success_rate": success_rate,
            "planning_accuracy": planning_accuracy,
            "contradictions_detected": contradictions,
        })

    def with_coding(self, tests_passed: int, tests_total: int, regressions: int, security_warnings: int) -> "EvaluationMetrics":
        return dataclasses.replace(self, coding={
            "tests_passed": tests_passed,
            "tests_total": tests_total,
            "regression_count": regressions,
            "security_warnings": security_warnings,
        })

    def with_autonomy(self, human_interventions: int, recovery_actions: int, failed_loops: int) -> "EvaluationMetrics":
        return dataclasses.replace(self, autonomy={
            "human_interventions": human_interventions,
            "recovery_actions": recovery_actions,
            "failed_loops": failed_loops,
        })

    def with_efficiency(self, tokens_used: int, latency_ms: float, compute_ms: float) -> "EvaluationMetrics":
        return dataclasses.replace(self, efficiency={
            "tokens_used": tokens_used,
            "latency_ms": latency_ms,
            "compute_ms": compute_ms,
        })

    def scored(self, overall: float) -> "EvaluationMetrics":
        return dataclasses.replace(self, overall_score=overall)

    def to_dict(self) -> dict[str, object]:
        return dataclasses.asdict(self)

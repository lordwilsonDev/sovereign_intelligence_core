from __future__ import annotations

import os

import pytest

from msb_v2.core.evaluation_metrics import EvaluationMetrics


def test_with_methods_are_immutable() -> None:
    m = EvaluationMetrics(task_id="task-1")
    next_m = m.with_reasoning(0.9, 0.9, 0)
    assert next_m.reasoning["success_rate"] == 0.9
    assert m.reasoning == {}


def test_scored_and_to_dict() -> None:
    m = EvaluationMetrics(task_id="task-1").scored(0.8)
    data = m.to_dict()
    assert data["overall_score"] == 0.8
    assert data["task_id"] == "task-1"

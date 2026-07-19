from __future__ import annotations

import pytest

from validation.workflow_tests import run_workflow_tests
from runtime.state_machine import RuntimeStateMachine, CREATED, INITIALIZING, READY, THINKING, EXECUTING, VERIFYING, COMPLETED, FAILED
from validation.health_report import HealthReport


def test_workflow_tests_returns_result_shape():
    data = run_workflow_tests("http://127.0.0.1:8766")
    assert "passed" in data
    assert "failed" in data
    assert "score" in data


def test_state_machine_transitions_allowed():
    sm = RuntimeStateMachine()
    task = sm.create_task("task-1", agent="tester")
    assert task.state == READY
    task.transition(THINKING)
    task.transition(EXECUTING)
    task.transition(VERIFYING)
    task.transition(COMPLETED, outcome="ok")
    assert task.state == COMPLETED
    assert len(task.transitions) == 6


def test_state_machine_transitions_invalid():
    sm = RuntimeStateMachine()
    task = sm.create_task("task-2")
    with pytest.raises(ValueError):
        task.transition(COMPLETED)


def test_health_report_build():
    report = HealthReport.build({
        "passed": ["GET /health", "GET /memory/health"],
        "failed": [],
        "score": 100.0,
    })
    assert report["grade"] == "A"
    assert report["msb_integrity_score"] == 100.0
    assert "health" in report["sections"]

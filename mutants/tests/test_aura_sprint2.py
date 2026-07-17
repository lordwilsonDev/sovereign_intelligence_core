from __future__ import annotations

import asyncio

from msb_v2.aura.models import Task, TaskStatus
from msb_v2.aura.orchestrator import run_scheduler, validate_output
from msb_v2.aura.persistence import Persistence
from msb_v2.aura.scheduler import Scheduler


def test_validator_layers_schema_and_rules_and_deterministic():
    task = Task(goal="validate this output")
    ok = {"status": "ok", "message": "hello", "confidence": 0.9}
    result = asyncio.run(validate_output(task, ok))
    assert result["ok"] is True
    assert result["layer"] == "deterministic"


def test_validator_blocks_forbidden_pattern():
    task = Task(goal="validate")
    bad = {"status": "ok", "message": "please run rm -rf now", "confidence": 0.5}
    result = asyncio.run(validate_output(task, bad))
    assert result["ok"] is False
    assert result["layer"] in {"rules", "deterministic"}


def test_scheduler_dlq_and_retry():
    persistence = Persistence(":memory:")
    scheduler = Scheduler(persistence=persistence, worker_count=2, fail_substring="fail-now", max_retries=1)
    scheduler.enqueue(Task(goal="ok 1"))
    scheduler.enqueue(Task(goal="fail-now 1"))
    scheduler.enqueue(Task(goal="ok 2"))
    results = asyncio.run(scheduler.drain())
    statuses = [t.status for t in results]
    assert statuses.count(TaskStatus.COMPLETED) == 2
    assert statuses.count(TaskStatus.DLQ) == 1
    assert len(scheduler.dlq) == 1


def test_run_scheduler_processed_count():
    persistence = Persistence(":memory:")
    result = asyncio.run(run_scheduler(persistence, task_count=20, failure_rate=0.1))
    assert result["enqueued"] == 20
    assert result["processed"] >= result["enqueued"]


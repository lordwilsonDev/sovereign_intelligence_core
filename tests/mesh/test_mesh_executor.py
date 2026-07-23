"""Tests for cross-node task execution."""
from __future__ import annotations

from typing import Any, Dict

import pytest

from msb_v2.mesh.executor import MeshTaskExecutor


class FakeIdentity:
    def __init__(self, node_id: str = "node-x") -> None:
        self.node_id = node_id


def test_executor_runs_queued_task() -> None:
    store: Dict[str, Dict[str, Any]] = {
        "t1": {"intent": "What is 2+2?", "status": "queued"}
    }
    executor = MeshTaskExecutor(FakeIdentity("node-1"), store)
    result = executor.execute("t1")
    assert result["status"] == "completed"
    assert "result" in result
    assert result["result"]["executed_by"] == "node-1"
    assert "signature" in result["result"]


def test_executor_rejects_already_completed_task() -> None:
    store = {"t2": {"intent": "test", "status": "completed"}}
    executor = MeshTaskExecutor(FakeIdentity(), store)
    result = executor.execute("t2")
    assert "error" in result


def test_executor_runs_fallback_when_kernel_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    store: Dict[str, Dict[str, Any]] = {"t3": {"intent": "test", "status": "queued"}}
    monkeypatch.setattr("msb_v2.kernel.kb4.KB4Kernel", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))
    executor = MeshTaskExecutor(FakeIdentity("node-3"), store)
    result = executor.execute("t3")
    assert result["status"] == "completed"
    assert "result" in result

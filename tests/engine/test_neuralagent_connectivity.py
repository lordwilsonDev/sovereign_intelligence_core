"""Neuralagent backend connectivity tests."""

from __future__ import annotations

import urllib.error
import urllib.request
from typing import Any

import pytest

from msb_v2.engine import neuralagent as neuralagent_module
from msb_v2.engine.neuralagent import execute_neuralagent


OLLAMA_ENDPOINT = "http://localhost:11434/api/tags"
NEURALAGENT_ENDPOINT = "http://localhost:8000/"


def _fetch(endpoint: str) -> dict[str, Any]:
    with urllib.request.urlopen(endpoint, timeout=5) as response:
        return pytest.importorskip("json").loads(response.read().decode("utf-8"))


def test_ollama_runtime_reachable() -> None:
    try:
        payload = _fetch(OLLAMA_ENDPOINT)
    except Exception as exc:
        pytest.fail(f"ollama_runtime_unreachable endpoint={OLLAMA_ENDPOINT} error={exc}")
    models = payload.get("models") or []
    names = [model.get("name", "") for model in models if isinstance(model, dict)]
    assert "qwen2.5:0.5b" in names, f"missing_expected_model models={names}"


def test_execute_neuralagent_dispatches_backend() -> None:
    captured: dict[str, Any] = {}

    def fake_backend(_payload: dict[str, Any]) -> dict[str, Any]:
        captured["called"] = True
        return {"ok": True, "backend": "stub"}

    neuralagent_module._dispatch_local_llm = fake_backend  # type: ignore[attr-defined]
    result = execute_neuralagent({"prompt": "ping", "provider": "ollama"})
    assert captured.get("called") is True
    assert result.get("ok") is True


def test_orchestrator_dispatches_default_backend_when_provider_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    from msb_v2.engine.orchestrator import Task, orchestrate

    captured: dict[str, Any] = {}

    def fake_backend(task: Task, hook) -> dict[str, Any]:  # type: ignore[no-untyped-def]
        captured["task_id"] = task.id
        return {"backend": "neuralagent", "task_id": task.id}

    monkeypatch.setattr("msb_v2.engine.orchestrator._dispatch_neuralagent", fake_backend)
    tasks = [Task(id="t1")]
    results = orchestrate(tasks)
    assert captured["task_id"] == "t1"
    assert results[0].status == "succeeded"
    assert str(results[0].result.get("backend")) == "neuralagent"

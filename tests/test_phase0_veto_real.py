from __future__ import annotations


import pytest
from fastapi.testclient import TestClient

from msb_v2.api.web import create_app
from msb_v2.core.budget_manager import CognitiveBudgetManager


@pytest.fixture()
def client_scorer(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("MSB_REASONING_SCORER", "1")
    return TestClient(create_app())


@pytest.fixture()
def client_no_scorer(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("MSB_REASONING_SCORER", "0")
    return TestClient(create_app())


def test_demo_query_returns_budget_when_scorer_enabled(client_scorer: TestClient) -> None:
    r = client_scorer.post(
        "/demo/query",
        json={"query": "veto check", "trace_id": "veto-1", "accepted": True},
    )
    assert r.status_code == 200
    body = r.json()
    assert "budget" in body
    budget = body["budget"]
    assert "breached" in budget
    assert "breach_reason" in budget
    assert "depth" in budget
    assert "tool_calls" in budget


def test_demo_query_short_circuit_without_scorer(client_no_scorer: TestClient) -> None:
    r = client_no_scorer.post(
        "/demo/query",
        json={"query": "veto check", "trace_id": "veto-2", "accepted": True},
    )
    assert r.status_code == 200
    body = r.json()
    assert body.get("confidence_assessment") is None
    assert "budget" not in body


def test_budget_manager_blocks_after_depth_breach() -> None:
    mgr = CognitiveBudgetManager(max_depth=5, max_tool_calls=10, max_global_depth=20, max_global_tool_calls=20)
    trace_id = "veto-unit"
    with mgr.track(trace_id):
        for _ in range(6):
            mgr.increment_depth(trace_id)
    assert mgr.can_execute(trace_id) is False


def test_budget_manager_blocks_when_circuit_open() -> None:
    mgr = CognitiveBudgetManager(max_depth=5, max_tool_calls=10, max_global_depth=20, max_global_tool_calls=20)
    breaker = mgr._circuit
    breaker.window_seconds = 60
    breaker.breach_rate_threshold = 0.0
    breaker.min_requests = 1
    breaker.record_request(True)
    assert breaker.open is True
    assert mgr.can_execute("veto-circuit") is False


def test_demo_query_429_after_depth_limit(client_scorer: TestClient) -> None:
    trace_id = "veto-429"
    for i in range(6):
        r = client_scorer.post(
            "/demo/query",
            json={"query": "x", "trace_id": trace_id, "accepted": True},
        )
        expected_status = 200 if i < 5 else 429
        assert r.status_code == expected_status, f"request {i+1} expected {expected_status} got {r.status_code}"
        if expected_status == 429:
            body = r.json()
            assert body["detail"] == "Budget exceeded – request rejected"
            assert body["trace_id"] == trace_id
            assert body["reason"] == "budget_exhausted"

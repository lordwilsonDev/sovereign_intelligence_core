from __future__ import annotations

import pytest

from msb_v2.api.main import create_app
from starlette.testclient import TestClient


@pytest.fixture()
def client():  # noqa: ANN001
    return TestClient(create_app())


def test_brain_requires_query(client):  # noqa: ANN001
    response = client.post("/brain/run", json={"intent": "default"})
    assert response.status_code == 422


def test_brain_empty_body(client):  # noqa: ANN001
    response = client.post("/brain/run", json={})
    assert response.status_code == 422


def test_brain_unknown_intent_falls_back(client):  # noqa: ANN001
    response = client.post("/brain/run", json={"query": "anything", "intent": "does_not_exist"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["kind"] == "fallback"
    assert payload["payload"]["resolved"] == "noop"


def test_brain_fallback_noop(client):  # noqa: ANN001
    response = client.post("/brain/run", json={"query": "ping", "intent": "default"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["kind"] == "fallback"
    assert payload["payload"]["resolved"] == "noop"
    assert payload["payload"]["query"] == "ping"
    assert payload["task_id"] != ""
    assert "metrics" in payload


def test_brain_drill(client):  # noqa: ANN001
    response = client.post("/brain/run", json={"query": "say hello", "intent": "drill"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["kind"] == "aura"
    assert payload["payload"]["module"] == "aura"
    assert payload["payload"]["decision"]["tool"] == "echo"


def test_brain_imagine(client):  # noqa: ANN001
    response = client.post("/brain/run", json={"query": "hello world", "intent": "imagine"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["kind"] == "imagination"
    assert "root_hash" in payload["payload"]
    assert payload["payload"]["seed"] == "hello"


def test_brain_branch_missing_trace(client):  # noqa: ANN001
    response = client.post("/brain/run", json={"query": "ping", "intent": "branch"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["kind"] == "counterfactual_error"
    assert "error" in payload["payload"]


def test_brain_debate_returns_moie(client):  # noqa: ANN001
    response = client.post("/brain/run", json={"query": "who should rule?", "intent": "debate"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["kind"] == "moie"
    assert "claims_total" in payload["payload"]


def test_brain_plan_returns_rcoh(client):  # noqa: ANN001
    response = client.post("/brain/run", json={"query": "build a ship", "intent": "plan"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["kind"] == "rcoh"
    assert "cycle_id" in payload["payload"]
    assert "alternatives_count" in payload["payload"]


def test_brain_assess_returns_cognitive(client):  # noqa: ANN001
    response = client.post("/brain/run", json={"query": "is this safe?", "intent": "assess"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["kind"] in {"cognitive", "cognitive_error"}


def test_brain_task_id_unique():  # noqa: ANN001
    client = TestClient(create_app())
    first = client.post("/brain/run", json={"query": "ping", "intent": "default"}).json()
    second = client.post("/brain/run", json={"query": "ping", "intent": "default"}).json()
    assert first["task_id"] != second["task_id"]
    assert first["trace_id"] == second["trace_id"]


def test_brain_response_schema(client):  # noqa: ANN001
    response = client.post("/brain/run", json={"query": "ping", "intent": "default"})
    assert response.status_code == 200
    payload = response.json()
    assert set(payload.keys()) == {"status", "kind", "task_id", "trace_id", "metrics", "payload"}
    assert isinstance(payload["task_id"], str)
    assert payload["task_id"]
    assert payload["status"] == "ok"
    metrics = payload["metrics"]
    assert "task_id" in metrics
    assert "timestamp" in metrics
    assert "overall_score" in metrics
    for section in ["reasoning", "coding", "autonomy", "efficiency"]:
        assert section in metrics

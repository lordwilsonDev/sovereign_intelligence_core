from __future__ import annotations

import pytest

from msb_v2.api.main import create_app
from starlette.testclient import TestClient


@pytest.fixture()
def client():  # noqa: ANN001
    return TestClient(create_app())


def test_brain_fallback_noop(client):  # noqa: ANN001
    response = client.post("/brain/run", json={"query": "ping", "intent": "default"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["kind"] == "fallback"
    assert payload["payload"]["resolved"] == "noop"
    assert payload["payload"]["query"] == "ping"


def test_brain_drill(client):  # noqa: ANN001
    response = client.post("/brain/run", json={"query": "say hello", "intent": "drill"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["kind"] == "aura"
    assert payload["payload"]["module"] == "aura"
    assert payload["payload"]["decision"]["tool"] == "echo"


def test_brain_imagine(client):  # noqa: ANN001
    response = client.post("/brain/run", json={"query": "hello world", "intent": "imagine"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["kind"] == "imagination"
    assert "root_hash" in payload["payload"]
    assert payload["payload"]["seed"] == "hello"


def test_brain_branch_missing_trace(client):  # noqa: ANN001
    response = client.post("/brain/run", json={"query": "ping", "intent": "branch"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["kind"] == "counterfactual_error"
    assert "error" in payload["payload"]


def test_brain_debate_returns_moie(client):  # noqa: ANN001
    response = client.post("/brain/run", json={"query": "who should rule?", "intent": "debate"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["kind"] == "moie"
    assert "claims_total" in payload["payload"]


def test_brain_plan_returns_rcoh(client):  # noqa: ANN001
    response = client.post("/brain/run", json={"query": "build a ship", "intent": "plan"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["kind"] == "rcoh"
    assert "cycle_id" in payload["payload"]
    assert "alternatives_count" in payload["payload"]


def test_brain_assess_returns_cognitive(client):  # noqa: ANN001
    response = client.post("/brain/run", json={"query": "is this safe?", "intent": "assess"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["kind"] in {"cognitive", "cognitive_error"}

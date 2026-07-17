from __future__ import annotations

import pytest

from starlette.testclient import TestClient

from msb_v2.api.main import create_app


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

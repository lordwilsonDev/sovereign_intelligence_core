"""Integration tests for mesh task contracts."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


@pytest.fixture()
def client() -> TestClient:
    app = create_app()
    return TestClient(app)


def _auth_headers() -> dict:
    return {"Authorization": "Bearer tok"}


def test_submit_task_returns_task_id(client: TestClient) -> None:
    resp = client.post("/mesh/tasks/submit", json={
        "intent": "Analyze the current sovereignty metrics",
        "context": {},
        "requesting_node_id": "node-1",
        "requesting_node_signature": "sig-1",
    }, headers=_auth_headers())
    assert resp.status_code == 200
    data = resp.json()
    assert "task_id" in data
    assert data["status"] == "queued"


def test_get_task_after_submission(client: TestClient) -> None:
    resp = client.post("/mesh/tasks/submit", json={
        "intent": "Generate a morning briefing",
        "context": {},
        "requesting_node_id": "node-2",
        "requesting_node_signature": "sig-2",
    }, headers=_auth_headers())
    task_id = resp.json()["task_id"]
    resp2 = client.get(f"/mesh/tasks/{task_id}", headers=_auth_headers())
    assert resp2.status_code == 200
    assert resp2.json()["task_id"] == task_id
    assert resp2.json()["status"] == "queued"


def test_get_nonexistent_task_returns_404(client: TestClient) -> None:
    resp = client.get("/mesh/tasks/nonexistent", headers=_auth_headers())
    assert resp.status_code == 404


def test_execute_task_returns_completed(client: TestClient) -> None:
    resp = client.post("/mesh/tasks/submit", json={
        "intent": "Return 42",
        "context": {},
        "requesting_node_id": "node-x",
        "requesting_node_signature": "sig-x",
    }, headers=_auth_headers())
    task_id = resp.json()["task_id"]
    resp2 = client.get(f"/mesh/tasks/{task_id}", params={"execute": True}, headers=_auth_headers())
    assert resp2.status_code == 200
    body = resp2.json()
    assert body["task_id"] == task_id
    assert body["status"] == "completed"
    assert body["result"] is not None
    assert "executed_by" in body["result"]

from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import app

client = TestClient(app)


def test_aura_run_endpoint():
    payload = {"goal": "Say hello from AURA API"}
    resp = client.post("/aura/run", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "task_id" in data
    assert "session_id" in data


def test_aura_tasks_endpoint():
    payload = {"goals": ["goal one", "goal two"], "client_id": "default", "priority": 2}
    resp = client.post("/aura/tasks", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["count"] == 2
    assert len(data["task_ids"]) == 2


def test_aura_recent_tasks_endpoint():
    resp = client.get("/aura/tasks/recent", params={"limit": 10})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "recent_limit" in data

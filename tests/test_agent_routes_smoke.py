from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app

client = TestClient(create_app())


def test_v3_planner_plan_route() -> None:
    response = client.post("/v3/planner/plan", json={"task": "open Spotify", "context": {"mode": "fast"}})
    assert response.status_code == 200
    body = response.json()
    assert "task" in body or "plan" in body


def test_v3_tasks_submit_route() -> None:
    response = client.post("/v3/tasks/submit", params={"goal": "demo", "priority": "normal"})
    assert response.status_code == 200
    body = response.json()
    assert body.get("status") == "queued"
    assert "task_id" in body


def test_agent_run_route() -> None:
    response = client.post("/agent/run", json={"run_id": "r1", "tasks": [{"goal": "Say hello"}]})
    assert response.status_code == 200
    body = response.json()
    assert "run_id" in body or "status" in body


def test_agent_execute_route() -> None:
    response = client.post("/agent/execute", params={"goal": "Say hello"})
    assert response.status_code == 200
    body = response.json()
    assert body.get("goal") == "Say hello"

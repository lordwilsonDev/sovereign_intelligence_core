from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app

client = TestClient(create_app())


def test_v3_planner_plan_route() -> None:
    response = client.post("/v3/planner/plan", json={"task": "open Spotify", "context": {"mode": "fast"}})
    assert response.status_code == 200
    body = response.json()
    assert "task" in body or "plan" in body


def test_v3_tasks_submit_and_list() -> None:
    response = client.post("/v3/tasks/submit", params={"goal": "demo", "priority": "normal"})
    assert response.status_code == 200
    body = response.json()
    assert body.get("status") == "queued"
    task_id = body.get("task_id")
    assert task_id

    status_resp = client.get(f"/v3/tasks/{task_id}")
    assert status_resp.status_code == 200

    list_resp = client.get("/v3/tasks")
    assert list_resp.status_code == 200


def test_agent_plan_route() -> None:
    response = client.post("/agent/plan", params={"goal": "Say hello"})
    assert response.status_code == 200
    body = response.json()
    assert body.get("goal") == "Say hello"
    assert "steps" in body


def test_agent_queue_route() -> None:
    response = client.post("/agent/queue", params={"goal": "queue task", "priority": 1})
    assert response.status_code == 200
    body = response.json()
    assert "task_id" in body
    assert body.get("status") == "queued"


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

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
    response = client.post("/v3/tasks/submit", json={"task": "demo"})
    assert response.status_code in {200, 422}


def test_agent_run_route() -> None:
    response = client.post("/agent/run", json={"goal": "Say hello"})
    assert response.status_code in {200, 422}


def test_agent_execute_route() -> None:
    response = client.post("/agent/execute", json={"plan": []})
    assert response.status_code in {200, 422}

from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


client = TestClient(create_app())


def test_agent_plan_returns_step():
    response = client.post("/agent/plan", params={"goal": "search something"})
    assert response.status_code == 200
    body = response.json()
    assert body["goal"] == "search something"
    assert len(body["steps"]) == 1
    assert body["steps"][0]["tool"] == "noop_command"


def test_agent_plan_empty_goal_falls_back():
    response = client.post("/agent/plan", params={"goal": "   "})
    assert response.status_code == 200
    body = response.json()
    assert len(body["steps"]) >= 1
    assert body["steps"][0]["tool"] == "noop"


def test_agent_execute_completes_noop():
    response = client.post("/agent/execute", params={"goal": "do nothing"})
    assert response.status_code == 200
    body = response.json()
    assert body["result"] == "Completed 1 step(s) for: do nothing"


def test_agent_queue_submit_returns_task_id():
    response = client.post("/agent/queue", params={"goal": "async task", "priority": 1})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "queued"
    assert "task_id" in body


def test_agent_queue_status_not_found():
    response = client.get("/agent/queue/00000000")
    assert response.status_code == 404

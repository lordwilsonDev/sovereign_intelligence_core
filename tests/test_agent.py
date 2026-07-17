from __future__ import annotations

from typing import Any, Dict

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_agent_run_executes_callable() -> None:
    client = TestClient(create_app())
    response = client.post("/agent/run", json={
        "run_id": "run-1",
        "tasks": [
            {
                "task_id": "t1",
                "name": "echo",
                "callable": "msb_v2.agent.runtime:_agent_echo",
                "payload": {"payload": {"key": "value"}},
            }
        ],
    })
    assert response.status_code == 200
    body = response.json()
    assert body["run_id"] == "run-1"
    assert body["count"] == 1
    assert body["completed"] == 1
    assert body["failed"] == 0
    assert body["tasks"][0]["status"] == "completed"
    assert body["tasks"][0]["result"] == {"echo": {"key": "value"}}


def test_agent_run_fails_on_bad_callable() -> None:
    client = TestClient(create_app())
    response = client.post("/agent/run", json={
        "run_id": "run-2",
        "tasks": [
            {
                "task_id": "t2",
                "name": "noop",
                "callable": "not.a.real.callable",
                "payload": {},
            }
        ],
    })
    assert response.status_code == 200
    body = response.json()
    assert body["tasks"][0]["status"] == "failed"
    assert "ModuleNotFoundError" in body["tasks"][0]["error"]


def test_agent_run_status_returns_state() -> None:
    client = TestClient(create_app())
    client.post("/agent/run", json={
        "run_id": "run-3",
        "tasks": [
            {
                "task_id": "t3",
                "name": "echo",
                "callable": "msb_v2.agent.runtime:_agent_echo",
                "payload": {"payload": {"x": 1}},
            }
        ],
    })
    response = client.get("/agent/run/run-3")
    assert response.status_code == 200
    body = response.json()
    assert body["run_id"] == "run-3"
    assert body["count"] == 1

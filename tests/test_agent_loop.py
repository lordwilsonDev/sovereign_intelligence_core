from __future__ import annotations

import time

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_agent_run_loop_default_max_iterations_capped_at_24() -> None:
    client = TestClient(create_app())
    response = client.post("/agent/run/loop", json={
        "run_id": "loop-default",
    })
    assert response.status_code == 200
    body = response.json()
    assert body["run_id"] == "loop-default"
    assert body["mode"] == "loop"
    assert body["max_iterations"] == 1
    assert body["completed"] == 1
    assert body["failed"] == 0
    assert len(body["iterations"]) == 1
    assert body["iterations"][0]["status"] == "completed"


def test_agent_run_loop_custom_iterations_and_task_template() -> None:
    client = TestClient(create_app())
    start = time.monotonic()
    response = client.post("/agent/run/loop", json={
        "run_id": "loop-3",
        "max_iterations": 3,
        "interval_seconds": 0.0,
        "task_template": {
            "name": "custom-loop",
            "callable": "msb_v2.agent.runtime:_agent_echo",
            "payload": {"source": "loop-test"},
        },
    })
    elapsed = time.monotonic() - start
    assert response.status_code == 200
    body = response.json()
    assert body["max_iterations"] == 3
    assert body["completed"] == 3
    assert body["failed"] == 0
    assert len(body["iterations"]) == 3
    for iteration in body["iterations"]:
        assert iteration["status"] == "completed"
    assert elapsed < 2.0


def test_agent_run_loop_stops_on_error() -> None:
    client = TestClient(create_app())
    response = client.post("/agent/run/loop", json={
        "run_id": "loop-err",
        "max_iterations": 5,
        "interval_seconds": 0.0,
        "task_template": {
            "name": "bad",
            "callable": "not.a.real.callable",
        },
        "stop_on_error": True,
    })
    assert response.status_code == 200
    body = response.json()
    assert body["completed"] == 0
    assert body["failed"] == 1
    assert body["stopped_reason"] is not None
    assert "stopped after 1 iteration(s)" in body["stopped_reason"]

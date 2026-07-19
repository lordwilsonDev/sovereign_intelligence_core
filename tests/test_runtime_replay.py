from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.runtime.replay import replay_store


def test_runtime_replay_runs_endpoint() -> None:
    client = TestClient(create_app())
    replay_store.record_run("rt-1", [{"task_id": "t1", "status": "completed"}])
    response = client.get("/runtime/replay/runs")
    assert response.status_code == 200
    body = response.json()
    assert body["runs"] == ["rt-1"]


def test_runtime_replay_run_endpoint() -> None:
    client = TestClient(create_app())
    replay_store.record_run("rt-2", [{"task_id": "t2", "status": "completed"}])
    response = client.get("/runtime/replay/run/rt-2")
    assert response.status_code == 200
    body = response.json()
    assert body["run_id"] == "rt-2"
    assert len(body["tasks"]) == 1
    assert body["tasks"][0]["task_id"] == "t2"

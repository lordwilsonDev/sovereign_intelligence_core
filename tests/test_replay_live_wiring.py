from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.runtime.replay import replay_store


@pytest.fixture(autouse=True)
def _isolate_replay_store() -> None:
    replay_store.reset()
    yield
    replay_store.reset()


def test_agent_run_is_visible_in_runtime_replay() -> None:
    client = TestClient(create_app())
    agent_body = {
        "run_id": "replay-live-1",
        "tasks": [
            {
                "task_id": "rt-1",
                "name": "echo",
                "callable": "msb_v2.agent.runtime:_agent_echo",
                "payload": {"payload": {"iteration": 1, "run_id": "replay-live-1"}},
            }
        ],
    }
    run_response = client.post("/agent/run", json=agent_body)
    assert run_response.status_code == 200

    runs_response = client.get("/runtime/replay/runs")
    assert runs_response.status_code == 200
    assert "replay-live-1" in runs_response.json()["runs"]

    run_response = client.get("/runtime/replay/run/replay-live-1")
    assert run_response.status_code == 200
    assert run_response.json()["run_id"] == "replay-live-1"
    assert len(run_response.json()["tasks"]) == 1
    assert run_response.json()["tasks"][0]["task_id"] == "rt-1"


def test_runtime_replay_run_missing_returns_empty() -> None:
    client = TestClient(create_app())
    response = client.get("/runtime/replay/run/__missing__")
    assert response.status_code == 200
    assert response.json()["tasks"] == []

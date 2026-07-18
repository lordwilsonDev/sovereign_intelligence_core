from __future__ import annotations

import time

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


client = TestClient(create_app())


def test_integration_plan_queue_crew_flow() -> None:
    goal = "open Spotify"
    plan_resp = client.post("/v3/planner/plan", json={"task": goal, "context": {"mode": "fast"}})
    assert plan_resp.status_code == 200
    plan = plan_resp.json()
    assert plan["task"] == goal

    task_resp = client.post("/v3/tasks/submit", params={"goal": plan["plan"], "priority": "high"})
    assert task_resp.status_code == 200
    task_id = task_resp.json()["task_id"]

    status_resp = client.get(f"/v3/tasks/{task_id}")
    assert status_resp.status_code == 200
    assert status_resp.json()["task_id"] == task_id

    crew_resp = client.post("/brain/run", json={"query": goal, "intent": "execute"})
    assert crew_resp.status_code == 200
    payload = crew_resp.json()
    assert payload["status"] == "ok"
    assert payload["kind"] == "executor"
    assert payload["payload"]["goal"] == goal

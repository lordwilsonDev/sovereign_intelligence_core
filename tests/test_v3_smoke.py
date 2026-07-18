from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


client = TestClient(create_app())


V3_GET_ROUTES = [
    "/v3/health",
    "/v3/capabilities",
    "/v3/summary",
    "/v3/memory/routes",
    "/v3/tools",
    "/v3/tools/schema",
    "/v3/memory/search?q=smoke",
]


def test_v3_get_routes_200() -> None:
    for route in V3_GET_ROUTES:
        response = client.get(route)
        assert response.status_code == 200, f"{route} failed: {response.status_code} {response.text}"


def test_v3_memory_search_smoke() -> None:
    response = client.get("/v3/memory/search", params={"q": "smoke"})
    assert response.status_code == 200
    body = response.json()
    assert body.get("query") == "smoke"


def test_v3_planner_plan_route() -> None:
    response = client.post("/v3/planner/plan", json={"task": "open Spotify", "context": {"mode": "fast"}})
    assert response.status_code == 200
    body = response.json()
    assert body.get("task") == "open Spotify"


def test_v3_tasks_submit_and_status_route() -> None:
    response = client.post("/v3/tasks/submit", params={"goal": "smoke", "priority": "normal"})
    assert response.status_code == 200
    body = response.json()
    assert body.get("status") == "queued"
    task_id = body.get("task_id")

    response = client.get(f"/v3/tasks/{task_id}")
    assert response.status_code == 200
    status = response.json()
    assert status.get("task_id") == task_id


def test_v3_twin_create_route() -> None:
    response = client.post("/v3/twin", json={"name": "smoke", "state": {}})
    assert response.status_code == 200
    body = response.json()
    assert "twin_id" in body


def test_v3_deliberate_route() -> None:
    response = client.post("/v3/deliberate", json={"query": "smoke", "max_rounds": 1})
    assert response.status_code == 200
    body = response.json()
    assert "rounds" in body

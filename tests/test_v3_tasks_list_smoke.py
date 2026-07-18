from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app

client = TestClient(create_app())


def test_v3_tasks_list_returns_payload() -> None:
    response = client.get("/v3/tasks")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert "tasks" in body


def test_v3_tasks_list_route_matches_response_shape() -> None:
    response = client.get("/v3/tasks/list")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert "error" in body or "tasks" in body

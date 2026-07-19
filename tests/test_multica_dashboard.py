from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


def test_observability_health_returns_200() -> None:
    client = TestClient(create_app())
    response = client.get("/observability/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"


def test_observability_squads_returns_payload() -> None:
    client = TestClient(create_app())
    response = client.get("/observability/squads")
    assert response.status_code == 200
    body = response.json()
    assert "squads" in body
    assert "hooks" in body

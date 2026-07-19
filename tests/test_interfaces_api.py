from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_interfaces_registry_returns_snapshot() -> None:
    client = TestClient(create_app())
    response = client.get("/interfaces/registry")
    assert response.status_code == 200
    body = response.json()
    assert "interfaces" in body
    assert "healthy_count" in body


def test_interfaces_refresh_endpoint() -> None:
    client = TestClient(create_app())
    response = client.post("/interfaces/refresh")
    assert response.status_code == 200
    body = response.json()
    assert "interfaces" in body
    assert "healthy_count" in body

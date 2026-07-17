from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_environment_status_returns_phase_active() -> None:
    client = TestClient(create_app())
    response = client.get("/environment/status")
    assert response.status_code == 200
    body = response.json()
    assert body["phase"] == "Phase 7"
    assert body["status"] == "active"
    assert "components" in body
    assert body["components"]["runtime"] == "active"


def test_sovereign_status_alias_returns_same_snapshot() -> None:
    client = TestClient(create_app())
    env_response = client.get("/environment/status")
    sovereign_response = client.get("/sovereign/status")
    assert sovereign_response.status_code == 200
    assert sovereign_response.json() == env_response.json()

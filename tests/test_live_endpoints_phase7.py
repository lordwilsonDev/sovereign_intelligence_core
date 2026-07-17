from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_live_endpoints_phase7_roundup() -> None:
    client = TestClient(create_app())
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    root = client.get("/")
    assert root.status_code == 200
    assert root.json()["name"] == "msb-studio"

    studio = client.get("/studio/status")
    assert studio.status_code == 200
    body = studio.json()
    assert body["runtime"]["ok"] is True
    assert body["memory"]["ok"] is True
    assert body["verification"]["ok"] is True
    assert body["evolution"]["ok"] is True
    assert "agent" in body
    assert "run_endpoint" in body["agent"]

    sovereign = client.get("/sovereign/status")
    assert sovereign.status_code == 200
    assert sovereign.json()["phase"] == "Phase 7"

    environment = client.get("/environment/status")
    assert environment.status_code == 200
    assert environment.json() == sovereign.json()

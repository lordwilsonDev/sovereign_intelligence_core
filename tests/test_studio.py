from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_studio_root_returns_json() -> None:
    client = TestClient(create_app())
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "msb-studio"
    assert "endpoints" in body


def test_studio_status_returns_composite_state() -> None:
    client = TestClient(create_app())
    response = client.get("/studio/status")
    assert response.status_code == 200
    body = response.json()
    assert "runtime" in body
    assert "memory" in body
    assert "verification" in body
    assert "evolution" in body
    assert "agent" in body
    assert body["runtime"]["ok"] is True
    assert body["memory"]["ok"] is True
    assert body["verification"]["ok"] is True
    assert body["evolution"]["ok"] is True

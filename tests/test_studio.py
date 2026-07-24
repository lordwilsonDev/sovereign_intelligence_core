from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_studio_root_returns_json() -> None:
    client = TestClient(create_app())
    response = client.get("/")
    assert response.status_code == 200
    assert "msb-studio" in response.json()["name"]


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


def test_studio_agent_dashboard_returns_neuralagent_assessment() -> None:
    client = TestClient(create_app())
    response = client.get("/agent-dashboard")
    assert response.status_code == 200
    body = response.json()
    assert body["model"] == "qwen2.5:0.5b"
    assert body["provider"] == "ollama"
    assert "result" in body
    assert body["result"]["ok"] is True


def test_studio_dashboard_page_renders_html() -> None:
    client = TestClient(create_app())
    response = client.get("/dashboard")
    assert response.status_code == 200
    body = response.text
    assert "<html" in body.lower()
    assert "msb-studio" in body
    assert "/studio/status" in body
    assert "/agent-dashboard" in body
    assert "/metrics" in body

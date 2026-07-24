from __future__ import annotations

from typing import Any, Dict

import urllib.error
import urllib.request
from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_studio_root_returns_json() -> None:
    client = TestClient(create_app())
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "msb-studio"
    assert "agent_dashboard" in body["endpoints"]


def test_studio_status_returns_composite_state() -> None:
    client = TestClient(create_app())
    response = client.get("/studio/status")
    assert response.status_code == 200
    body = response.json()
    for key in ["runtime", "memory", "verification", "evolution", "agent"]:
        assert key in body
    assert body["runtime"]["ok"] is True
    assert body["memory"]["ok"] is True
    assert body["verification"]["ok"] is True
    assert body["evolution"]["ok"] is True


def test_studio_agent_dashboard_uses_default_local_ollama_when_no_payload() -> None:
    client = TestClient(create_app())
    response = client.get("/agent-dashboard")
    assert response.status_code == 200
    body = response.json()
    assert body["provider"] == "ollama"
    assert body["model"] == "qwen2.5:0.5b"
    assert isinstance(body["result"], dict)
    assert body["result"].get("ok") is True


def test_studio_agent_dashboard_response_shape_is_stable() -> None:
    client = TestClient(create_app())
    response = client.get("/agent-dashboard")
    assert response.status_code == 200
    body = response.json()
    assert "prompt" in body
    assert "result" in body
    assert "model" in body
    assert "provider" in body
    text = str(body)
    assert "http://localhost:11434" not in text
    assert "api/generate" not in text
    assert "qwen2.5:0.5b" in text


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
    assert "loadAll" in body


def test_studio_dashboard_contains_fallback_status_cards() -> None:
    client = TestClient(create_app())
    response = client.get("/dashboard")
    assert response.status_code == 200
    body = response.text
    assert "studio" in body
    assert "agent" in body
    assert "observability" in body
    assert "metrics" in body


def test_studio_dashboard_does_not_expose_internal_backend_paths() -> None:
    client = TestClient(create_app())
    response = client.get("/dashboard")
    assert response.status_code == 200
    body = response.text
    assert "/debug" not in body.lower()
    assert "pydantic_core" not in body

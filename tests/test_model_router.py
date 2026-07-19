from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.api.model_router import model_router


def test_model_status_endpoint() -> None:
    client = TestClient(create_app())
    r = client.get("/model/status")
    assert r.status_code == 200
    body = r.json()
    assert "models" in body
    assert body["available_count"] >= 1


def test_model_route_prefers_registered_model_names() -> None:
    client = TestClient(create_app())
    r = client.post("/model/route", json={"task": "extract entities from legal document"})
    assert r.status_code == 200
    body = r.json()
    assert body["result"]["model"] in {"qwen2.5:7b-instruct", "qwen3:latest", "deepseek", "local", "claude"}
    assert body["result"]["provider"] in {"ollama", "local", "openai", "anthropic"}


def test_model_route_respects_prefer_local_context() -> None:
    client = TestClient(create_app())
    r = client.post("/model/route", json={"task": "summarize notes", "context": {"prefer_local": True}})
    assert r.status_code == 200
    body = r.json()
    assert body["result"]["model"] in {"local", "qwen2.5:7b-instruct", "qwen3:latest"}
    assert body["result"]["provider"] == "local"

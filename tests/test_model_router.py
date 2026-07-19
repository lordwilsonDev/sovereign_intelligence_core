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


def test_model_route_endpoint_prefers_capability_match() -> None:
    client = TestClient(create_app())
    r = client.post("/model/route", json={"task": "extract entities from legal document"})
    assert r.status_code == 200
    body = r.json()
    assert body["result"]["model"] in {"deepseek", "local", "claude"}

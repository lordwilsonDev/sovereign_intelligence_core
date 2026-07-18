from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


client = TestClient(create_app())


def test_deployment_health_endpoint():
    r = client.get("/v3/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_deployment_memory_search_contract():
    r = client.get("/v3/memory/search", params={"q": "AI", "limit": 5})
    assert r.status_code == 200
    body = r.json()
    assert "query" in body
    assert "entries" in body
    assert "count" in body


def test_deployment_brain_run_contract():
    r = client.post("/brain/run", json={"query": "smoke", "intent": "default"})
    assert r.status_code == 200
    payload = r.json()
    assert set(payload.keys()) == {"status", "kind", "task_id", "trace_id", "metrics", "payload"}

from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


client = TestClient(create_app())


def test_v3_capabilities():
    r = client.get("/v3/capabilities")
    assert r.status_code == 200
    body = r.json()
    assert "capabilities" in body
    ids = [c["capability_id"] for c in body["capabilities"]]
    assert "cap:brain:run" in ids


def test_v3_summary():
    r = client.get("/v3/summary")
    assert r.status_code == 200
    body = r.json()
    assert "capabilities" in body
    assert "memory" in body
    assert "constraints" in body


def test_v3_memory_routes():
    r = client.get("/v3/memory/routes")
    assert r.status_code == 200
    body = r.json()
    assert len(body["routes"]) == 8


def test_v3_validate_missing_returns_404():
    r = client.post("/v3/capabilities/cap:missing/validate")
    assert r.status_code == 404


def test_v3_validate_existing_returns_result():
    r = client.post("/v3/capabilities/cap:brain:run/validate")
    assert r.status_code == 200
    body = r.json()
    assert "constraint_result" in body

from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


def test_optimize_status_endpoint():
    client = TestClient(create_app())
    response = client.get("/optimize/status")
    assert response.status_code == 200
    body = response.json()
    assert "status" in body
    assert "last_run" in body


def test_optimize_analyze_endpoint():
    client = TestClient(create_app())
    response = client.post("/optimize/analyze", json={"cpu_percent": 0.95, "memory_percent": 0.1, "disk_percent": 0.1})
    assert response.status_code == 200
    body = response.json()
    assert "proposals" in body
    assert isinstance(body["proposals"], list)

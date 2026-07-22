from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


def test_systems_health_status_endpoint():
    client = TestClient(create_app())
    response = client.get("/systems-health/status")
    assert response.status_code == 200
    body = response.json()
    assert "system_readiness" in body
    assert "checks" in body


def test_systems_health_check_endpoint():
    client = TestClient(create_app())
    response = client.post("/systems-health/check")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] in {"GREEN", "YELLOW", "RED"}
    assert "checks" in body


def test_systems_health_history_endpoint():
    client = TestClient(create_app())
    response = client.get("/systems-health/history")
    assert response.status_code == 200
    body = response.json()
    assert "items" in body


def test_systems_health_processes_endpoint():
    client = TestClient(create_app())
    response = client.get("/systems-health/processes")
    assert response.status_code == 200
    body = response.json()
    assert "processes" in body


def test_systems_health_repair_endpoint_rejects_unsupported_action():
    client = TestClient(create_app())
    response = client.post("/systems-health/repair", json={"action": "reboot"})
    assert response.status_code == 200
    assert response.json()["status"] == "error"

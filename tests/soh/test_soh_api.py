from __future__ import annotations

from typing import Any, Dict

from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


def test_soh_status_endpoint_returns_readiness_fields() -> None:
    client = TestClient(create_app())
    response = client.get("/soh/status")
    assert response.status_code == 200
    body = response.json()
    assert body["system_readiness"] in {"GREEN", "YELLOW", "RED"}
    assert body["healthy_count"] + body["degraded_count"] + body["unhealthy_count"] >= 0
    assert isinstance(body["updated_at"], str)
    assert body["updated_at"]


def test_soh_readiness_endpoint() -> None:
    client = TestClient(create_app())
    response = client.get("/soh/readiness")
    assert response.status_code == 200
    body = response.json()
    assert "ready" in body
    assert isinstance(body["ready"], bool)


def test_soh_snapshot_endpoint() -> None:
    client = TestClient(create_app())
    response = client.get("/soh/snapshot")
    assert response.status_code == 200
    body = response.json()
    assert "readiness" in body
    assert "sac_ready" in body
    assert body["readiness"] in {"GREEN", "YELLOW", "RED"}

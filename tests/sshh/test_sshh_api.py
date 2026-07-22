from __future__ import annotations

from typing import Any, Dict

from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


def test_sshh_status_endpoint_returns_snapshot() -> None:
    client = TestClient(create_app())
    response = client.get("/sshh/status")
    assert response.status_code == 200
    body = response.json()
    assert body["system_readiness"] in {"GREEN", "YELLOW", "RED"}
    assert isinstance(body["sac_ready"], bool)


def test_sshh_heal_missing_component() -> None:
    client = TestClient(create_app())
    response = client.get("/sshh/heal/unknown")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "not_found"

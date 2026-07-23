from __future__ import annotations

from typing import Any, Dict

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def test_status_returns_readiness(client: TestClient) -> None:
    response = client.get("/schh/status")
    assert response.status_code == 200
    body = response.json()
    assert body["system_readiness"] in {"GREEN", "YELLOW", "RED"}


def test_list_components_returns_registry(client: TestClient) -> None:
    response = client.get("/schh/components")
    assert response.status_code == 200
    body = response.json()
    assert "components" in body
    assert isinstance(body["components"], list)


def test_component_detail_not_found(client: TestClient) -> None:
    response = client.get("/schh/components/does-not-exist")
    assert response.status_code == 200
    body = response.json()
    assert body.get("status") == "not_found"


def test_register_component_accepts_payload(client: TestClient) -> None:
    payload: Dict[str, Any] = {
        "id": "test-comp",
        "name": "Test Component",
        "type": "harness",
        "health_endpoint": "/health",
        "check_method": "http",
        "critical": True,
        "auto_heal": False,
        "dependencies": [],
        "metadata": {},
    }
    response = client.post("/schh/components", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body.get("status") == "registered"
    assert body.get("id") == "test-comp"


def test_unregister_component_returns_accepted(client: TestClient) -> None:
    response = client.delete("/schh/components/test-comp")
    assert response.status_code == 200
    body = response.json()
    assert body.get("status") == "unregistered"

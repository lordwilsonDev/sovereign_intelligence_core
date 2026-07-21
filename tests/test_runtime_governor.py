from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.web import create_app
from msb_v2.runtime.contracts import registry as contract_registry
from msb_v2.runtime.governor import register_runtime_capabilities


def test_register_runtime_capabilities_populates_registry() -> None:
    contract_registry()._entries.clear()
    register_runtime_capabilities()
    names = [c.name for c in contract_registry().all()]
    assert "lifecycle" in names
    assert "events" in names
    assert len(names) >= 3


def test_health_endpoint_reports_registered_capabilities() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["runtime"]["state"] == "running"
    assert isinstance(body["contracts"]["registered"], int)
    assert len(body["contracts"]["names"]) >= 3

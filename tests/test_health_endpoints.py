from __future__ import annotations

from msb_v2.api.web import create_app
from starlette.testclient import TestClient


def test_health_baseline():
    client = TestClient(create_app())
    response = client.get("/health").json()
    assert response["status"] == "ok"
    assert response["runtime"]["state"] == "running"
    assert isinstance(response["contracts"]["registered"], int)
    assert isinstance(response["contracts"]["names"], list)
    assert client.get("/runtime/ping").json() == {"status": "ok", "module": "runtime"}


def test_health_deep_and_ready():
    client = TestClient(create_app())
    deep = client.get("/health/deep").json()
    assert deep["status"] == "ok"
    assert deep["downstream"]["contract_registry"] == "ok"
    assert deep["live"]["status"] == "ok"

    ready = client.get("/health/ready").json()
    assert ready["status"] == "ready"
    assert ready["checks"]["contract_registry_ready"] is True
    assert ready["checks"]["sac_auditor_ready"] is True
    assert ready["checks"]["runtime_known"] is True

from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


def test_health_contains_runtime_and_contracts() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "runtime" in body
    assert "contracts" in body
    assert "registered" in body["contracts"]
    assert isinstance(body["contracts"]["names"], list)

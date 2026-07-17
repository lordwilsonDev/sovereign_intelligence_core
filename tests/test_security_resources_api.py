from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_security_resources_defaults() -> None:
    client = TestClient(create_app())
    response = client.get("/cognitive/security/resources", headers={"accept": "application/json"})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert isinstance(body["limits"], dict)
    assert isinstance(body["usage"], dict)
    assert isinstance(body["warnings"], list)

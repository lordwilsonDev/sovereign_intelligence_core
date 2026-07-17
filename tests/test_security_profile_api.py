from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_security_profile_defaults() -> None:
    client = TestClient(create_app())
    response = client.get("/cognitive/security/profile", headers={"accept": "application/json"})
    assert response.status_code == 200
    body = response.json()
    assert body["airgap"] is True
    assert body["allow_exec"] is False
    assert body["allow_network"] is False
    assert isinstance(body["pubkey_hex"], str)
    assert isinstance(body["registered_identities"], int)

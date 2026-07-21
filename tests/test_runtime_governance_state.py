from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


client = TestClient(create_app())


def test_governance_state_snapshot() -> None:
    response = client.get("/runtime/governance/state")
    assert response.status_code == 200
    body = response.json()
    assert "registry" in body
    assert "policy" in body
    assert "captured_at" in body
    assert isinstance(body["registry"]["capabilities"], list)
    assert isinstance(body["policy"]["rules"], list)
    assert body["registry"]["registered"] == len(body["registry"]["capabilities"])
    assert body["policy"]["registered"] == len(body["policy"]["rules"])

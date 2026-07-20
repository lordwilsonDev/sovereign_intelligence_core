from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_memory_peers() -> None:
    client = TestClient(create_app())
    response = client.get("/memory/peers")
    assert response.status_code == 200
    body = response.json()
    assert "peers" in body
    assert isinstance(body["peers"], list)

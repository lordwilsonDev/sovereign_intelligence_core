from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app

client = TestClient(create_app())


def test_v3_summary_returns_payload() -> None:
    response = client.get("/v3/summary")
    assert response.status_code == 200
    body = response.json()
    assert "capabilities" in body or "memory" in body or "constraints" in body

from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app

client = TestClient(create_app())


def test_aura_validate_accepts_payload() -> None:
    response = client.post(
        "/aura/validate",
        json={"task": {"type": "test"}, "context": {"strict": True}},
    )
    assert response.status_code == 200
    body = response.json()
    assert "ok" in body
    assert "results" in body


def test_aura_validate_rejects_missing_task() -> None:
    response = client.post("/aura/validate", json={"context": {}})
    assert response.status_code == 422

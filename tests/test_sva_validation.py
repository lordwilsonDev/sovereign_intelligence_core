from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


client = TestClient(create_app())


def test_validation_run_returns_scored_result() -> None:
    response = client.post("/validation/run", json={
        "system": "Alzheimer hypothesis",
        "domain": "medicine",
        "claim": "Amyloid removal cures disease",
    })
    assert response.status_code == 200
    body = response.json()
    assert "subject" in body
    assert "confidence" in body
    assert "evolution_required" in body
    assert 0.0 <= body["falsification_risk"] <= 1.0

from __future__ import annotations

from msb_v2.api.web import create_app
from starlette.testclient import TestClient


def test_validation_run_endpoint() -> None:
    client = TestClient(create_app())
    r = client.post(
        "/validation/run",
        json={
            "system": "test-system",
            "domain": "software",
            "claim": "claim text",
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert "subject" in data
    assert data["subject"] == "test-system:claim text"
    assert data["confidence"] == 0.8
    assert data["evidence_score"] == 0.9
    assert data["falsification_risk"] == 0.4
    assert data["assumption_count"] == 3


def test_validation_ail_endpoints() -> None:
    client = TestClient(create_app())
    r = client.post("/validation/validation/ail/invert", json={"assumption": "the system is stable"})
    assert r.status_code == 200
    data = r.json()
    assert "inversions" in data
    assert len(data["inversions"]) == 2

    r = client.post("/validation/validation/ail/mine", json={"text": "It scales horizontally. Because multiple workers handle load, failure domains shrink."})
    assert r.status_code == 200
    data = r.json()
    assert "assumptions" in data
    assert data["count"] >= 1


def test_validation_propulsion_endpoint() -> None:
    client = TestClient(create_app())
    payload = {
        "id": "c1",
        "problem": "latency",
        "assumption": "caching reduces latency",
        "inverse": "caching increases latency",
        "novelty": 0.8,
        "explanatory_power": 0.9,
        "predictive_value": 0.7,
        "verification_cost": 0.5,
        "impact": 0.9,
        "cost": 0.4,
        "complexity": 0.3,
        "risk": 0.2,
        "timing": 0.6,
        "leverage": 0.8,
    }
    r = client.post("/validation/propulsion/evaluate", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "scored" in data
    assert "ranked" in data
    assert data["scored"]["id"] == "c1"

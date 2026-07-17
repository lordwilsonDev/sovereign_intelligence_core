from __future__ import annotations


from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_evolution_scan_returns_findings() -> None:
    client = TestClient(create_app())
    response = client.post("/evolution/scan")
    assert response.status_code == 200
    body = response.json()
    assert "hotspots" in body
    assert "duplication" in body
    assert "dead_symbols" in body


def test_evolution_propose_records_proposal() -> None:
    client = TestClient(create_app())
    response = client.post("/evolution/propose", json={
        "proposal_id": "ev-1",
        "title": "tune scanner",
        "affected_modules": ["msb_v2/evolution/scanner.py"],
        "rationale": "reduce false positives"
    })
    assert response.status_code == 200
    body = response.json()
    assert body["proposal_id"] == "ev-1"
    assert body["status"] == "proposed"


def test_evolution_simulate_returns_result() -> None:
    client = TestClient(create_app())
    response = client.post("/evolution/simulate", json={"proposal_id": "ev-1", "pytest_targets": ["tests/test_verification.py"]})
    assert response.status_code == 200
    body = response.json()
    assert "passed" in body
    assert "capability_parity" in body


def test_evolution_list_proposals() -> None:
    client = TestClient(create_app())
    response = client.get("/evolution/proposals")
    assert response.status_code == 200
    body = response.json()
    assert "proposals" in body

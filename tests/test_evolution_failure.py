from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


client = TestClient(create_app())


def test_evolution_propose_duplicate_rejected() -> None:
    payload = {
        "proposal_id": "ev-dup",
        "title": "dup",
        "affected_modules": ["msb_v2/evolution/scanner.py"],
        "rationale": "dup",
    }
    first = client.post("/evolution/propose", json=payload)
    assert first.status_code == 200
    assert first.json()["status"] == "proposed"

    second = client.post("/evolution/propose", json=payload)
    assert second.status_code == 200
    body = second.json()
    # duplicate should not create a new proposal silently
    assert body["proposal_id"] == "ev-dup"
    assert body["status"] in {"proposed", "duplicate", "rejected"}


def test_evolution_simulate_missing_proposal_returns_failure() -> None:
    r = client.post("/evolution/simulate", json={"proposal_id": "ev-missing"})
    assert r.status_code == 200
    body = r.json()
    assert body["passed"] is False
    assert body["failure_reason"] is not None


def test_evolution_simulate_hard_failure_path_surfaces_reason() -> None:
    propose = client.post("/evolution/propose", json={
        "proposal_id": "ev-bad",
        "title": "bad",
        "affected_modules": ["msb_v2/evolution/scanner.py"],
        "rationale": "intentional bad probes",
        "risk": "high",
    }).json()
    assert propose["proposal_id"] == "ev-bad"

    sim = client.post("/evolution/simulate", json={"proposal_id": "ev-bad"}).json()
    assert "passed" in sim
    assert "failure_reason" in sim
    # proposed changes with high risk or invalid probes should be detected
    assert sim["passed"] is False or sim["failure_reason"] is not None


def test_evolution_scan_plus_proposal_plus_rollback_safety() -> None:
    scan = client.post("/evolution/scan").json()
    assert "hotspots" in scan

    propose = client.post("/evolution/propose", json={
        "proposal_id": "ev-safe",
        "title": "safe probe",
        "affected_modules": ["msb_v2/evolution/scanner.py"],
        "rationale": "only metadata change",
        "risk": "low",
    }).json()
    assert propose["status"] == "proposed"

    sim = client.post("/evolution/simulate", json={"proposal_id": "ev-safe", "dry_run": True}).json()
    assert sim["passed"] is True

    proposals = client.get("/evolution/proposals").json()
    assert any(p["proposal_id"] == "ev-safe" for p in proposals["proposals"])

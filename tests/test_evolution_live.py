from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


client = TestClient(create_app())


def test_evolution_live_flow() -> None:
    body = client.post("/evolution/scan").json()
    assert "hotspots" in body
    assert "duplication" in body

    propose = client.post("/evolution/propose", json={
        "proposal_id": "ev-live-1",
        "title": "tighten probe scope",
        "affected_modules": ["msb_v2/evolution/scanner.py"],
        "rationale": "reduce speculative fan-out",
    }).json()
    assert propose["proposal_id"] == "ev-live-1"

    sim_dry = client.post("/evolution/simulate", json={"proposal_id": "ev-live-1", "dry_run": True}).json()
    assert sim_dry["passed"] is True
    assert sim_dry["failure_reason"] is None

    sim_hard = client.post("/evolution/simulate", json={"proposal_id": "ev-live-1"}).json()
    assert "passed" in sim_hard
    assert "failure_reason" in sim_hard

    proposals = client.get("/evolution/proposals").json()
    assert any(p["proposal_id"] == "ev-live-1" for p in proposals["proposals"])

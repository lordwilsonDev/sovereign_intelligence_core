from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app

client = TestClient(create_app())


def test_runtime_ping_returns_status() -> None:
    response = client.get("/runtime/ping")
    assert response.status_code == 200
    body = response.json()
    assert body.get("status") == "ok"
    assert body.get("module") == "runtime"


def test_evolution_scan_returns_payload() -> None:
    response = client.post("/evolution/scan")
    assert response.status_code == 200
    body = response.json()
    assert "proposal_count" in body or "dead_symbols" in body


def test_evolution_propose_contract() -> None:
    response = client.post("/evolution/propose", json={
        "proposal_id": "p1",
        "title": "test",
        "affected_modules": ["msb_v2.aura.core"],
        "rationale": "smoke",
    })
    assert response.status_code == 200
    body = response.json()
    assert body.get("status") in {"simulated", "recorded", "accepted", "ok"} or "proposal_id" in body


def test_evolution_simulate_dry_run() -> None:
    response = client.post("/evolution/simulate", json={
        "proposal_id": "p1",
        "pytest_targets": ["msb_v2.aura.core"],
        "dry_run": True,
    })
    assert response.status_code == 200
    body = response.json()
    assert "passed" in body or "dry_run" in body or "failure_reason" in body

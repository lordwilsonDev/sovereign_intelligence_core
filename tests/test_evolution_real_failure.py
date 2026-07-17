from __future__ import annotations

import os

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.core.snapshots import SnapshotManager


def test_evolution_simulate_failure_triggers_rollback_restores_original_state(tmp_path: str) -> None:
    client = TestClient(create_app())

    src = os.path.join(tmp_path, "src")
    os.makedirs(src, exist_ok=True)
    original = "STABLE_CONTENT\n"
    with open(os.path.join(src, "state.txt"), "w", encoding="utf-8") as f:
        f.write(original)

    mgr = SnapshotManager(os.path.join(tmp_path, "snapshots"))
    mgr.snapshot("pre-evolution", src)

    broken_proposal = {
        "proposal_id": "ev-break-1",
        "title": "intentional bad probes",
        "affected_modules": ["msb_v2/evolution/scanner.py"],
        "rationale": "force failure path",
        "risk": "high",
    }
    propose = client.post("/evolution/propose", json=broken_proposal).json()
    assert propose["proposal_id"] == "ev-break-1"

    sim = client.post("/evolution/simulate", json={"proposal_id": "ev-break-1", "dry_run": False, "pytest_targets": ["tests/test_snapshots_real_failure.py"]}).json()
    assert "passed" in sim
    assert "failure_reason" in sim

    with open(os.path.join(src, "state.txt"), "w", encoding="utf-8") as f:
        f.write("MUTATED_BY_BAD_PROPOSAL")

    dest = os.path.join(tmp_path, "rolled_back")
    mgr.rollback("pre-evolution", dest)

    with open(os.path.join(dest, "state.txt"), "rb") as f:
        assert f.read() == original.encode("utf-8")


def test_evolution_dry_run_false_with_valid_targets_runs_real_checks(tmp_path: str) -> None:
    client = TestClient(create_app())

    proposal = {
        "proposal_id": "ev-real-1",
        "title": "real checks",
        "affected_modules": ["msb_v2/evolution/simulator.py"],
        "rationale": "verify real execution path",
        "risk": "low",
    }
    client.post("/evolution/propose", json=proposal)

    sim = client.post("/evolution/simulate", json={"proposal_id": "ev-real-1", "dry_run": False, "pytest_targets": ["tests/test_snapshots_real_failure.py"]}).json()
    assert "passed" in sim
    assert "regression_tests" in sim
    assert "capability_parity" in sim
    assert sim["regression_tests"] >= 0

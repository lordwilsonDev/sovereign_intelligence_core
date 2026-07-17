from __future__ import annotations

import json

import pytest

from msb_v2.core.evolution_memory import EvolutionMemory


@pytest.fixture
def mem(tmp_path):
    db = tmp_path / "evolution_memory.db"
    return EvolutionMemory(str(db))


def test_record_and_get_proposal(mem: EvolutionMemory) -> None:
    proposal = {
        "proposal_id": "prop-1",
        "module": "msb_v2/knowledge.py",
        "patch_hash": "abc",
        "change_type": "refactor",
    }
    proposal_id = mem.record_proposal(
        proposal=proposal,
        result="accepted",
        reason="tests pass",
        lesson="keep it small",
        metrics_before={"vdr": 0.1},
        metrics_after={"vdr": 0.4},
    )
    assert proposal_id == "prop-1"
    row = mem.get_proposal("prop-1")
    assert row is not None
    assert row["module"] == "msb_v2/knowledge.py"
    assert row["result"] == "accepted"


def test_record_event_and_list(mem: EvolutionMemory) -> None:
    mem.record_event("prop-1", "build", "nothing broke", {"vdr": 0.4}, "continue")
    events = mem.get_events("prop-1")
    assert len(events) == 1
    assert events[0]["stage"] == "build"
    assert json.loads(events[0]["metric_delta"]) == {"vdr": 0.4}


def test_historical_confidence(mem: EvolutionMemory) -> None:
    for i, result in enumerate(("accepted", "rejected", "accepted")):
        mem.record_proposal(
            proposal={"proposal_id": f"prop-{i}", "module": "msb_v2/knowledge.py", "change_type": "refactor"},
            result=result,
            reason="",
            lesson="",
            metrics_before={},
            metrics_after={},
        )
    conf = mem.get_historical_confidence("msb_v2/knowledge.py", "refactor")
    assert abs(conf - 2/3) < 1e-9


def test_capability_baseline_roundtrip(mem: EvolutionMemory) -> None:
    mem.set_capability_baseline("demo", 0.9, tolerance=0.05)
    row = mem.get_capability_baseline("demo")
    assert row is not None
    assert abs(row["expected_value"] - 0.9) < 1e-9
    all_b = mem.get_all_capability_baselines()
    assert "demo" in all_b
    assert abs(all_b["demo"]["expected"] - 0.9) < 1e-9


def test_similar_proposals_empty(mem: EvolutionMemory) -> None:
    assert mem.get_similar_proposals("msb_v2/unknown.py") == []
    assert mem.get_historical_confidence("msb_v2/unknown.py") == 1.0

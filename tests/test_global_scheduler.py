from __future__ import annotations

import tempfile

from msb_v2.core.evolution_memory import EvolutionMemory
from msb_v2.core.falsification_mirror import FalsificationMirror
from msb_v2.core.global_scheduler import GlobalScheduler


def _tmp_mem(tmp_path):
    from pathlib import Path
    db = Path(tmp_path) / "evolution_memory.db"
    return EvolutionMemory(str(db))


def test_phase4_scheduler_sets_baseline_and_accepts():
    with tempfile.TemporaryDirectory() as tmp:
        mem = _tmp_mem(tmp)
        scheduler = GlobalScheduler(mem)

        proposal = {
            "proposal_id": "phase4-001",
            "module": "mock-module",
            "update_baseline": True,
        }

        outcome = scheduler.execute_cycle(proposal, mode="simulate")
        assert outcome["mode"] == "simulate"
        assert "capability_results" in outcome
        assert "mirror" in outcome
        baseline = mem.get_capability_baseline(list(outcome["capability_results"]["summary"].keys())[0])
        assert baseline is not None
        assert outcome["decision"] == "accepted"
        assert outcome["accepted"] is True


def test_phase4_scheduler_rejects_after_falsification():
    with tempfile.TemporaryDirectory() as tmp:
        mem = _tmp_mem(tmp)
        mirror = FalsificationMirror(mem)
        scheduler = GlobalScheduler(mem, mirror=mirror)

        # Force a falsified outcome regardless of live capability scores
        scheduler.mirror.evaluate_batch = lambda results: {
            "checks": [],
            "falsified": [{"category": "demo", "status": "FALSIFIED"}],
            "coherence_rate": 0.0,
        }

        proposal = {
            "proposal_id": "phase4-bad",
            "module": "breakage-module",
            "update_baseline": False,
        }

        outcome = scheduler.execute_cycle(proposal, mode="simulate")
        assert outcome["decision"] == "rejected"
        assert outcome["accepted"] is False
        assert "demo" in outcome["falsified_categories"]


def test_phase4_scheduler_accepts_when_coherent():
    with tempfile.TemporaryDirectory() as tmp:
        mem = _tmp_mem(tmp)
        mirror = FalsificationMirror(mem)
        scheduler = GlobalScheduler(mem, mirror=mirror)

        proposal = {
            "proposal_id": "phase4-good",
            "module": "ok-module",
            "update_baseline": False,
        }

        outcome = scheduler.execute_cycle(proposal, mode="simulate")
        assert outcome["decision"] == "accepted"
        assert outcome["accepted"] is True

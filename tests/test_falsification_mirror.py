from __future__ import annotations


import pytest

from msb_v2.core.evolution_memory import EvolutionMemory
from msb_v2.core.falsification_mirror import FalsificationMirror


def _tmp_db(tmp_path):
    db = tmp_path / "evolution_memory.db"
    return EvolutionMemory(str(db))


def test_no_baseline_status(tmp_path):
    mem = _tmp_db(tmp_path)
    mirror = FalsificationMirror(mem)
    outcome = mirror.evaluate("demo", 0.95)
    assert outcome["status"] == "NO_BASELINE"
    assert outcome["r_i"] is None


def test_coherent_when_within_tolerance(tmp_path):
    mem = _tmp_db(tmp_path)
    mem.set_capability_baseline("demo", expected_value=0.9, tolerance=0.05)
    mirror = FalsificationMirror(mem)
    outcome = mirror.evaluate("demo", 0.93)
    assert outcome["status"] == "COHERENT"
    assert outcome["r_i"] == 1.0
    assert outcome["delta"] == pytest.approx(0.03)


def test_falsified_when_outside_tolerance(tmp_path):
    mem = _tmp_db(tmp_path)
    mem.set_capability_baseline("demo", expected_value=0.9, tolerance=0.05)
    mirror = FalsificationMirror(mem)
    outcome = mirror.evaluate("demo", 0.2)
    assert outcome["status"] == "FALSIFIED"
    assert outcome["r_i"] < 1.0


def test_r_i_boundary(tmp_path):
    mem = _tmp_db(tmp_path)
    mem.set_capability_baseline("demo", expected_value=0.95, tolerance=0.01)
    mirror = FalsificationMirror(mem)
    outcome = mirror.evaluate("demo", 0.95)
    assert outcome["r_i"] == 1.0

    outcome = mirror.evaluate("demo", 0.01)
    assert outcome["status"] == "FALSIFIED"


def test_history_filters(tmp_path):
    mem = _tmp_db(tmp_path)
    mem.set_capability_baseline("demo", expected_value=0.9, tolerance=0.05)
    mirror = FalsificationMirror(mem)
    mirror.evaluate("demo", 0.9)
    mirror.evaluate("demo", 0.2)

    rows = mirror.history(category="demo")
    assert len(rows) == 2
    rows_status = mirror.history(status="FALSIFIED")
    assert all(r["status"] == "FALSIFIED" for r in rows_status)


def test_evaluate_batch_counts_falsified(tmp_path):
    mem = _tmp_db(tmp_path)
    mem.set_capability_baseline("demo", expected_value=0.95, tolerance=0.01)
    mem.set_capability_baseline("health", expected_value=0.9, tolerance=0.05)
    mirror = FalsificationMirror(mem)

    capability_results = {
        "summary": {
            "demo": {"average_score": 0.9, "pass_rate": 1.0, "total": 1},
            "health": {"average_score": 0.1, "pass_rate": 0.0, "total": 1},
        }
    }

    batch = mirror.evaluate_batch(capability_results)
    assert batch["coherence_rate"] == pytest.approx(0.5)
    assert len(batch["falsified"]) == 1
    assert batch["falsified"][0]["category"] == "health"

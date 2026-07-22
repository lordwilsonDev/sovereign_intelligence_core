from __future__ import annotations

from msb_v2.optimization.engine import OptimizationEngine, ProposalStatus


def test_analyze_generates_proposals_for_high_cpu():
    engine = OptimizationEngine()
    proposals = engine.analyze({"cpu_percent": 0.95, "memory_percent": 0.1, "disk_percent": 0.1})
    assert any(p["target"] == "cpu_limit" for p in proposals)


def test_analyze_generates_proposals_for_high_memory():
    engine = OptimizationEngine()
    proposals = engine.analyze({"cpu_percent": 0.1, "memory_percent": 0.95, "disk_percent": 0.1})
    assert any(p["target"] == "memory_limit" for p in proposals)


def test_analyze_generates_proposals_for_high_disk():
    engine = OptimizationEngine()
    proposals = engine.analyze({"cpu_percent": 0.1, "memory_percent": 0.1, "disk_percent": 0.95})
    assert any(p["target"] == "disk_cleanup" for p in proposals)


def test_status_returns_last_run():
    engine = OptimizationEngine()
    engine.analyze({"cpu_percent": 0.1, "memory_percent": 0.1, "disk_percent": 0.1})
    status = engine.status()
    assert status["last_run"] is not None

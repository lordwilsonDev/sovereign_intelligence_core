from __future__ import annotations

from msb_v2.optimization.engine import OptimizationEngine


def test_apply_changes_proposal_status():
    engine = OptimizationEngine()
    engine.analyze({"cpu_percent": 0.95})
    proposals = engine.proposals()
    assert proposals
    proposal_id = proposals[0]["id"]
    result = engine.apply(proposal_id)
    assert result["status"] == "applied"
    assert result["id"] == proposal_id


def test_rollback_restores_previous_value():
    engine = OptimizationEngine()
    engine.analyze({"cpu_percent": 0.95})
    proposals = engine.proposals()
    proposal_id = proposals[0]["id"]
    engine.apply(proposal_id)
    result = engine.rollback(proposal_id)
    assert result["status"] == "rolled_back"
    assert result["id"] == proposal_id


def test_apply_unknown_proposal_returns_none():
    engine = OptimizationEngine()
    assert engine.apply("missing") is None


def test_rollback_unknown_proposal_returns_none():
    engine = OptimizationEngine()
    assert engine.rollback("missing") is None

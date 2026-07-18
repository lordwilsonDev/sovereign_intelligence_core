from __future__ import annotations

from msb_v2.planning.axiom_inversion import AxiomInversionEngine, PlanningState


def test_planning_state_enum():
    assert PlanningState.DRAFT.value == "draft"
    assert PlanningState.FAILED.value == "failed"


def test_axiom_inversion_engine_invert():
    engine = AxiomInversionEngine()
    out = engine.invert("This feature is safe")
    assert "opposite" in out
    assert "feature" in out


def test_evidence_score():
    engine = AxiomInversionEngine()
    assert engine.evidence_score("some claim", True) == 0.8
    assert engine.evidence_score("some claim", False) == 0.2


def test_constraints_ok_blocks_high_cost():
    engine = AxiomInversionEngine()
    node = {"cost_estimate": 11.0}
    constraints = {"max_cost": 10.0}
    assert engine.constraints_ok(node, constraints) is False


def test_rank_sorts_descending():
    engine = AxiomInversionEngine()
    nodes = [{"score": 0.3}, {"score": 0.9}, {"score": 0.1}]
    ranked = engine.rank(nodes)
    assert [n["score"] for n in ranked] == [0.9, 0.3, 0.1]

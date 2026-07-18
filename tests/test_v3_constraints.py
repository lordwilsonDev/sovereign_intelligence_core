from __future__ import annotations

from msb_v2.v3.constraints import Constraint, ConstraintEngine


def test_passes_with_no_constraints():
    engine = ConstraintEngine()
    assert engine.check({"cost_estimate": 0.5, "autonomy_level": "observe"}).get("passed") is True


def test_rejects_above_cost():
    engine = ConstraintEngine([Constraint(name="budget", description="cap", max_cost=0.1)])
    result = engine.check({"cost_estimate": 5.0, "autonomy_level": "observe"})
    assert result["passed"] is False
    assert result["violations"][0]["constraint"] == "budget"


def test_rejects_autonomy():
    engine = ConstraintEngine([Constraint(name="autonomy", description="autonomy", required_autonomy="recommend")])
    result = engine.check({"cost_estimate": 0.0, "autonomy_level": "observe"})
    assert result["passed"] is False


def test_passes_autonomy():
    engine = ConstraintEngine([Constraint(name="autonomy", description="autonomy", required_autonomy="recommend")])
    result = engine.check({"cost_estimate": 0.0, "autonomy_level": "recommend"})
    assert result["passed"] is True

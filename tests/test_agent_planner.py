from __future__ import annotations

from msb_v2.agent.planner import Plan, Step, fallback_plan


def test_plan_valid_true_with_steps():
    plan = Plan(goal="g", steps=[Step(step=1, tool="noop", description="x", critical=True)])
    assert plan.valid() is True


def test_plan_valid_false_when_steps_empty():
    plan = Plan(goal="g", steps=[])
    assert plan.valid() is False


def test_fallback_plan_returns_single_noop_step():
    plan = fallback_plan("anything")
    assert plan.goal == "anything"
    assert len(plan.steps) == 1
    assert plan.steps[0].tool == "noop"

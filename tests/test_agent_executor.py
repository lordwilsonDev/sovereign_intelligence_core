from __future__ import annotations

import threading

from msb_v2.agent.executor import execute
from msb_v2.agent.planner import Plan, Step


def test_execute_completes_noop_step():
    plan = Plan(goal="g", steps=[Step(step=1, tool="noop", description="noop", critical=True)])
    result = execute(plan.goal, plan=plan)
    assert "Completed" in result


def test_execute_cancels_when_flag_set():
    cancel = threading.Event()
    cancel.set()
    plan = Plan(goal="g", steps=[Step(step=1, tool="noop", description="noop", critical=True)])
    result = execute(plan.goal, cancel_flag=cancel, plan=plan)
    assert result == "Task cancelled."


def test_execute_unknown_tool_recovers_via_noop():
    plan = Plan(goal="g", steps=[Step(step=1, tool="unknown", description="x", critical=True)])
    result = execute(plan.goal, plan=plan)
    assert "Completed" in result

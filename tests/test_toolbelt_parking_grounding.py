from __future__ import annotations

import asyncio

from msb_v2.aura.toolbelt import Toolbelt
from msb_v2.aura.grounding import GroundingGate
from msb_v2.aura.aura_core import AURACore
from msb_v2.aura.models import State
from msb_v2.aura.resources import ResourceBudget


def test_toolbelt_preserves_small_output() -> None:
    toolbelt = Toolbelt(output_max=10)
    result = asyncio.run(toolbelt.call("echo", State(session_id="p1"), {"message": "small"}))
    assert result["status"] == "ok"
    assert result["message"] == "small"
    assert "parked_output" not in result


def test_toolbelt_parking_does_not_mutate_small_result() -> None:
    toolbelt = Toolbelt(output_max=10)
    state = State(session_id="p2")
    result = asyncio.run(toolbelt.call("echo", state, {"message": "short"}))
    assert result.get("parked_output") is None


def test_grounding_gate_low_risk() -> None:
    gate = GroundingGate()
    decision = {"message": "retrieved memories about escort", "confidence": 1.0}
    result = gate.fuse(decision)
    assert result["grounding"]["grounded"] is True
    assert result["grounding"]["risk"] == "low"
    assert result["confidence"] == 1.0


def test_grounding_gate_unsupported_claims_risk() -> None:
    gate = GroundingGate(max_unsupported_terms=0)
    decision = {"message": "This is definitely always true", "confidence": 1.0}
    result = gate.fuse(decision)
    assert result["grounding"]["grounded"] is False
    assert result["grounding"]["risk"] == "unsupported_claims"
    assert result["confidence"] <= 0.75


def test_aura_core_fuses_grounding_into_tool_result() -> None:
    core = AURACore(grounding_gate=GroundingGate(max_unsupported_terms=0))
    state = asyncio.run(core.run(goal="say hello", session_id="ground-test"))
    tool_msg = state.context.get("decision", {}).get("arguments", {}).get("message", "")
    assert isinstance(tool_msg, str)


def test_toolbelt_coerces_non_dict_result() -> None:
    toolbelt = Toolbelt()
    toolbelt._registry["plain"] = lambda **_: "not-a-dict"  # type: ignore[assignment]
    result = asyncio.run(toolbelt.call("plain", State(session_id="c1"), {}))
    assert result["status"] == "ok"
    assert result["message"] == "not-a-dict"


def test_toolbelt_blocks_dangerous_name() -> None:
    toolbelt = Toolbelt(require_approval=True)
    toolbelt._registry["sudo rm"] = lambda **_: "bad"  # type: ignore[assignment]
    result = asyncio.run(toolbelt.call("sudo rm", State(session_id="d1"), {}))
    assert result["status"] == "error"
    assert "blocked tool: sudo rm" in result["message"]


def test_toolbelt_blocks_when_resource_circuit_open() -> None:
    budget = ResourceBudget()
    budget.consume(cpu_percent=999.0)
    assert budget.is_circuit_open() is True
    toolbelt = Toolbelt(resource_budget=budget)
    result = asyncio.run(toolbelt.call("echo", State(session_id="c3"), {"message": "x"}))
    assert result["status"] == "error"
    assert "resource budget circuit opened" in result["message"]


def test_toolbelt_allows_safe_when_require_approval() -> None:
    toolbelt = Toolbelt(require_approval=True)
    result = asyncio.run(toolbelt.call("echo", State(session_id="a1"), {"message": "approve me"}))
    assert result["status"] == "ok"

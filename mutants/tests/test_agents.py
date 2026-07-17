from __future__ import annotations

from msb_v2.agents.repair import run_repair
from msb_v2.agents.tool_agent import run_tool_agent


def test_repair_agent_returns_contract():
    result = run_repair(problem="invert cloud billing", context="segment B")
    assert result["status"] == "ok"
    assert 0.0 <= float(result["confidence"]) <= 1.0
    assert result["action"] in {"propose_inversion", "escalate_to_human"}


def test_repair_handles_missing_input():
    result = run_repair()
    assert result["status"] == "error"


def test_tool_agent_returns_contract():
    result = run_tool_agent(tool="broadcast", arguments={"claim_id": "c01"})
    assert result["status"] == "ok"
    assert result["tool"] == "broadcast"


def test_tool_agent_handles_missing_tool():
    result = run_tool_agent()
    assert result["status"] == "error"

from __future__ import annotations

from typing import Any, Dict, List

from msb_v2.agents.repair import run_repair
from msb_v2.agents.tool_agent import run_tool_agent
from msb_v2.engine.moie_types import Claim, HiveMindNode


class RepairNode(HiveMindNode):
    role = "repair"

    def deliberate(self, claim: Claim, context: Dict[str, Any]) -> tuple[str, str, float]:
        result = run_repair(problem=claim.text, context=str(context))
        stance = "support" if result.get("action") == "propose_inversion" else "refine"
        return stance, str(result.get("message", "")), float(result.get("confidence", 0.5))


class ToolNode(HiveMindNode):
    role = "tool_agent"

    def deliberate(self, claim: Claim, context: Dict[str, Any]) -> tuple[str, str, float]:
        result = run_tool_agent(tool="moie_broadcast", arguments={"claim_id": claim.id})
        return "support", str(result.get("message", "")), float(result.get("confidence", 0.5))


def executable_nodes() -> List[HiveMindNode]:
    return [RepairNode(), ToolNode()]

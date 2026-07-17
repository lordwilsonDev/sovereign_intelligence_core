from __future__ import annotations

from typing import List

from msb_v2.engine.moie_types import Claim, HiveMindNode


class TechnicalNode(HiveMindNode):
    role = "technical"

    def deliberate(self, claim: Claim, context: dict) -> tuple[str, str, float]:
        if "software" in claim.text.lower() or "api" in claim.text.lower() or "system" in claim.text.lower():
            return "support", "Technical feasibility is high for software-system inversions", 0.85
        return "refine", "Needs a more specific technical artifact to evaluate", 0.6


class FirstPrinciplesNode(HiveMindNode):
    role = "first_principles"

    def deliberate(self, claim: Claim, context: dict) -> tuple[str, str, float]:
        impact = float(claim.scores.get("impact", 0.5))
        if impact >= 0.7:
            return "support", "First-principles boundary is crossed; existing models likely wrong", 0.8
        return "reject", "Impact too low to override incumbent assumption", 0.75


class SystemicNode(HiveMindNode):
    role = "systemic"

    def deliberate(self, claim: Claim, context: dict) -> tuple[str, str, float]:
        score = float(claim.scores.get("confidence", 0.5))
        if score >= 0.6:
            return "support", "Systemic second-order effects are favorable", 0.7
        return "refine", "Systemic ripple effects are unverified; needs causal memory", 0.55


class SkepticNode(HiveMindNode):
    role = "skeptic"

    def deliberate(self, claim: Claim, context: dict) -> tuple[str, str, float]:
        if len(claim.text.split()) <= 6:
            return "reject", "Claim is too vague to falsify", 0.9
        return "outside_scope", "Needs operationalized falsification criteria", 0.4


def default_nodes() -> List[HiveMindNode]:
    return [TechnicalNode(), FirstPrinciplesNode(), SystemicNode(), SkepticNode()]

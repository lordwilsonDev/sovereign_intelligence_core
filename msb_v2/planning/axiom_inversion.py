from __future__ import annotations

from enum import Enum


class PlanningState(str, Enum):
    DRAFT = "draft"
    INVERTED = "inverted"
    EVIDENCE = "evidence"
    CONSTRAINED = "constrained"
    RANKED = "ranked"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"


class AxiomInversionEngine:
    @staticmethod
    def invert(assumption: str) -> str:
        a = assumption.strip()
        if not a:
            return ""
        if "not " in a.casefold():
            return a
        return f"What if the opposite is true: {a}"

    @staticmethod
    def evidence_score(inverted: str, supports: bool) -> float:
        if not inverted:
            return 0.0
        return 0.8 if supports else 0.2

    @staticmethod
    def constraints_ok(node: dict, constraints: dict) -> bool:
        if constraints.get("max_cost") is not None and node.get("cost_estimate", 0) > constraints["max_cost"]:
            return False
        if constraints.get("required_autonomy") is not None and node.get("autonomy_level", "") != constraints["required_autonomy"]:
            return False
        return True

    @staticmethod
    def rank(nodes: list[dict]) -> list[dict]:
        return sorted(nodes, key=lambda x: x.get("score", 0.0), reverse=True)

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class Constraint:
    name: str
    description: str
    enabled: bool = True
    max_cost: Optional[float] = None
    required_autonomy: Optional[str] = None
    allowed_tools: Optional[List[str]] = None
    tags: Optional[List[str]] = None


class ConstraintEngine:
    def __init__(self, constraints: Optional[List[Constraint]] = None) -> None:
        self._constraints: Dict[str, Constraint] = {c.name: c for c in (constraints or []) if c.enabled}

    def register(self, constraint: Constraint) -> Constraint:
        if constraint.enabled:
            self._constraints[constraint.name] = constraint
        return constraint

    def check(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        result: Dict[str, Any] = {"passed": True, "violations": []}
        for constraint in self._constraints.values():
            violation = self._evaluate(constraint, payload)
            if violation:
                result["passed"] = False
                result["violations"].append(violation)
        return result

    def _evaluate(self, constraint: Constraint, payload: Dict[str, Any]) -> Optional[Dict[str, str]]:
        if constraint.max_cost is not None:
            cost = float(payload.get("cost_estimate", 0.0) or 0.0)
            if cost > constraint.max_cost:
                return {"constraint": constraint.name, "reason": f"cost {cost} exceeds {constraint.max_cost}"}

        if constraint.required_autonomy is not None:
            autonomy = payload.get("autonomy_level", "observe")
            allowed = {"observe": 0, "recommend": 1, "draft": 2, "execute_with_confirmation": 3, "execute_within_policy": 4, "autonomous_execution": 5}
            requested = allowed.get(autonomy, -1)
            required = allowed.get(constraint.required_autonomy, -1)
            if requested < 0 or required < 0 or requested < required:
                return {"constraint": constraint.name, "reason": f"autonomy {autonomy} below required {constraint.required_autonomy}"}

        if constraint.allowed_tools is not None:
            tool = payload.get("tool")
            if tool and tool not in constraint.allowed_tools:
                return {"constraint": constraint.name, "reason": f"tool {tool} is not allowed"}

        if constraint.tags is not None:
            request_tags = payload.get("tags", []) or []
            if not set(constraint.tags).intersection(set(request_tags)):
                return {"constraint": constraint.name, "reason": "missing required tags"}

        return None

    def list(self) -> List[Constraint]:
        return list(self._constraints.values())

    def summary(self) -> Dict[str, Any]:
        enabled = [c.name for c in self._constraints.values() if c.enabled]
        return {"count": len(self._constraints), "enabled": enabled}

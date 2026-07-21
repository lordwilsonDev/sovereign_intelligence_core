from __future__ import annotations

import logging
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class EnforcementLevel(str, Enum):
    ADVISORY = "advisory"
    WARN = "warn"
    BLOCK = "block"
    REQUIRE_APPROVAL = "approval"
    AUTO_ROLLBACK = "rollback"


@dataclass(frozen=True)
class GovernanceRule:
    rule_id: str
    name: str
    category: str
    enforcement: EnforcementLevel
    condition: Optional[Callable[[Dict[str, Any]], bool]] = None
    rationale: str = ""
    owner: str = "system"
    metadata: Dict[str, Any] = field(default_factory=dict)


class PolicyEngine:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._rules: Dict[str, GovernanceRule] = {}

    def register(self, rule: GovernanceRule) -> None:
        with self._lock:
            self._rules[rule.rule_id] = rule

    def evaluate(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        for rule in self._rules.values():
            triggered = False
            if rule.condition is not None:
                try:
                    triggered = bool(rule.condition(context))
                except Exception:
                    triggered = False
            results.append({
                "rule_id": rule.rule_id,
                "name": rule.name,
                "enforcement": rule.enforcement.value,
                "triggered": triggered,
                "owner": rule.owner,
            })
        return results


_policy_engine = PolicyEngine()


def policy_engine() -> PolicyEngine:
    return _policy_engine


def register_default_rules() -> None:
    engine = policy_engine()
    engine.register(GovernanceRule(
        rule_id="re-allow-unsigned-mutation",
        name="Capability Mutation Requires Signature",
        category="mutation",
        enforcement=EnforcementLevel.BLOCK,
        condition=lambda ctx: ctx.get("mutation_unsigned", False),
        rationale="All capability mutations require scalloped approval.",
        owner="governor",
    ))
    engine.register(GovernanceRule(
        rule_id="re-max-failure-rate",
        name="Maximum Allowable Failure Rate",
        category="reliability",
        enforcement=EnforcementLevel.WARN,
        condition=lambda ctx: ctx.get("failure_rate", 0.0) > 0.25,
        rationale="Failure rate exceeds 25% threshold.",
        owner="sre",
    ))

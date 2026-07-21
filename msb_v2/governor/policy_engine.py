from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class PolicyRule:
    id: str
    name: str
    condition: str
    action: str
    enabled: bool = True


class PolicyEngine:
    def __init__(self) -> None:
        self._rules: Dict[str, PolicyRule] = {}
        self._load_defaults()

    def _load_defaults(self) -> None:
        default = [
            PolicyRule(id="block_force_push_main", name="Block force push to main", condition='event == "force_push" and branch == "main"', action="veto"),
            PolicyRule(id="block_on_sqa_failure", name="Block downstream deployments on SQA failure", condition='harness == "sqa" and status != "pass"', action="veto"),
            PolicyRule(id="model_download_approval", name='Require approval for model downloads >10GB', condition='action == "model_download" and size_gb > 10', action="notify"),
            PolicyRule(id="memory_suspend_policy", name='Suspend LRU deployments if memory >80%', condition='action == "deploy" and memory_pct > 80', action="suspend"),
        ]
        for rule in default:
            self._rules[rule.id] = rule

    def rule(self, policy_id: str) -> Optional[PolicyRule]:
        return self._rules.get(policy_id)

    def rules(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": r.id,
                "name": r.name,
                "condition": r.condition,
                "action": r.action,
                "enabled": r.enabled,
            }
            for r in self._rules.values()
        ]

    def add_rule(self, rule: PolicyRule) -> Dict[str, Any]:
        self._rules[rule.id] = rule
        return {"status": "added", "rule_id": rule.id}

    def remove_rule(self, policy_id: str) -> Dict[str, Any]:
        if policy_id in self._rules:
            del self._rules[policy_id]
            return {"status": "removed", "rule_id": policy_id}
        return {"status": "not_found", "rule_id": policy_id}

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not context:
            return {"status": "pass", "violations": []}
        violations = []
        for rule in self._rules.values():
            if not rule.enabled:
                continue
            if self._matches(rule.condition, context):
                violations.append({"rule_id": rule.id, "action": rule.action, "context": context})
        if violations:
            return {"status": "violation", "violations": violations}
        return {"status": "pass", "violations": []}

    def _matches(self, condition: str, context: Dict[str, Any]) -> bool:
        if " and " in condition:
            return all(self._matches(part.strip(), context) for part in condition.split(" and "))
        if "==" in condition:
            left, right = condition.split("==", maxsplit=1)
            return str(context.get(left.strip())).strip('"') == right.strip().strip('"')
        if ">" in condition:
            left, right = condition.split(">", maxsplit=1)
            try:
                return float(context.get(left.strip(), 0)) > float(right.strip())
            except ValueError:
                return False
        return False

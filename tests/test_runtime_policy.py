from __future__ import annotations

import pytest

from msb_v2.runtime.policy import (
    EnforcementLevel,
    GovernanceRule,
    PolicyEngine,
    policy_engine,
    register_default_rules,
)


def test_register_and_evaluate_block_rule() -> None:
    engine = PolicyEngine()
    engine.register(
        GovernanceRule(
            rule_id="r1",
            name="Signed mutations only",
            category="mutation",
            enforcement=EnforcementLevel.BLOCK,
            condition=lambda ctx: ctx.get("unsigned", False),
            rationale="...",
        )
    )
    results = engine.evaluate({"unsigned": True})
    assert results[0]["triggered"] is True
    assert results[0]["enforcement"] == "block"
    assert results[0]["rule_id"] == "r1"


def test_default_rules_evaluate() -> None:
    register_default_rules()
    results = policy_engine().evaluate({"mutation_unsigned": True})
    ids = [r["rule_id"] for r in results]
    assert "re-allow-unsigned-mutation" in ids

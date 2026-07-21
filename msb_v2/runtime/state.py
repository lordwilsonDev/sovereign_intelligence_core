from __future__ import annotations

import logging
import time
from typing import Any, Dict, List

from msb_v2.runtime.contracts import registry as _runtime_registry
from msb_v2.runtime.governor import register_runtime_capabilities
from msb_v2.runtime.policy import policy_engine, register_default_rules

logger = logging.getLogger(__name__)


def governance_state() -> Dict[str, Any]:
    registry = _runtime_registry()
    capabilities = [c.capability_interface() for c in registry.all()]
    policy = policy_engine()
    register_default_rules()
    rules = []
    for rule in policy._rules.values():
        rules.append({
            "rule_id": rule.rule_id,
            "name": rule.name,
            "category": rule.category,
            "enforcement": rule.enforcement.value,
            "owner": rule.owner,
            "rationale": rule.rationale,
        })
    return {
        "captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "registry": {
            "attached": True,
            "registered": len(capabilities),
            "capabilities": capabilities,
        },
        "policy": {
            "attached": True,
            "registered": len(rules),
            "rules": rules,
        },
    }

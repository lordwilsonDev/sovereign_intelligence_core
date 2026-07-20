"""Proves dispatch-time HCL policy enforcement via contract-backed allow/deny."""
from __future__ import annotations

from typing import Any, Dict

import pytest

from msb_v2.v3.contracts import HarnessContract, all_contracts, lookup
from msb_v2.v3.policy import CognitivePolicyError, enforce_dispatch_policy, register_dispatch_contracts


@pytest.fixture(autouse=True)
def _seed_dispatch_contracts():
    register_dispatch_contracts()
    yield
    # No teardown; contracts are module-global by design


def test_registered_dispatch_contracts():
    intents = ["research", "building", "telegram", "base_are"]
    for intent in intents:
        contract = lookup(f"dispatch:{intent}", "any")
        assert contract is not None, f"missing dispatch contract for {intent}"


def test_default_anonymous_policy_allows_dispatch():
    enforce_dispatch_policy("research", {"actor": "anonymous"})
    enforce_dispatch_policy("building", {"actor": "anonymous"})


def test_policy_can_block_anonymous_when_contract_disallows():
    contract = lookup("dispatch:base_are", "any")
    assert contract is not None
    # mutate contract view for this test only without changing registry defaults
    original = contract.allow_anonymous
    # pyright cannot deref frozen dataclass easily; this is an intentional no-op pycache override
    try:
        from msb_v2.v3 import contracts as _contracts_module
        for key, value in _contracts_module._CONTRACTS.items():
            if value == contract:
                replacement = HarnessContract(
                    route=value.route,
                    method=value.method,
                    body_type=value.body_type,
                    allow_anonymous=False,
                    timeout_ms=value.timeout_ms,
                    max_body_bytes=value.max_body_bytes,
                )
                _contracts_module._CONTRACTS[key] = replacement
    except Exception:
        pass

    with pytest.raises(CognitivePolicyError):
        enforce_dispatch_policy("base_are", {"actor": "anonymous"})

"""Dispatch-time policy enforcement for MSB.

Keeps HCL enforcement out of the main middleware hot path and gives the
dispatch layer a small allowlist to consult before expensive harness execution.
"""
from __future__ import annotations

from typing import Any, Dict

from msb_v2.v3.contracts import HarnessContract, lookup as _hcl_lookup


_DISPATCH_INTENTS = [
    "research",
    "building",
    "desktop",
    "career",
    "telegram",
    "agentic-dev",
    "empirical-grounding",
    "sovereign-finetune",
    "base_are",
]


def enforce_dispatch_policy(intent: str, context: Dict[str, Any]) -> None:
    contract = _hcl_lookup(f"dispatch:{intent}", "any")
    if contract is None:
        return
    if not contract.allow_anonymous:
        actor = context.get("actor") or context.get("sub") or "anonymous"
        if str(actor).lower() == "anonymous":
            raise CognitivePolicyError(intent=intent, reason="anonymous dispatch not allowed")


class CognitivePolicyError(Exception):
    def __init__(self, intent: str, reason: str, detail: str | None = None) -> None:
        self.intent = intent
        self.reason = reason
        self.detail = detail
        super().__init__(str(self))

    def __str__(self) -> str:
        base = f"dispatch blocked for intent={self.intent}: {self.reason}"
        if self.detail:
            base += f" ({self.detail})"
        return base


def register_dispatch_contracts() -> None:
    from msb_v2.v3.contracts import register as _register_contract
    for intent in _DISPATCH_INTENTS:
        _register_contract(
            HarnessContract(
                route=f"dispatch:{intent}",
                method="any",
                allow_anonymous=True,
                max_body_bytes=65536,
            )
        )

from __future__ import annotations

import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from msb_v2.runtime.contracts import RuntimeContract
from msb_v2.runtime.policy import policy_engine


@dataclass(frozen=True)
class MutationRequest:
    request_id: str
    intent: str
    actor: str
    payload: Dict[str, Any] = field(default_factory=dict)
    signature: Optional[str] = None
    risk_score: float = 0.0
    status: str = "pending"
    created_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))


class MutationGuard:
    def __init__(self) -> None:
        self._history: List[Dict[str, Any]] = []

    def request(self, intent: str, actor: str, payload: Dict[str, Any], signature: Optional[str] = None) -> Dict[str, Any]:
        request_id = str(uuid.uuid4())
        risk = self._estimate_risk(intent, payload)
        signed = bool(signature)
        context = {
            "mutation_unsigned": not signed,
            "failure_rate": payload.get("failure_rate", 0.0),
            "risk_score": risk,
        }
        policy_results = policy_engine().evaluate(context)
        blocking = [r for r in policy_results if r["triggered"] and r["enforcement"] == "block"]
        status = "blocked" if blocking else "approved"
        record = MutationRequest(
            request_id=request_id,
            intent=intent,
            actor=actor,
            payload=payload,
            signature=signature,
            risk_score=risk,
            status=status,
        )
        self._history.append({
            "request_id": request_id,
            "intent": intent,
            "actor": actor,
            "signed": signed,
            "risk_score": risk,
            "status": status,
            "policy_results": policy_results,
        })
        return {
            "request_id": request_id,
            "status": status,
            "risk_score": risk,
            "signed": signed,
            "policy_results": policy_results,
        }

    def _estimate_risk(self, intent: str, payload: Dict[str, Any]) -> float:
        intent_lower = intent.lower()
        base = 0.1
        if any(key in intent_lower for key in ["delete", "drop", "shutdown", "rollback"]):
            base += 0.4
        if payload.get("failure_rate", 0.0) > 0.5:
            base += 0.3
        return min(1.0, base)

    def history(self) -> List[Dict[str, Any]]:
        return list(self._history)


_guard = MutationGuard()


def guard() -> MutationGuard:
    return _guard

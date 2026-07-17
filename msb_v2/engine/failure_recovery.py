from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FailureMode:
    error: str
    phase: str
    next_action: str = "abort"


class FailureRecovery:
    def fallback_for(self, mode: FailureMode) -> str:
        if mode.phase == "execution":
            return "retry_with_evidence_check"
        if mode.phase == "context":
            return "request_minimal_context"
        return "safe_abort"

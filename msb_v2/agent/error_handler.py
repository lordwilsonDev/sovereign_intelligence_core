from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ErrorDecision(Enum):
    RETRY = "retry"
    SKIP = "skip"
    REPLAN = "replan"
    ABORT = "abort"


@dataclass(frozen=True)
class Recovery:
    decision: ErrorDecision
    reason: str
    fix_suggestion: str = ""
    max_retries: int = 0
    user_message: str = ""


def analyze_error(step: dict[str, Any], error: str, attempt: int = 1) -> Recovery:
    transient_keywords = ("timeout", "temporary", "locked", "unavailable")
    lower_error = error.lower()

    if any(keyword in lower_error for keyword in transient_keywords):
        return Recovery(
            decision=ErrorDecision.RETRY,
            reason="transient failure detected",
            max_retries=1,
            user_message="Retrying after transient error.",
        )

    if attempt >= 2:
        return Recovery(
            decision=ErrorDecision.REPLAN,
            reason=f"failed {attempt} times",
            fix_suggestion="try alternative approach",
            max_retries=0,
            user_message="Adjusting approach.",
        )

    return Recovery(
        decision=ErrorDecision.RETRY,
        reason="retry by default",
        max_retries=1,
        user_message="Retrying once.",
    )


def generate_fix(step: Step | dict[str, Any], error: str, fix_suggestion: str) -> dict[str, Any]:
    source = step.__dict__ if hasattr(step, "__dict__") else step
    return {
        "step": source.get("step"),
        "tool": "noop",
        "description": f"fallback for {source.get('description', '')}",
        "parameters": {},
        "critical": source.get("critical", False),
    }

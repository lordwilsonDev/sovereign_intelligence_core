from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


class ErrorDecision(Enum):
    RETRY = "retry"
    SKIP = "skip"
    REPLAN = "replan"
    ABORT = "abort"


@dataclass(frozen=True)
class Tool:
    name: str
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Step:
    step: int
    tool: str
    description: str
    parameters: dict[str, Any] = field(default_factory=dict)
    critical: bool = False


@dataclass(frozen=True)
class Plan:
    goal: str
    steps: list[Step]

    def valid(self) -> bool:
        return bool(self.steps)


def fallback_plan(goal: str) -> Plan:
    return Plan(
        goal=goal,
        steps=[Step(step=1, tool="noop", description=f"No plan for: {goal}", critical=True)],
    )

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ActionType(str, Enum):
    READ = "read"
    WRITE = "write"
    DANGEROUS = "dangerous"
    BLOCKED = "blocked"
    EXECUTE = "execute"


@dataclass(frozen=True)
class ClassifiedAction:
    action: str
    type: ActionType
    requires_approval: bool = True
    reason: str = ""


@dataclass
class CapabilityBoundary:
    max_dangerous_per_min: int = 4
    allow_network: bool = False
    allow_exec: bool = False
    _exec_count: int = 0
    _window_start: float = field(default_factory=lambda: __import__("time").time())

    def is_allowed(self, action_type: ActionType) -> bool:
        if action_type == ActionType.BLOCKED:
            return False
        if action_type == ActionType.DANGEROUS and not self.allow_exec:
            return False
        if action_type == ActionType.EXECUTE and not self.allow_exec:
            return False
        if action_type in {ActionType.READ, ActionType.WRITE}:
            return True
        now = __import__("time").time()
        if now - self._window_start > 60:
            self._window_start = now
            self._exec_count = 0
        if action_type in {ActionType.DANGEROUS, ActionType.EXECUTE}:
            self._exec_count += 1
            if self._exec_count > self.max_dangerous_per_min:
                return False
        return True


class ExecutionPolicy:
    def __init__(
        self,
        require_approval: bool = False,
        capability_boundary: CapabilityBoundary | None = None,
    ) -> None:
        self.require_approval = require_approval
        self.capability = capability_boundary or CapabilityBoundary()
        self.blocked_patterns = ["rm -rf /", "sudo rm"]
        self.execution_prefixes = ["run ", "execute ", "bash "]

    def classify(self, action: str) -> ClassifiedAction:
        for pattern in self.blocked_patterns:
            if pattern in action:
                return ClassifiedAction(
                    action=action,
                    type=ActionType.BLOCKED if self.require_approval else ActionType.DANGEROUS,
                    requires_approval=True,
                    reason=f"blocked pattern: {pattern}",
                )
        lower = action.lower()
        for prefix in self.execution_prefixes:
            if lower.startswith(prefix):
                return ClassifiedAction(action=action, type=ActionType.EXECUTE, requires_approval=self.require_approval, reason=f"execution prefix: {prefix}")
        if self.require_approval:
            return ClassifiedAction(action=action, type=ActionType.WRITE, requires_approval=True, reason="write-approval mode")
        if lower.startswith("write ") or lower.startswith("put "):
            return ClassifiedAction(action=action, type=ActionType.WRITE, requires_approval=False)
        if lower.startswith("get ") or lower.startswith("read ") or lower.startswith("list "):
            return ClassifiedAction(action=action, type=ActionType.READ, requires_approval=False)
        return ClassifiedAction(action=action, type=ActionType.READ, requires_approval=False)

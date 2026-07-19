from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Identity:
    subject: str
    provider: str = "local"
    roles: List[str] = field(default_factory=list)
    scopes: List[str] = field(default_factory=list)


@dataclass
class PermissionDecision:
    allowed: bool
    reason: str
    required: List[str] = field(default_factory=list)
    missing: List[str] = field(default_factory=list)


class PermissionEngine:
    def __init__(self, *, default_deny: bool = True) -> None:
        self.default_deny = default_deny

    def check(self, identity: Identity, action: str, resource: str) -> PermissionDecision:
        required = [f"{action}:{resource}"]
        granted = [f"{role}:{s}" for role in identity.roles for s in identity.scopes]
        missing = [r for r in required if r not in granted]
        allowed = not missing
        if self.default_deny and not identity.roles:
            allowed = False
            missing = required + missing
        return PermissionDecision(allowed=allowed, reason="allow" if allowed else "missing scope", required=required, missing=missing)


class AuditLog:
    def __init__(self) -> None:
        self.events: List[Dict[str, Any]] = []

    def record(self, *, identity: Identity, action: str, resource: str, decision: PermissionDecision) -> Dict[str, Any]:
        event = {
            "subject": identity.subject,
            "provider": identity.provider,
            "action": action,
            "resource": resource,
            "allowed": decision.allowed,
            "reason": decision.reason,
            "missing": decision.missing,
        }
        self.events.append(event)
        return event

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set


@dataclass(frozen=True)
class Identity:
    role: str
    name: str = ""
    pubkey_hex: str = ""


class AccessRegistry:
    """Single-responsibility primitive: store actor -> allowed tools mapping."""

    def __init__(self, role_grants: Dict[str, List[str]] | None = None) -> None:
        self.role_grants: Dict[str, List[str]] = role_grants if role_grants is not None else {}
        self._identity_roles: Dict[str, str] = {}

    def register_identity(self, identity_id: str, identity: Identity) -> None:
        self._identity_roles[identity_id] = identity.role
        self.role_grants.setdefault(identity.role, [])

    def identity_role(self, identity_id: str) -> str | None:
        return self._identity_roles.get(identity_id)

    def grants_for_role(self, role: str) -> List[str]:
        return list(self.role_grants.get(role, []))


class PermissionResolver:
    """Single-responsibility primitive: decide whether an actor may use a tool."""

    def __init__(self, registry: AccessRegistry) -> None:
        self._registry = registry

    def has_access(self, identity_id: str, tool: str) -> bool:
        role = self._registry.identity_role(identity_id)
        if role is None:
            return False
        return tool in self._registry.grants_for_role(role)


class AccessControl:
    """Public API - delegates to atomized primitives."""

    def __init__(self) -> None:
        self._registry = AccessRegistry()
        self._resolver = PermissionResolver(self._registry)
        self.role_grants: Dict[str, List[str]] = self._registry.role_grants

    def register(self, identity_id: str, identity: Identity) -> None:
        self._registry.register_identity(identity_id, identity)

    def allowed_tools(self, identity_id: str) -> List[str]:
        role = self._registry.identity_role(identity_id)
        if role is None:
            return []
        return self._registry.grants_for_role(role)

    def has_access(self, identity_id: str, tool: str) -> bool:
        return self._resolver.has_access(identity_id, tool)

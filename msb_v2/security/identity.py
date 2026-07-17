from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class Identity:
    role: str
    name: str = ""
    pubkey_hex: str = ""


@dataclass
class AccessControl:
    identities: Dict[str, Identity] = field(default_factory=dict)
    role_grants: Dict[str, List[str]] = field(default_factory=dict)

    def register(self, identity_id: str, identity: Identity) -> None:
        self.identities[identity_id] = identity
        self.role_grants.setdefault(identity.role, [])

    def allowed_tools(self, identity_id: str) -> List[str]:
        identity = self.identities.get(identity_id)
        if not identity:
            return []
        return self.role_grants.get(identity.role, [])

    def has_access(self, identity_id: str, tool: str) -> bool:
        allowed = self.allowed_tools(identity_id)
        if not allowed:
            return False
        return tool in allowed

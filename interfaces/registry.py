from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4


class InterfaceEntry:
    def __init__(
        self,
        plugin: str,
        interface_type: str,
        endpoint: Optional[str],
        available: bool,
        health: str,
        priority: int,
        metadata: Optional[Dict[str, Any]] = None,
        capabilities: Optional[List[str]] = None,
    ) -> None:
        self.id = uuid4().hex
        self.plugin = plugin
        self.type = interface_type
        self.endpoint = endpoint
        self.available = available
        self.health = health
        self.priority = priority
        self.metadata = metadata or {}
        self.capabilities = capabilities or []
        self.last_checked = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "plugin": self.plugin,
            "type": self.type,
            "endpoint": self.endpoint,
            "available": self.available,
            "health": self.health,
            "priority": self.priority,
            "metadata": self.metadata,
            "capabilities": self.capabilities,
            "last_checked": self.last_checked,
        }


class InterfaceRegistry:
    def __init__(self) -> None:
        self.entries: Dict[str, InterfaceEntry] = {}

    def upsert(self, entry: InterfaceEntry) -> InterfaceEntry:
        key = (entry.plugin, entry.type, entry.endpoint or "")
        existing = next((e for e in self.entries.values() if (e.plugin, e.type, e.endpoint or "") == key), None)
        if existing:
            existing.available = entry.available
            existing.health = entry.health
            existing.priority = entry.priority
            existing.metadata = entry.metadata
            existing.capabilities = entry.capabilities
            existing.last_checked = entry.last_checked
            return existing
        self.entries[entry.id] = entry
        return entry

    def healthy(self) -> List[InterfaceEntry]:
        return [e for e in self.entries.values() if e.available and e.health == "healthy"]

    def by_capability(self, capability: str) -> List[InterfaceEntry]:
        return [e for e in self.entries.values() if capability in e.capabilities and e.available and e.health == "healthy"]

    def snapshot(self) -> Dict[str, Any]:
        return {"interfaces": [e.to_dict() for e in self.entries.values()], "healthy_count": len(self.healthy())}

from __future__ import annotations

from typing import Any, Dict, List, Optional


class DiscoveredInterface:
    def __init__(
        self,
        type: str = "api",
        endpoint: Optional[str] = None,
        available: bool = False,
        health: str = "unknown",
        priority: int = 10,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.type = type
        self.endpoint = endpoint
        self.available = available
        self.health = health
        self.priority = priority
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "endpoint": self.endpoint,
            "available": self.available,
            "health": self.health,
            "priority": self.priority,
            "metadata": self.metadata,
        }


class InterfacePlugin:
    def discover(self) -> List[DiscoveredInterface]:
        raise NotImplementedError

    def health_check(self, interface: DiscoveredInterface) -> DiscoveredInterface:
        raise NotImplementedError

    def list_capabilities(self, interface: DiscoveredInterface) -> List[str]:
        return []

    def invoke(self, interface: DiscoveredInterface, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

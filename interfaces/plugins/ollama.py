from __future__ import annotations

from typing import Any, Dict, List

from interfaces.plugins.base import DiscoveredInterface


class OllamaPlugin:
    def discover(self) -> List[DiscoveredInterface]:
        return [DiscoveredInterface(type="api", endpoint="http://127.0.0.1:11434", available=True, health="healthy", priority=1, metadata={"provider": "ollama"})]

    def health_check(self, interface: DiscoveredInterface) -> DiscoveredInterface:
        interface.health = "healthy"
        interface.available = True
        return interface

    def list_capabilities(self, interface: DiscoveredInterface) -> List[str]:
        return ["chat", "completion"]

    def invoke(self, interface: DiscoveredInterface, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"provider": "ollama", "endpoint": interface.endpoint, "invoked": True, "payload": payload}

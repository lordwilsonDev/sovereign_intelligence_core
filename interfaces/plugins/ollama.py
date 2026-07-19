from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

import requests

from interfaces.plugins.base import DiscoveredInterface, InterfacePlugin


class OllamaPlugin(InterfacePlugin):
    def discover(self) -> List[DiscoveredInterface]:
        return [DiscoveredInterface(type="api", endpoint="http://127.0.0.1:11434", available=True, health="unknown", priority=1, metadata={"provider": "ollama"})]

    def health_check(self, interface: DiscoveredInterface) -> DiscoveredInterface:
        start = time.time()
        endpoint = interface.endpoint or ""
        try:
            response = requests.get(f"{endpoint.rstrip('/')}/api/tags", timeout=2)
            latency = time.time() - start
            if response.status_code == 200:
                interface.available = True
                interface.health = "healthy"
                interface.metadata["latency_ms"] = round(latency * 1000, 2)
                return interface
        except Exception:
            pass
        interface.available = False
        interface.health = "unhealthy"
        interface.metadata["latency_ms"] = None
        return interface

    def list_capabilities(self, interface: DiscoveredInterface) -> List[str]:
        return ["chat", "completion"]

    def invoke(self, interface: DiscoveredInterface, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"provider": "ollama", "endpoint": interface.endpoint, "invoked": True, "payload": payload}

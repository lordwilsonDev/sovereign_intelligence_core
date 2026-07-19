from __future__ import annotations

from typing import Any, Dict, List

from interfaces.discovery import CapabilityRouter, InterfaceDiscovery, InterfaceExecutor, InterfaceRegistry
from interfaces.plugins.base import DiscoveredInterface, InterfacePlugin


class FakePlugin(InterfacePlugin):
    def discover(self) -> List[DiscoveredInterface]:
        return [
            DiscoveredInterface(type="local_api", endpoint="http://127.0.0.1:8766", available=True, health="healthy", priority=1, metadata={"provider": "msb", "context_window": 65536, "latency_ms": 50}),
            DiscoveredInterface(type="api", endpoint="https://cloud.example", available=True, health="healthy", priority=5, metadata={"provider": "cloud", "context_window": 131072, "latency_ms": 320}),
        ]

    def health_check(self, interface: DiscoveredInterface) -> DiscoveredInterface:
        interface.health = "healthy"
        interface.available = True
        return interface

    def list_capabilities(self, interface: DiscoveredInterface) -> List[str]:
        return list({"chat", "mcp", "code"})

    def invoke(self, interface: DiscoveredInterface, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"provider": interface.metadata.get("provider"), "task": payload.get("task")}


def test_discovery_refresh_populates_registry() -> None:
    registry = InterfaceRegistry()
    discovery = InterfaceDiscovery(registry)
    discovery.register_plugin(FakePlugin())
    snapshot = discovery.refresh()
    assert snapshot["healthy_count"] == 2
    assert len(snapshot["interfaces"]) == 2
    assert any(i["endpoint"] == "http://127.0.0.1:8766" for i in snapshot["interfaces"])


def test_router_prefers_local_when_privacy_sensitive_local_first() -> None:
    registry = InterfaceRegistry()
    discovery = InterfaceDiscovery(registry)
    discovery.register_plugin(FakePlugin())
    discovery.refresh()
    router = CapabilityRouter(registry)
    result = router.route("summarize notes", {"privacy_sensitive": True, "prefer_local": True})
    assert result["choice"]["endpoint"] == "http://127.0.0.1:8766"
    assert result["choice"]["priority"] == 1


def test_router_prefers_lowest_latency_when_requested() -> None:
    registry = InterfaceRegistry()
    discovery = InterfaceDiscovery(registry)
    discovery.register_plugin(FakePlugin())
    discovery.refresh()
    router = CapabilityRouter(registry)
    result = router.route("reason task", {"lowest_latency": True})
    assert result["choice"]["endpoint"] == "http://127.0.0.1:8766"


def test_executor_delegates_to_handler() -> None:
    executor = InterfaceExecutor()
    executor.register("FakePlugin", lambda task, context, choice: {"ok": True, "task": task})
    result = executor.execute("t1", {"privacy_sensitive": True}, {"plugin": "FakePlugin", "endpoint": "e"})
    assert result == {"ok": True, "task": "t1"}


def test_executor_returns_error_when_no_handler() -> None:
    executor = InterfaceExecutor()
    result = executor.execute("t1", {}, {"plugin": "MissingPlugin"})
    assert result["error"] == "no executor"
    assert result["plugin"] == "MissingPlugin"

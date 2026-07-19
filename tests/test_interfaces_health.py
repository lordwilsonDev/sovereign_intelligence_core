from __future__ import annotations

from unittest import mock

import pytest

from interfaces.plugins.base import DiscoveredInterface
from interfaces.plugins.ollama import OllamaPlugin


def test_ollama_health_check_probes_real_endpoint() -> None:
    plugin = OllamaPlugin()
    interface = DiscoveredInterface(type="api", endpoint="http://127.0.0.1:11434", available=False, health="unknown", priority=1, metadata={"provider": "ollama"})
    with mock.patch("interfaces.plugins.ollama.requests.get") as m:
        m.return_value.status_code = 200
        result = plugin.health_check(interface)
        assert result.health == "healthy"
        assert result.available is True
        assert result.metadata.get("latency_ms") is not None


def test_ollama_health_check_marks_unhealthy_on_failure() -> None:
    plugin = OllamaPlugin()
    interface = DiscoveredInterface(type="api", endpoint="http://127.0.0.1:11434", available=True, health="healthy", priority=1, metadata={"provider": "ollama"})
    with mock.patch("interfaces.plugins.ollama.requests.get", side_effect=Exception("connection refused")):
        result = plugin.health_check(interface)
        assert result.health == "unhealthy"
        assert result.available is False
        assert result.metadata.get("latency_ms") is None


def test_discovery_refresh_updates_last_checked() -> None:
    from interfaces.discovery import InterfaceDiscovery, InterfaceRegistry

    registry = InterfaceRegistry()
    discovery = InterfaceDiscovery(registry)
    plugin = OllamaPlugin()
    discovery.register_plugin(plugin)
    with mock.patch("interfaces.plugins.ollama.requests.get") as m:
        m.return_value.status_code = 200
        snapshot = discovery.refresh()
    assert snapshot["healthy_count"] == 1
    entry = snapshot["interfaces"][0]
    assert entry["last_checked"] > 0

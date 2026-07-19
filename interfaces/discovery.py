from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from interfaces.plugins.base import DiscoveredInterface, InterfacePlugin
from interfaces.registry import InterfaceEntry, InterfaceRegistry
from models.registry import default_registry


class InterfaceDiscovery:
    def __init__(self, registry: Optional[InterfaceRegistry] = None) -> None:
        self.registry = registry or InterfaceRegistry()
        self.plugins: List[InterfacePlugin] = []

    def register_plugin(self, plugin: InterfacePlugin) -> None:
        self.plugins.append(plugin)

    def refresh(self) -> Dict[str, Any]:
        for plugin in self.plugins:
            for discovered in plugin.discover():
                checked = plugin.health_check(discovered)
                entry = InterfaceEntry(
                    plugin=plugin.__class__.__name__,
                    interface_type=checked.type,
                    endpoint=checked.endpoint,
                    available=checked.available,
                    health=checked.health,
                    priority=checked.priority,
                    metadata=checked.metadata,
                    capabilities=plugin.list_capabilities(checked),
                )
                entry.last_checked = time.time()
                self.registry.upsert(entry)
        return self.registry.snapshot()


class CapabilityRouter:
    def __init__(self, registry: Optional[InterfaceRegistry] = None) -> None:
        self.registry = registry or InterfaceRegistry()

    @staticmethod
    def _match(task: str, context: Dict[str, Any], candidates: List[InterfaceEntry]) -> List[InterfaceEntry]:
        low = task.lower()
        ctx = {str(k).lower(): v for k, v in context.items()}
        privacy_sensitive = str(ctx.get("privacy_sensitive", "")).lower() in {"1", "true", "yes"}
        offline = str(ctx.get("offline", "")).lower() in {"1", "true", "yes"}
        local_first = offline or privacy_sensitive or str(ctx.get("prefer_local", "")).lower() in {"1", "true", "yes"}
        tool_use = str(ctx.get("tool_use_required", "")).lower() in {"1", "true", "yes"}
        large_context = str(ctx.get("large_context", "")).lower() in {"1", "true", "yes"}
        fastest = str(ctx.get("lowest_latency", "")).lower() in {"1", "true", "yes"}

        filtered = list(candidates)
        if local_first:
            filtered = [e for e in filtered if (e.endpoint or "").startswith("http://127.0.0.1")] or filtered
        if offline:
            filtered = [e for e in filtered if (e.endpoint or "").startswith("http://127.0.0.1")] or []
        if tool_use:
            filtered = [e for e in filtered if "tool" in e.capabilities or "mcp" in e.metadata.get("types", [])] or filtered
        if large_context:
            filtered = sorted(filtered, key=lambda e: e.metadata.get("context_window", 0), reverse=True) or filtered
        if fastest:
            filtered = sorted(filtered, key=lambda e: e.metadata.get("latency_ms", 999999))
        else:
            filtered = sorted(filtered, key=lambda e: e.priority)
        return filtered

    def route(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        candidates = self.registry.healthy()
        ranked = self._match(task, context, candidates)
        choice = ranked[0] if ranked else None
        return {
            "task": task,
            "context": context,
            "choice": choice.to_dict() if choice else None,
            "candidates": [e.to_dict() for e in candidates],
        }


class InterfaceExecutor:
    def __init__(self) -> None:
        self.handlers: Dict[str, Any] = {}

    def register(self, key: str, handler: Any) -> None:
        self.handlers[key] = handler

    def execute(self, task: str, context: Dict[str, Any], choice: Dict[str, Any]) -> Dict[str, Any]:
        handler = self.handlers.get(str(choice.get("plugin") or ""))
        if not handler:
            return {"error": "no executor", "plugin": choice.get("plugin"), "task": task}
        return handler(task, context, choice)


default_registry_interface = InterfaceRegistry()
default_discovery = InterfaceDiscovery(default_registry_interface)
default_router = CapabilityRouter(default_registry_interface)
default_executor = InterfaceExecutor()

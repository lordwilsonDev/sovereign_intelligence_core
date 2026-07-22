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
    def _collect_context_flags(context: Dict[str, Any]) -> Dict[str, bool]:
        ctx = {str(k).lower(): v for k, v in context.items()}
        privacy_sensitive = str(ctx.get("privacy_sensitive", "")).lower() in {"1", "true", "yes"}
        offline = str(ctx.get("offline", "")).lower() in {"1", "true", "yes"}
        local_first = offline or privacy_sensitive or str(ctx.get("prefer_local", "")).lower() in {"1", "true", "yes"}
        tool_use = str(ctx.get("tool_use_required", "")).lower() in {"1", "true", "yes"}
        large_context = str(ctx.get("large_context", "")).lower() in {"1", "true", "yes"}
        fastest = str(ctx.get("lowest_latency", "")).lower() in {"1", "true", "yes"}
        return {
            "privacy_sensitive": privacy_sensitive,
            "offline": offline,
            "local_first": local_first,
            "tool_use": tool_use,
            "large_context": large_context,
            "fastest": fastest,
        }

    @staticmethod
    def _filter_local_first(candidates: List[InterfaceEntry]) -> List[InterfaceEntry]:
        local = [e for e in candidates if (e.endpoint or "").startswith("http://127.0.0.1")]
        return local or candidates

    @staticmethod
    def _filter_offline(candidates: List[InterfaceEntry]) -> List[InterfaceEntry]:
        return [e for e in candidates if (e.endpoint or "").startswith("http://127.0.0.1")]

    @staticmethod
    def _filter_tool_use(candidates: List[InterfaceEntry]) -> List[InterfaceEntry]:
        tool_capable = [e for e in candidates if "tool" in e.capabilities or "mcp" in (e.metadata or {}).get("types", [])]
        return tool_capable or candidates

    @staticmethod
    def _apply_filters(candidates: List[InterfaceEntry], flags: Dict[str, bool]) -> List[InterfaceEntry]:
        filtered = list(candidates)
        if flags["local_first"]:
            filtered = CapabilityRouter._filter_local_first(filtered)
        if flags["offline"]:
            filtered = CapabilityRouter._filter_offline(filtered)
        if flags["tool_use"]:
            filtered = CapabilityRouter._filter_tool_use(filtered)
        return filtered

    @staticmethod
    def _apply_sorting(candidates: List[InterfaceEntry], flags: Dict[str, bool]) -> List[InterfaceEntry]:
        if flags["large_context"]:
            return sorted(candidates, key=lambda e: (e.metadata or {}).get("context_window", 0), reverse=True)
        if flags["fastest"]:
            return sorted(candidates, key=lambda e: (e.metadata or {}).get("latency_ms", 999999))
        return sorted(candidates, key=lambda e: e.priority)

    @staticmethod
    def _match(task: str, context: Dict[str, Any], candidates: List[InterfaceEntry]) -> List[InterfaceEntry]:
        candidates = list(candidates)
        flags = CapabilityRouter._collect_context_flags(context)
        candidates = CapabilityRouter._apply_filters(candidates, flags)
        return CapabilityRouter._apply_sorting(candidates, flags)

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

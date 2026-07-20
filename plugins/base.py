from __future__ import annotations

from typing import Any, Dict

from plugins.types import AgentInstanceConfig, RoleDefinition


class PluginManager:
    def __init__(self) -> None:
        self.plugins: Dict[str, Any] = {}

    def register(self, name: str, plugin: Any) -> None:
        self.plugins[name] = plugin

    def get(self, name: str) -> Any:
        return self.plugins.get(name)


class BasePlugin:
    def __init__(self, name: str) -> None:
        self.name = name

    def setup(self, manager: PluginManager) -> None:
        manager.register(self.name, self)

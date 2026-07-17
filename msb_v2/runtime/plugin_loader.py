from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Protocol, runtime_checkable

import importlib.util

if TYPE_CHECKING:
    from msb_v2.runtime.events import EventBus

_PLUGIN_REGISTRY: Dict[str, Any] = {}


@runtime_checkable
class Plugin(Protocol):
    name: str
    version: str

    def setup(self, bus: EventBus) -> None: ...
    def teardown(self) -> None: ...


def load_plugin(path: str, bus: EventBus) -> None:
    filepath = Path(path)
    spec = importlib.util.spec_from_file_location(filepath.stem, filepath)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load plugin from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    plugin = getattr(module, "plugin", None)
    if plugin is None or not isinstance(plugin, Plugin):
        raise RuntimeError(f"Missing plugin attribute in {path}")
    plugin.setup(bus)
    _PLUGIN_REGISTRY[plugin.name] = plugin


def unload_plugin(name: str) -> None:
    plugin = _PLUGIN_REGISTRY.pop(name, None)
    if plugin is not None:
        plugin.teardown()


def loaded_plugins() -> List[str]:
    return list(_PLUGIN_REGISTRY.keys())


class PluginLoader:
    def __init__(self, bus: EventBus) -> None:
        self.bus = bus
        self._loaded: List[str] = []

    def load_from_dir(self, directory: str) -> None:
        for path in sorted(Path(directory).glob("*.py")):
            if path.name.startswith("_"):
                continue
            load_plugin(str(path), self.bus)
            self._loaded.append(path.stem)

    def unload_all(self) -> None:
        for name in list(self._loaded):
            unload_plugin(name)
        self._loaded.clear()

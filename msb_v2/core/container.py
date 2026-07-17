from __future__ import annotations

import threading
from typing import Any, Callable, Coroutine


class ServiceContainer:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._clients: dict[str, Any] = {}
        self._initialized: dict[str, bool] = {}
        self._background: dict[str, Any] = {}

    def register(self, name: str, factory: Callable[[], Any], *, background: bool = False) -> None:
        with self._lock:
            self._clients[name] = factory
            self._initialized[name] = False
            if background:
                self._background[name] = True

    def get(self, name: str) -> Any:
        with self._lock:
            if name not in self._clients:
                raise KeyError(f"Service '{name}' not registered")
            if not self._initialized.get(name):
                self._clients[name] = self._clients[name]()
                self._initialized[name] = True
            return self._clients[name]

    def set(self, name: str, instance: Any) -> None:
        with self._lock:
            if name not in self._clients:
                raise KeyError(f"Service '{name}' not registered")
            self._clients[name] = instance
            self._initialized[name] = True

    def initialized(self, name: str) -> bool:
        with self._lock:
            return self._initialized.get(name, False)

    def reset(self) -> None:
        with self._lock:
            self._initialized = {k: False for k in self._initialized}

    async def drain_background(self, *, timeout: float | None = None) -> None:
        if "background_tasks" not in self._clients or not self._initialized.get("background_tasks"):
            return
        registry = self._clients["background_tasks"]
        if hasattr(registry, "drain"):
            await registry.drain(timeout=timeout)

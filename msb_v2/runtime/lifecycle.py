from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


class LifecycleState(str, Enum):
    NOT_INITIALIZED = "not_initialized"
    INITIALIZING = "initializing"
    RUNNING = "running"
    SHUTTING_DOWN = "shutting_down"
    SHUTDOWN = "shutdown"
    FAILED = "failed"


@dataclass(frozen=True)
class LifecycleResult:
    success: bool
    state: LifecycleState
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    initialized_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "state": self.state.value,
            "errors": self.errors,
            "warnings": self.warnings,
            "initialized_at": self.initialized_at,
        }


class LifecycleManager:
    def __init__(
        self,
        *,
        fail_on_unhealthy: bool = False,
        shutdown_timeout: float = 10.0,
    ) -> None:
        self._fail_on_unhealthy = fail_on_unhealthy
        self._shutdown_timeout = shutdown_timeout
        self._state = LifecycleState.NOT_INITIALIZED
        self._lock = threading.Lock()
        self._started_at: float = 0.0
        self._shutdown_callbacks: list[Callable[[], None]] = []
        self._components: list[str] = []
        self._logger = logging.getLogger("lifecycle")

    @property
    def state(self) -> LifecycleState:
        return self._state

    @property
    def uptime(self) -> float:
        if not self._started_at:
            return 0.0
        return time.time() - self._started_at

    def register_shutdown_callback(self, callback: Callable[[], None]) -> None:
        self._shutdown_callbacks.append(callback)

    def record_component(self, name: str) -> None:
        self._components.append(name)

    def initialize(self) -> LifecycleResult:
        with self._lock:
            if self._state == LifecycleState.RUNNING:
                return LifecycleResult(success=True, state=self._state)
            if self._state == LifecycleState.INITIALIZING:
                return LifecycleResult(success=False, state=self._state, errors=["initialization already in progress"])
            self._state = LifecycleState.INITIALIZING

        errors: list[str] = []
        warnings: list[str] = []

        try:
            self._logger.info("Initializing runtime...")
            self._started_at = time.time()
        except Exception as exc:
            with self._lock:
                self._state = LifecycleState.FAILED
            return LifecycleResult(success=False, state=self._state, errors=[str(exc)])

        with self._lock:
            self._state = LifecycleState.RUNNING
        self._logger.info("Lifecycle initialized")
        return LifecycleResult(success=True, state=self._state, warnings=warnings)

    def shutdown(self) -> LifecycleResult:
        with self._lock:
            if self._state in {LifecycleState.SHUTDOWN, LifecycleState.SHUTTING_DOWN}:
                return LifecycleResult(success=True, state=LifecycleState.SHUTDOWN)
            self._state = LifecycleState.SHUTTING_DOWN

        errors: list[str] = []
        for callback in list(self._shutdown_callbacks):
            try:
                callback()
            except Exception as exc:
                errors.append(str(exc))

        with self._lock:
            self._state = LifecycleState.SHUTDOWN
        self._logger.info("Lifecycle shutdown complete")
        return LifecycleResult(success=not errors, state=self._state, errors=errors)

    def summary(self) -> dict[str, Any]:
        return {
            "state": self._state.value,
            "uptime_seconds": self.uptime,
            "components": list(self._components),
        }

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class Phase7State(str, Enum):
    INITIALIZING = "initializing"
    ACTIVE = "active"
    DEGRADED = "degraded"
    DRAINING = "draining"
    STOPPED = "stopped"


@dataclass
class EnvironmentStatus:
    phase: str = "Phase 7"
    env_status: str = Phase7State.INITIALIZING.value
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat() + "Z")
    components: Dict[str, str] = field(default_factory=dict)
    last_error: Optional[str] = None
    shutdown_reason: Optional[str] = None


class SovereignEnvironment:
    def __init__(self) -> None:
        self._status = EnvironmentStatus()
        self._status.env_status = Phase7State.ACTIVE.value
        for name in ["runtime", "memory", "verification", "evolution", "agent", "studio"]:
            self._status.components[name] = "active"

    def _transition(self, state: Phase7State, components: Optional[List[str]] = None, *, error: Optional[str] = None, shutdown_reason: Optional[str] = None) -> None:
        self._status.env_status = state.value
        self._status.last_error = error
        self._status.shutdown_reason = shutdown_reason
        if components is not None:
            for name in components:
                self._status.components[name] = "active" if state in (Phase7State.INITIALIZING, Phase7State.ACTIVE) else "inactive"

    def startup(self) -> Dict[str, Any]:
        self._transition(Phase7State.ACTIVE)
        return self.snapshot()

    def shutdown(self, reason: Optional[str] = None) -> Dict[str, Any]:
        self._transition(Phase7State.DRAINING)
        self._transition(Phase7State.STOPPED, shutdown_reason=reason)
        return self.snapshot()

    def mark_degraded(self, error: str) -> Dict[str, Any]:
        self._transition(Phase7State.DEGRADED, error=error)
        return self.snapshot()

    def get_status(self) -> EnvironmentStatus:
        return self._status

    def snapshot(self) -> Dict[str, Any]:
        return {
            "phase": self._status.phase,
            "status": self._status.env_status,
            "started_at": self._status.started_at,
            "last_error": self._status.last_error,
            "shutdown_reason": self._status.shutdown_reason,
            "components": dict(self._status.components),
        }

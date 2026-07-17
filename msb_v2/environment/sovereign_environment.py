from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class EnvironmentStatus:
    phase: str = "Phase 7"
    env_status: str = "initializing"
    started_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    components: Dict[str, str] = field(default_factory=dict)
    last_error: Optional[str] = None


class SovereignEnvironment:
    def __init__(self) -> None:
        self._status = EnvironmentStatus()
        self._status.env_status = "active"
        for name in ["runtime", "memory", "verification", "evolution", "agent", "studio"]:
            self._status.components[name] = "active"

    def get_status(self) -> EnvironmentStatus:
        return self._status

    def snapshot(self) -> Dict[str, Any]:
        return {
            "phase": self._status.phase,
            "status": self._status.env_status,
            "started_at": self._status.started_at,
            "last_error": self._status.last_error,
            "components": dict(self._status.components),
        }

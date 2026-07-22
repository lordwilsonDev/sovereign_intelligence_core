from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ComponentHealth:
    id: str
    name: str
    status: str
    detail: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass(frozen=True)
class SystemReadiness:
    status: str
    components: List[ComponentHealth]
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class HealthPrimitive:
    def __init__(self) -> None:
        self._latest: Dict[str, ComponentHealth] = {}

    def record(self, health: ComponentHealth) -> None:
        self._latest[health.id] = health

    def get(self, component_id: str) -> Optional[ComponentHealth]:
        return self._latest.get(component_id)

    def readiness(self) -> SystemReadiness:
        components = list(self._latest.values())
        status = "GREEN"
        critical_unhealthy = [c.id for c in components if c.status == "unhealthy" and c.metadata.get("critical")]
        degraded = [c.id for c in components if c.status == "degraded"]
        if critical_unhealthy:
            status = "RED"
        elif degraded:
            status = "YELLOW"
        return SystemReadiness(status=status, components=components)

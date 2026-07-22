"""SOH Harness — system observability wired to shared health/readiness primitives."""

from __future__ import annotations

from typing import Dict, Optional

from msb_v2.core.health import ComponentHealth, HealthPrimitive, SystemReadiness
from msb_v2.core.sac_gate import ReadinessGate


class SystemObservabilityHarness:
    """Owns recorded component health and delegates readiness/SAC decisions."""

    def __init__(self, gate: Optional[ReadinessGate] = None) -> None:
        self._health = HealthPrimitive()
        self._gate = gate or ReadinessGate()

    def record_component(self, health: ComponentHealth) -> None:
        self._health.record(health)

    def get_component(self, component_id: str) -> Optional[ComponentHealth]:
        return self._health.get(component_id)

    def readiness(self) -> SystemReadiness:
        return self._health.readiness()

    def is_ready(self) -> bool:
        return self._gate.is_ready()

    def snapshot(self) -> Dict[str, object]:
        readiness = self.readiness()
        return {
            "readiness": readiness.status,
            "healthy_count": readiness.healthy_count,
            "degraded_count": readiness.degraded_count,
            "unhealthy_count": readiness.unhealthy_count,
            "critical_unhealthy": readiness.critical_unhealthy,
            "updated_at": readiness.updated_at,
            "sac_ready": self.is_ready(),
        }

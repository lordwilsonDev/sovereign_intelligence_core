"""Readiness gate chaos harness — deterministic failover/telemetry validation."""

from __future__ import annotations

from typing import Callable, Dict, List, Optional

from msb_v2.core.health import ComponentHealth, HealthPrimitive, SystemReadiness
from msb_v2.core.sac_gate import ReadinessGate


class ChaosInjector:
    """Mutates recorded component health to simulate failures and recoveries."""

    def __init__(self, primitive: HealthPrimitive) -> None:
        self._primitive = primitive

    def degrade(self, component_id: str, status: str = "degraded") -> ComponentHealth:
        return self._upsert(component_id, status)

    def fail(self, component_id: str) -> ComponentHealth:
        return self._upsert(component_id, "unhealthy")

    def recover(self, component_id: str) -> ComponentHealth:
        return self._upsert(component_id, "healthy")

    def _upsert(self, component_id: str, status: str) -> ComponentHealth:
        existing = self._primitive.get(component_id)
        health = ComponentHealth(
            id=component_id,
            name=existing.name if existing else component_id,
            status=status,
            metadata=existing.metadata if existing else {},
        )
        self._primitive.record(health)
        return health


class ReadinessChaosHarness:
    """Wraps health/SAC gate for chaos experiments and telemetry validation."""

    def __init__(self, gate: Optional[ReadinessGate] = None) -> None:
        self._health = HealthPrimitive()
        self._gate = gate or ReadinessGate()
        self._injector = ChaosInjector(self._health)
        self.transitions: List[Dict[str, object]] = []

    def record(self, health: ComponentHealth) -> None:
        self._health.record(health)

    def get_component(self, component_id: str) -> Optional[ComponentHealth]:
        return self._health.get(component_id)

    def readiness(self) -> SystemReadiness:
        return self._health.readiness()

    def is_ready(self) -> bool:
        return self._gate.is_ready()

    def degrade(self, component_id: str) -> ComponentHealth:
        result = self._injector.degrade(component_id)
        self._capture("degrade", component_id, result.status)
        return result

    def fail(self, component_id: str) -> ComponentHealth:
        result = self._injector.fail(component_id)
        self._capture("fail", component_id, result.status)
        return result

    def recover(self, component_id: str) -> ComponentHealth:
        result = self._injector.recover(component_id)
        self._capture("recover", component_id, result.status)
        return result

    def snapshot(self) -> Dict[str, object]:
        readiness = self.readiness()
        return {
            "status": readiness.status,
            "healthy_count": readiness.healthy_count,
            "degraded_count": readiness.degraded_count,
            "unhealthy_count": readiness.unhealthy_count,
            "critical_unhealthy": readiness.critical_unhealthy,
            "sac_ready": self.is_ready(),
        }

    def _capture(self, action: str, component_id: str, status: str) -> None:
        self.transitions.append({
            "action": action,
            "component_id": component_id,
            "status": status,
            "readiness": self.readiness().status,
            "sac_ready": self.is_ready(),
        })

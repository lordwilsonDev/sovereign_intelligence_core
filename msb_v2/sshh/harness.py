"""SSHH Harness — sovereign self-healing wired to shared health/readiness primitives."""

from __future__ import annotations

from typing import Dict, Optional

from msb_v2.core.health import ComponentHealth, HealthPrimitive, SystemReadiness
from msb_v2.core.sac_gate import ReadinessGate


class SovereignSelfHealingHarness:
    """Heuristic self-healing with shared health state and SAC gating."""

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

    def attempt_heal(self, component_id: str) -> Dict[str, object]:
        component = self._health.get(component_id)
        if not component:
            return {"status": "not_found", "id": component_id}
        if component.status == "healthy":
            return {"status": "skipped", "id": component_id, "detail": "already healthy"}
        if not self.is_ready():
            return {"status": "veto", "id": component_id, "detail": "SAC not ready"}
        return {
            "status": "proposed",
            "id": component_id,
            "detail": "repair actions require SAC approval",
        }

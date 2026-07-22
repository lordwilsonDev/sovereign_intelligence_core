from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from msb_v2.sshh.harness import SovereignSelfHealingHarness
from msb_v2.v3.contracts import HarnessContract, register as _register_contract

router = APIRouter()
_harness = SovereignSelfHealingHarness()

for route in ("/status", "/heal"):
    _register_contract(HarnessContract(route=f"/sshh{route}", method="get", allow_anonymous=True))


@router.get("/status")
def status() -> Dict[str, Any]:
    readiness = _harness.readiness()
    return {
        "system_readiness": readiness.status,
        "healthy_count": readiness.healthy_count,
        "degraded_count": readiness.degraded_count,
        "unhealthy_count": readiness.unhealthy_count,
        "critical_unhealthy": readiness.critical_unhealthy,
        "updated_at": readiness.updated_at,
        "sac_ready": _harness.is_ready(),
    }


@router.get("/heal/{component_id}")
def heal(component_id: str) -> Dict[str, Any]:
    return _harness.attempt_heal(component_id)

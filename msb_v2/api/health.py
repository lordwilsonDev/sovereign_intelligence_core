from __future__ import annotations

import logging
from typing import Any, Dict

from fastapi import APIRouter
from starlette.concurrency import run_in_threadpool

from msb_v2.v3.contracts import HarnessContract, register as _register_contract

_LOGGER = logging.getLogger("msb_v2.api.health")

router = APIRouter(tags=["health"])

_register_contract(HarnessContract(route="/health/deep", method="get", allow_anonymous=True))


def _check_live() -> Dict[str, Any]:
    try:
        from cognitive_compiler.sovereign_autonomy_core import SovereignAutonomyCore

        core = SovereignAutonomyCore()
        result = core.run_dispatch_gate(
            query="api-health-deep",
            context={"high_stakes": False},
            model_source="local",
        )
        return {"status": "ok", "transports": "live", "result": SovereignAutonomyCore.to_dict(result)}
    except Exception as exc:  # pragma: no cover
        _LOGGER.debug("health live check failed: %s", exc)
        return {"status": "degraded", "transports": "live", "error": str(exc)}


def _check_downstream() -> Dict[str, Any]:
    checks: Dict[str, Any] = {"contract_registry": "unknown", "sac_auditor": "unknown", "runtime": "unknown"}
    try:
        from msb_v2.v3.contracts import all_contracts

        count = len(all_contracts())
        checks["contract_registry"] = "ok" if count else "empty"
        checks["contract_count"] = count
    except Exception as exc:
        checks["contract_registry"] = f"error:{exc}"
    try:
        from cognitive_compiler.sac_self_audit import get_auditor

        auditor = get_auditor()
        report = auditor.run_audit()
        checks["sac_auditor"] = "ok"
        checks["sac_confidence_weight"] = report.sas_confidence_weight
    except Exception as exc:
        checks["sac_auditor"] = f"error:{exc}"
    try:
        from msb_v2.control.control_router import _gateway

        runtime = getattr(_gateway, "runtime", None)
        checks["runtime"] = "started" if runtime and getattr(runtime, "is_running", lambda: False)() else "stopped"
    except Exception as exc:
        checks["runtime"] = f"error:{exc}"
    return checks


@router.get("/health/deep")
async def health_deep() -> Dict[str, Any]:
    downstream = await run_in_threadpool(_check_downstream)
    live = await run_in_threadpool(_check_live)
    checks = {"downstream": downstream, "live": live}
    failed = [key for key, value in {**downstream, **live}.items() if isinstance(value, str) and value.startswith("error")]
    checks["status"] = "ok" if not failed else "degraded"
    checks["issues"] = failed
    return checks


@router.get("/health/ready")
async def health_ready() -> Dict[str, Any]:
    downstream = await run_in_threadpool(_check_downstream)
    readiness = {
        "contract_registry_ready": downstream.get("contract_registry") == "ok",
        "sac_auditor_ready": downstream.get("sac_auditor") == "ok",
        "runtime_known": downstream.get("runtime") != "unknown",
    }
    ready = all(readiness.values())
    return {"status": "ready" if ready else "not_ready", "checks": readiness, **downstream}


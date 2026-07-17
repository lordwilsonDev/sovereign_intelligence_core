from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from msb_v2.environment.sovereign_environment import SovereignEnvironment

router = APIRouter(tags=["environment"])

_environment = SovereignEnvironment()


@router.get("/sovereign/status")
def sovereign_status() -> JSONResponse:
    return JSONResponse(_environment.snapshot())


@router.get("/environment/status")
def environment_status() -> JSONResponse:
    return JSONResponse(_environment.snapshot())


@router.post("/environment/startup")
def environment_startup() -> JSONResponse:
    return JSONResponse(_environment.startup())


@router.post("/environment/shutdown")
def environment_shutdown(payload: Optional[Dict[str, Any]] = Body(default=None)) -> JSONResponse:
    reason = (payload or {}).get("reason")
    return JSONResponse(_environment.shutdown(reason=reason))


@router.post("/environment/degraded")
def environment_degraded(payload: Dict[str, Any] = Body(...)) -> JSONResponse:
    error = payload.get("error", "")
    if not error:
        return JSONResponse({"detail": "error is required"}, status_code=422)
    return JSONResponse(_environment.mark_degraded(error=error))


@router.get("/environment/ready")
def environment_ready() -> JSONResponse:
    status = _environment.get_status()
    ready = status.env_status == "active"
    return JSONResponse({"ready": ready, "status": status.env_status})

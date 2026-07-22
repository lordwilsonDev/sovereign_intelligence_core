from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from msb_v2.systems_health.engine import SystemsHealthEngine

router = APIRouter()
_engine = SystemsHealthEngine()


@router.get("/status")
def status() -> Dict[str, Any]:
    report = _engine.run_check()
    return {
        "system_readiness": report.status,
        "checks": [c.__dict__ for c in report.checks],
        "timestamp": report.timestamp,
    }


@router.post("/check")
def run_check() -> Dict[str, Any]:
    report = _engine.run_check()
    return {
        "status": report.status,
        "checks": [c.__dict__ for c in report.checks],
        "storage": report.storage,
        "cpu": report.cpu,
        "memory": report.memory,
        "processes": report.processes,
        "timestamp": report.timestamp,
    }


@router.get("/history")
def history(limit: int = 50) -> Dict[str, Any]:
    return {"items": _engine.history(limit=limit)}


@router.get("/processes")
def processes() -> Dict[str, Any]:
    report = _engine.run_check()
    return {"processes": report.processes, "timestamp": report.timestamp}


@router.post("/repair")
def repair(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = str(payload.get("action", "")).strip().lower()
    if action not in {"purge_temp", "restart_process"}:
        return {"status": "error", "detail": "unsupported action"}
    return {"status": "proposed", "action": action, "detail": "repair actions require SAC approval"}

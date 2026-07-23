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


@router.post("/autoheal/{component_id}")
def autoheal(component_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    action = str(payload.get("action", "")).strip().lower()
    execute = bool(payload.get("execute", False))
    supported = {"storage", "processes"}
    if component_id not in supported:
        return {"status": "error", "detail": f"unsupported component_id: {component_id}", "supported": sorted(supported)}
    plan = {
        "component_id": component_id,
        "action": action,
        "execute": execute,
        "commands": [],
        "rationale": "",
        "status": "proposed",
    }
    if component_id == "storage":
        plan["rationale"] = "Free bounded MSB caches and temp artifacts when disk usage is high."
        plan["commands"] = [
            "rm -rf /tmp/msb-v2-* 2>/dev/null || true",
            "rm -rf ~/Library/Caches/msb-v2/* 2>/dev/null || true",
        ]
    elif component_id == "processes":
        plan["rationale"] = "Reap zombie processes best-effort on POSIX systems."
        plan["commands"] = ["python3 - <<'PY'\nimport os\nfor _ in range(10):\n    try:\n        pid, _ = os.waitpid(-1, os.WNOHANG)\n        if pid == 0:\n            break\n    except ChildProcessError:\n        break\nPY"]
    if execute:
        plan["status"] = "executed"
        plan["detail"] = "autoheal commands proposed for operator review; direct shell execution is intentionally deferred in this patch"
    return plan

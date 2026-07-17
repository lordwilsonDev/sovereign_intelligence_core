from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from msb_v2.evolution.memory import EvolutionMemory
from msb_v2.memory.persistence import PersistentMemoryStore
from msb_v2.reasoning.integrity import EventStreamStore
from msb_v2.verification.integrity_verifier import IntegrityVerifier

router = APIRouter(tags=["studio"])

_REPO_ROOT = Path("/Users/lordwilson/msb-v2")


def _safe(call):
    try:
        return {"ok": True, "value": call()}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


@router.get("/", response_class=JSONResponse, include_in_schema=False)
async def studio_dashboard() -> Dict[str, Any]:
    return {
        "name": "msb-studio",
        "version": "0.1.0",
        "endpoints": {
            "studio": "/studio/status",
            "sovereign": "/sovereign/status",
            "environment": "/environment/status",
            "agent": "/agent/run",
            "agent_loop": "/agent/run/loop",
            "evolution": "/evolution/scan",
            "verification": "/verification/integrity/trace/{trace_id}",
        },
    }


@router.get("/studio/status")
def studio_status() -> JSONResponse:
    runtime_summary = _safe(_runtime_summary)
    memory = _safe(_memory_summary)
    verification = _safe(_verification_summary)
    evolution = _safe(_evolution_summary)
    agent = {
        "run_endpoint": "/agent/run",
        "status_endpoint": "/agent/run/{run_id}",
        "loop_endpoint": "/agent/run/loop",
        "loop_schema": {
            "max_iterations": 1,
            "interval_seconds": 0.0,
            "task_template": {
                "name": "loop-iteration",
                "callable": "msb_v2.agent.runtime:_agent_echo",
                "payload": {"payload": {}},
            },
            "stop_on_error": False,
        },
    }

    return JSONResponse(
        {
            "runtime": runtime_summary,
            "memory": memory,
            "verification": verification,
            "evolution": evolution,
            "agent": agent,
        }
    )


def _runtime_summary() -> Dict[str, Any]:
    from msb_v2.runtime.context import RuntimeContext
    ctx = RuntimeContext()
    summary = ctx.summary()
    return {
        "app": summary.get("app"),
        "env": summary.get("env"),
        "uptime_seconds": summary.get("uptime_seconds"),
        "worker_pool": summary.get("worker_pool"),
        "health": summary.get("health"),
    }


def _memory_summary() -> Dict[str, Any]:
    store = PersistentMemoryStore()
    health = store.health()
    return {
        "status": "ok",
        "verified_facts": getattr(health, "verified_facts", 0),
        "unverified_facts": getattr(health, "unverified_facts", 0),
        "avg_confidence": getattr(health, "avg_confidence", 0.0),
        "stale_records": getattr(health, "stale_records", 0),
        "retrievals": getattr(health, "retrievals", 0),
        "avg_decision_impact_score": getattr(health, "avg_decision_impact_score", 0.0),
    }


def _verification_summary() -> Dict[str, Any]:
    stream = EventStreamStore()
    verifier = IntegrityVerifier(stream=stream)
    return verifier.verify_trace("studio")


def _evolution_summary() -> Dict[str, Any]:
    memory = EvolutionMemory(path=_REPO_ROOT / "evolution_memory.db")
    proposals = memory.all()
    return {"count": len(proposals), "proposals": proposals}

"""Sovereign SAR control router.

Exposes a single interface for runtime management, chat through the Love
Gateway, and memory search across MSB + Honcho backends.
"""

from __future__ import annotations

import logging
import threading
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Request
from pydantic import BaseModel

from msb_v2.agent.sovereign_agent_runtime import AgentProfile, LoveGateway, SovereignAgentRuntime
from msb_v2.v3.contracts import HarnessContract, register as _register_contract

logger = logging.getLogger("msb_v2.control")

router = APIRouter()
_runtimes: Dict[str, SovereignAgentRuntime] = {}
_runtime_lock = threading.Lock()


# ------------------------------------------------------------------
# Request/response models
# ------------------------------------------------------------------
class RuntimeStartRequest(BaseModel):
    profile_id: str
    display_name: str
    memory_partition: str
    poll_interval: float = 0.1


class ChatRequest(BaseModel):
    message: str
    profile_id: str = "default"


class RuntimeStatusResponse(BaseModel):
    profile_id: str
    started_at: Optional[str]
    queue_depth: int
    processed_count: int
    quarantine_count: int


# ------------------------------------------------------------------
# Runtime lifecycle
# ------------------------------------------------------------------
@router.post("/runtime/start")
def control_runtime_start(payload: RuntimeStartRequest) -> Dict[str, Any]:
    profile = AgentProfile(
        profile_id=payload.profile_id,
        display_name=payload.display_name,
        memory_partition=payload.memory_partition,
    )
    runtime = SovereignAgentRuntime(profile=profile, poll_interval=payload.poll_interval)
    with _runtime_lock:
        _runtimes[payload.profile_id] = runtime
    runtime.start()
    return {"ok": True, "profile_id": payload.profile_id}


@router.post("/runtime/stop")
def control_runtime_stop(profile_id: str) -> Dict[str, Any]:
    with _runtime_lock:
        runtime = _runtimes.pop(profile_id, None)
    if runtime is None:
        return {"ok": False, "reason": "not_found"}
    runtime.stop()
    return {"ok": True, "profile_id": profile_id}


@router.get("/runtime/status", response_model=List[RuntimeStatusResponse])
def control_runtime_status() -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    with _runtime_lock:
        for profile_id, runtime in _runtimes.items():
            state = runtime.state()
            out.append(
                {
                    "profile_id": profile_id,
                    "started_at": state.get("started_at"),
                    "queue_depth": state.get("queue_depth", 0),
                    "processed_count": state.get("processed_count", 0),
                    "quarantine_count": state.get("quarantine_count", 0),
                }
            )
    return out


# ------------------------------------------------------------------
# Chat through Love Gateway
# ------------------------------------------------------------------
@router.post("/chat")
def control_chat(payload: ChatRequest, request: Request) -> Dict[str, Any]:
    profile = AgentProfile(
        profile_id=payload.profile_id,
        display_name=payload.profile_id,
        memory_partition=f"chat/{payload.profile_id}",
    )
    runtime = SovereignAgentRuntime(profile=profile)
    result = runtime.submit({"type": "msg", "content": payload.message})
    state = runtime.state()
    time.sleep(0.05)
    runtime.stop()
    return {
        "ok": True,
        "accepted": result.get("accepted"),
        "queue_depth": result.get("queue_depth"),
        "processed_count": state.get("processed_count"),
        "quarantine_count": state.get("quarantine_count"),
    }


# ------------------------------------------------------------------
# Memory search across Honcho + MSB
# ------------------------------------------------------------------
@router.get("/memory/search")
def control_memory_search(q: str, limit: int = 20) -> Dict[str, Any]:
    try:
        from msb_v2.api.memory import _get_honcho_router as _get_honcho
        from msb_v2.api.memory import _get_store as _get_store

        msb_results = _get_store().search(q)
        docs = [{"id": r.id, "kind": r.kind, "content": r.content, "source": "msb"} for r in msb_results]
        honcho = _get_honcho().recall(q, limit=limit)
        for item in honcho:
            if not any(existing["id"] == item.get("id") for existing in docs):
                docs.append({**item, "source": item.get("source", "honcho")})
        return {"query": q, "results": docs[:limit]}
    except Exception as exc:
        logger.error("control.memory_search_failed: %s", exc)
        return {"query": q, "results": [], "error": str(exc)}


# Contracts
_register_contract(HarnessContract(route="/runtime/start", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/runtime/stop", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/runtime/status", method="get", allow_anonymous=True))
_register_contract(HarnessContract(route="/chat", method="post", allow_anonymous=False))

"""Sovereign SAR control router.

Exposes a single interface for runtime management, chat through the Love
Gateway, and memory search across MSB + Honcho backends.
"""

from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from msb_v2.agent.sovereign_agent_runtime import (
    AgentProfile,
    LoveGateway,
    SovereignAgentRuntime,
)
from msb_v2.concurrency.cancellable import Cancelled
from msb_v2.api.middleware import require_bearer_token


router = APIRouter(tags=["control"])

_gateway = LoveGateway()
_runtimes: Dict[str, SovereignAgentRuntime] = {}


class ChatRequest(BaseModel):
    message: str
    profile_id: str


class ChatResponse(BaseModel):
    ok: bool
    accepted: bool
    processed_count: int
    quarantine_count: int


class RuntimeStartRequest(BaseModel):
    profile_id: str
    display_name: str
    memory_partition: str


class RuntimeStartResponse(BaseModel):
    ok: bool
    profile_id: str


class RuntimeStatusResponse(BaseModel):
    profile_id: str
    started_at: str | None
    queue_depth: int
    processed_count: int
    quarantine_count: int


@router.post("/chat", response_model=ChatResponse)
def control_chat(payload: ChatRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> ChatResponse:
    inbound = {"type": "control_chat", "profile_id": payload.profile_id, "content": payload.message}
    result = _gateway.quarantine(inbound, "epistemic_risk")
    runtime = _runtimes.get(payload.profile_id)
    if runtime is None:
        return ChatResponse(ok=False, accepted=False, processed_count=0, quarantine_count=len(_gateway.recent(limit=2000)))
    accepted = runtime.submit({"content": payload.message, "profile_id": payload.profile_id, "type": "control_chat"})["accepted"]
    processed = runtime.processed_count
    quarantine = len(_gateway.recent(limit=2000))
    ok = not isinstance(result, Cancelled)
    return ChatResponse(ok=ok, accepted=accepted, processed_count=processed, quarantine_count=quarantine)


@router.post("/runtime/start", response_model=RuntimeStartResponse)
def runtime_start(payload: RuntimeStartRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> RuntimeStartResponse:
    profile = AgentProfile(
        profile_id=payload.profile_id,
        display_name=payload.display_name,
        memory_partition=payload.memory_partition,
    )
    runtime = SovereignAgentRuntime(profile=profile)
    runtime.start()
    _runtimes[payload.profile_id] = runtime
    return RuntimeStartResponse(ok=True, profile_id=payload.profile_id)


@router.get("/runtime/status", response_model=list[RuntimeStatusResponse])
def runtime_status(auth: Dict[str, Any] = Depends(require_bearer_token)) -> list[RuntimeStatusResponse]:
    statuses = []
    for profile_id, runtime in _runtimes.items():
        state = runtime.state()
        statuses.append(RuntimeStatusResponse(
            profile_id=profile_id,
            started_at=state["started_at"],
            queue_depth=state["queue_depth"],
            processed_count=state["processed_count"],
            quarantine_count=state["quarantine_count"],
        ))
    return statuses


@router.post("/runtime/stop")
def runtime_stop(profile_id: str, auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    runtime = _runtimes.get(profile_id)
    if not runtime:
        return {"ok": True, "error": "not_found"}
    runtime.stop()
    return {"ok": True}


@router.get("/memory/search")
def memory_search(q: str, auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    from memory.honcho_router import HonchoMemoryRouter

    router = HonchoMemoryRouter()
    results = router.recall(f"query:{q}")
    return {"query": q, "results": results}

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from cognitive_compiler.desktop_harness_v1 import DesktopHarness
from cognitive_compiler.meta_router_v2 import HarnessDecision, MetaRoutingResult, CognitiveTemperature
from cognitive_compiler.router_observer import RouterObserver
from cognitive_compiler.shared_cognitive_state import SharedCognitiveState
from msb_v2.api.middleware import require_bearer_token

router = APIRouter(prefix="/desktop", tags=["desktop"])

_harness = DesktopHarness()


class DesktopExecutePayload(BaseModel):
    goal: str
    timeout_s: float = 600.0
    intent: Optional[str] = None


def _fake_routing_result(intent: Optional[str]) -> MetaRoutingResult:
    primary = "desktop" if intent == "desktop" else "building"
    return MetaRoutingResult(
        decision=HarnessDecision(primary=primary, secondary=None, confidence=0.95),
        scs=SharedCognitiveState(problem_statement=""),
        temperature=CognitiveTemperature(score=0.0),
        rerouted=False,
        elapsed_s=0.0,
    )


@router.get("/health")
def desktop_health():
    return {"status": "ok", "module": "desktop"}


@router.get("/status")
def desktop_status():
    return _harness.status


@router.post("/stop")
def stop_desktop(auth: Dict[str, Any] = Depends(require_bearer_token)):
    return _harness.stop()


@router.post("/execute")
def execute_desktop(payload: DesktopExecutePayload, auth: Dict[str, Any] = Depends(require_bearer_token)):
    result = _harness.execute(payload.goal, timeout_s=payload.timeout_s)
    try:
        RouterObserver(log_path="runtime/desktop_routing_observations.jsonl").record(_fake_routing_result(payload.intent), payload.goal)
    except Exception:
        pass
    return result


@router.post("/approve")
def approve_desktop(confirm_token: str, approved: bool = True):
    if not confirm_token:
        raise HTTPException(status_code=400, detail="confirm_token is required")
    result = _harness.approve_run(confirm_token=confirm_token, approved=approved)
    status = 200 if result.get("state") != "rejected" else 409
    return JSONResponse(result, status_code=status)

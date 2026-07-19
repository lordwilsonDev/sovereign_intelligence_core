from __future__ import annotations

import asyncio
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from msb_v2.api.middleware import require_bearer_token
from msb_v2.aura.aura_core import AURACore
from msb_v2.aura.models import State

from msb_v2.v3.contracts import HarnessContract
from msb_v2.v3.contracts import register as _register_contract
router = APIRouter(tags=["aura"])


@router.post("/run", dependencies=[Depends(require_bearer_token)])
def aura_run(payload: dict) -> JSONResponse:
    goal = str(payload.get("goal", "") or "")
    state = asyncio.run(AURACore().run(goal=goal))
    last = state.context.get("last_tool_result") or {}
    result = {
        "session_id": state.session_id,
        "goal": state.current_goal,
        "status": state.context.get("task_status"),
        "result": last.get("message") or last.get("now") or last,
        "step": state.step,
    }
    return JSONResponse({"status": "ok", "result": result})
# HCL contract registration
_register_contract(HarnessContract(route="/aura/run", method="post", allow_anonymous=False))

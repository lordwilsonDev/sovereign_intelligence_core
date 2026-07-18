from __future__ import annotations

import asyncio
from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from msb_v2.aura.aura_core import AURACore
from msb_v2.aura.models import State

router = APIRouter(tags=["aura"])


@router.post("/run")
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

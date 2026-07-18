from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from msb_v2.aura.core import AURACore, State, Task

router = APIRouter(tags=["aura"])


@router.post("/aura/run")
def aura_run(payload: dict) -> JSONResponse:
    goal = payload.get("goal", "")
    task = Task(goal=goal)
    state = State(task=task)
    final = AURACore().run(state)
    return JSONResponse({"status": "ok", "result": final["last_result"], "state": final})

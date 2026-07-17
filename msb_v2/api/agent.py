from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from msb_v2.agent.prompt_contract import build_hermes_phase5_contract
from msb_v2.agent.runtime import AgentRuntime
from msb_v2.runtime.context import RuntimeContext

router = APIRouter(tags=["agent"])

_context = RuntimeContext()
_agent = AgentRuntime(worker_pool=_context.workers)
_contract = build_hermes_phase5_contract()


class AgentTaskRequest(BaseModel):
    task_id: str
    name: str
    callable: str
    payload: Dict[str, Any] = {}


class AgentRunRequest(BaseModel):
    run_id: str
    tasks: List[Dict[str, Any]]


@router.post("/agent/run")
def agent_run(payload: AgentRunRequest) -> JSONResponse:
    result = _agent.run(payload.run_id, list(payload.tasks))
    result["contract"] = {
        "citation": "msb_v2.agent.prompt_contract:build_hermes_phase5_contract",
        "version": "phase5",
    }
    return JSONResponse(result)


@router.get("/agent/run/{run_id}")
def agent_run_status(run_id: str) -> JSONResponse:
    return JSONResponse(_agent.run_status(run_id))

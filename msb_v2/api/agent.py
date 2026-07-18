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


class AgentRunLoopRequest(BaseModel):
    run_id: str
    max_iterations: int = 1
    interval_seconds: float = 0.0
    task_template: Dict[str, Any] = {}
    stop_on_error: bool = False


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


@router.post("/agent/run/loop")
def agent_run_loop(payload: AgentRunLoopRequest) -> JSONResponse:
    config = dict(payload.model_dump())
    config.pop("run_id", None)
    result = _agent.run_loop(payload.run_id, config)
    return JSONResponse(result)


def _queue() -> TaskQueue:
    from msb_v2.agent.task_queue import get_queue
    return get_queue()


@router.post("/agent/plan")
def agent_plan(goal: str) -> JSONResponse:
    from msb_v2.agent.planner import Plan, fallback_plan, Step

    plan = fallback_plan(goal) if not goal.strip() else Plan(
        goal=goal,
        steps=[Step(step=1, tool="noop_command", description=goal, critical=True)],
    )
    return JSONResponse({
        "goal": plan.goal,
        "steps": [
            {
                "step": s.step,
                "tool": s.tool,
                "description": s.description,
                "parameters": s.parameters,
                "critical": s.critical,
            }
            for s in plan.steps
        ],
    })


@router.post("/agent/execute")
def agent_execute(goal: str) -> JSONResponse:
    from msb_v2.agent.planner import Plan, Step
    from msb_v2.agent.executor import execute

    plan = Plan(goal=goal, steps=[Step(step=1, tool="noop_command", description=goal, critical=True)])
    result = execute(goal, plan=plan)
    return JSONResponse({"goal": goal, "result": result, "steps_completed": 1})


@router.post("/agent/queue")
def agent_queue_submit(goal: str, priority: int = 2) -> JSONResponse:
    from msb_v2.agent.task_queue import TaskPriority, get_queue

    p = TaskPriority.HIGH if priority <= 1 else (TaskPriority.LOW if priority >= 3 else TaskPriority.NORMAL)
    task_id = _queue().submit(goal, priority=p)
    return JSONResponse({"task_id": task_id, "status": "queued"})


@router.get("/agent/queue/{task_id}")
def agent_queue_status(task_id: str) -> JSONResponse:
    status = _queue().status(task_id)
    if status is None:
        return JSONResponse({"error": "not_found"}, status_code=404)
    return JSONResponse(status)

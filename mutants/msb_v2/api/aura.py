from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from msb_v2.aura.aura_core import AURACore
from msb_v2.aura.langgraph_bridge import sovereign_tool_calls
from msb_v2.aura.memory.retriever import BM25Retriever
from msb_v2.aura.models import Task
from msb_v2.aura.orchestrator import submit_goals
from msb_v2.aura.persistence import Persistence
from msb_v2.aura.policies.engine import PolicyEngine

router = APIRouter()
_core = AURACore()
_persistence = Persistence("/tmp/_msb_aura_tests.sqlite")
_retriever = BM25Retriever([])
_policy_engine = PolicyEngine()


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class RunRequest(BaseModel):
    goal: str
    session_id: Optional[str] = None


class GoalsRequest(BaseModel):
    goals: List[str]
    client_id: str = "default"
    priority: int = 2


@router.post("/run")
def aura_run(payload: RunRequest) -> Dict[str, Any]:
    state = asyncio.run(
        _core.run(
            goal=payload.goal,
            session_id=payload.session_id,
            retriever=_retriever,
            policy_engine=_policy_engine,
        )
    )
    task = Task(goal=payload.goal, metadata={"session_id": state.session_id, "step_count": state.step})
    _persistence.save_task(task.__dict__)
    return {
        "status": "ok",
        "task_id": state.task_id,
        "session_id": state.session_id,
        "step": state.step,
    }


@router.post("/tasks")
def aura_tasks(payload: GoalsRequest) -> Dict[str, Any]:
    tasks = asyncio.run(submit_goals(payload.goals, client_id=payload.client_id, priority=payload.priority))
    return {"status": "ok", "task_ids": [t.task_id for t in tasks], "count": len(tasks)}


@router.get("/tasks/recent")
def aura_recent_tasks(limit: int = 20) -> Dict[str, Any]:
    # AURA tasks are not persisted in a dedicated task table by default; return recent events by session count proxy.
    return {"status": "ok", "recent_limit": limit}


class ToolCallsRequest(BaseModel):
    tool_calls: List[Dict[str, Any]]


@router.post("/langgraph/tools")
def aura_langgraph_tool_calls(payload: ToolCallsRequest) -> Dict[str, Any]:
    return sovereign_tool_calls(payload.tool_calls)

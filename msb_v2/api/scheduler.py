from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Body
from pydantic import BaseModel
from msb_v2.agent.task_queue import TaskPriority, get_queue

from msb_v2.v3.contracts import HarnessContract
from msb_v2.v3.contracts import register as _register_contract
router = APIRouter(tags=["scheduler"])


class SchedulerSubmitRequest(BaseModel):
    goal: str
    priority: int = 2


@router.post("/scheduler/submit")
def scheduler_submit(body: SchedulerSubmitRequest) -> Dict[str, Any]:
    p = TaskPriority.HIGH if body.priority <= 1 else (TaskPriority.LOW if body.priority >= 3 else TaskPriority.NORMAL)
    task_id = get_queue().submit(body.goal, priority=p)
    return {"task_id": task_id, "status": "queued", "priority": p.value}


@router.get("/scheduler/status/{task_id}")
def scheduler_status(task_id: str) -> Dict[str, Any]:
    status = get_queue().get_status(task_id)
    if status is None:
        return {"task_id": task_id, "status": "not_found"}
    return status


@router.get("/scheduler/queue")
def scheduler_queue() -> Dict[str, Any]:
    return {"tasks": get_queue().get_all_statuses()}
# HCL contract registration
_register_contract(HarnessContract(route="/scheduler/submit", method="post", allow_anonymous=False))

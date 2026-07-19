from __future__ import annotations

from fastapi import APIRouter, Depends

from msb_v2.api.middleware import require_bearer_token
from msb_v2.agent.task_queue import TaskPriority, get_queue

from msb_v2.v3.contracts import HarnessContract
from msb_v2.v3.contracts import register as _register_contract
router = APIRouter()


@router.post("/v3/tasks/submit")
def submit_task(goal: str, priority: str = "normal", auth: Dict[str, Any] = Depends(require_bearer_token)) -> dict:
    pq = TaskPriority.NORMAL
    if priority.lower() == "high":
        pq = TaskPriority.HIGH
    elif priority.lower() == "low":
        pq = TaskPriority.LOW

    queue = get_queue()
    task_id = queue.submit(goal=goal, priority=pq)
    return {"status": "queued", "task_id": task_id}


@router.get("/v3/tasks/{task_id}")
def get_task_status(task_id: str) -> dict:
    queue = get_queue()
    status = queue.get_status(task_id)
    if status is None:
        return {"error": "not_found"}
    return status


@router.get("/v3/tasks")
def list_tasks() -> dict:
    queue = get_queue()
    return {"tasks": queue.get_all_statuses()}
# HCL contract registration
_register_contract(HarnessContract(route="/v3/tasks/submit", method="post", allow_anonymous=False))

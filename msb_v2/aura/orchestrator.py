from __future__ import annotations

from typing import Any, Dict, List

from msb_v2.aura.models import Task, TaskStatus
from msb_v2.aura.persistence import Persistence
from msb_v2.aura.scheduler import Scheduler
from msb_v2.aura.validator import TaskValidator


async def submit_goals(goals: List[str], client_id: str = "default", priority: int = 2) -> List[Task]:
    scheduler = Scheduler()
    tasks: List[Task] = []
    for goal in goals:
        task = Task(goal=goal, status=TaskStatus.PENDING, client_id=client_id, priority=int(priority))
        scheduler.enqueue(task)
        tasks.append(task)
    return tasks


async def run_scheduler(persistence: Persistence, task_count: int = 50, failure_rate: float = 0.1) -> Dict[str, Any]:
    scheduler = Scheduler(persistence=persistence, worker_count=4, fail_substring="fail-now")
    goals = [f"test goal {idx}" for idx in range(task_count)]
    injected_failures = max(1, int(task_count * failure_rate))
    for idx in range(injected_failures):
        goals[idx] = f"fail-now {idx}"
    enqueued: List[Task] = []
    for goal in goals:
        task = Task(goal=goal, status=TaskStatus.PENDING)
        scheduler.enqueue(task)
        enqueued.append(task)
    results = await scheduler.drain()
    return {
        "enqueued": len(enqueued),
        "processed": len(results),
        "dlq": scheduler.dlq,
        "status": "ok",
    }


async def validate_output(task: Task, output: Dict[str, Any]) -> Dict[str, Any]:
    validator = TaskValidator()
    result = validator.validate(task, output)
    return {
        "ok": result.ok,
        "layer": result.layer,
        "message": result.message,
        "details": result.details,
    }

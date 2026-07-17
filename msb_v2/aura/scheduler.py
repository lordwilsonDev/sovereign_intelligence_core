from __future__ import annotations

import asyncio
from typing import List, Optional, Tuple

from msb_v2.aura.models import Task, TaskStatus
from msb_v2.aura.persistence import Persistence
from msb_v2.aura.aura_core import AURACore


class Worker:
    def __init__(self, worker_id: str, core: "AURACore", persistence: Persistence, fail_substring: str | None = None) -> None:
        self.worker_id = worker_id
        self.core = core
        self.persistence = persistence
        self.fail_substring = fail_substring

    async def handle(self, task: Task) -> Task:
        task.status = TaskStatus.RUNNING
        self.persistence.save_task(task.__dict__)
        session_id = f"worker-{self.worker_id}-{task.task_id}"
        try:
            if self.fail_substring and self.fail_substring in task.goal:
                raise RuntimeError("simulated worker failure")
            state = await self.core.run(goal=task.goal, session_id=session_id)
            task.status = TaskStatus.COMPLETED
            task.metadata["session_id"] = state.session_id
            task.metadata["step_count"] = state.step
            task.metadata["last_tool_status"] = state.context.get("last_tool_status", "SUCCESS")
        except Exception as exc:
            task.status = TaskStatus.FAILED
            task.retry_count += 1
            task.metadata["last_error"] = str(exc)
        self.persistence.save_task(task.__dict__)
        return task


class Scheduler:
    def __init__(self, persistence: Persistence | None = None, max_retries: int = 3, worker_count: int = 4, fail_substring: str | None = None) -> None:
        self.persistence = persistence or Persistence()
        self.max_retries = max_retries
        self.worker_count = worker_count
        self.fail_substring = fail_substring
        self.queue: asyncio.PriorityQueue[Tuple[int, float, Task]] = asyncio.PriorityQueue()
        self.dlq: List[Task] = []
        self.core = AURACore(persistence=self.persistence)

    def enqueue(self, task: Task) -> None:
        self.queue.put_nowait((int(task.priority.value), float(task.created_at), task))

    async def run_once(self) -> Optional[Task]:
        if self.queue.empty():
            return None
        priority, created_at, task = await self.queue.get()
        worker = Worker(worker_id=f"{priority}-{created_at:.6f}", core=self.core, persistence=self.persistence, fail_substring=self.fail_substring)
        result = await worker.handle(task)
        if result.status == TaskStatus.FAILED and result.retry_count < self.max_retries:
            result.status = TaskStatus.RETRYING
            self.persistence.save_task(result.__dict__)
            self.enqueue(result)
        elif result.status == TaskStatus.FAILED:
            result.status = TaskStatus.DLQ
            self.persistence.save_task(result.__dict__)
            self.dlq.append(result)
        return result

    async def drain(self) -> List[Task]:
        results: List[Task] = []
        while not self.queue.empty():
            results.append(await self.run_once())
        return results

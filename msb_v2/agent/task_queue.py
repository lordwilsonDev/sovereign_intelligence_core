from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


@dataclass
class Task:
    task_id: str
    goal: str
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: str = ""
    priority: TaskPriority = TaskPriority.NORMAL
    cancel_flag: threading.Event = field(default_factory=threading.Event)
    created_at: float = field(default_factory=time.time)
    started_at: float | None = None
    finished_at: float | None = None


class TaskQueue:
    def __init__(self, max_concurrent: int = 1) -> None:
        self._queue: list[Task] = []
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._tasks: dict[str, Task] = {}
        self._running = False
        self._worker_thread: threading.Thread | None = None
        self._max_concurrent = max_concurrent
        self._active_count = 0
        self._resolve: Callable[..., str] | None = None

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True, name="TaskQueue")
        self._worker_thread.start()

    def stop(self) -> None:
        self._running = False
        with self._condition:
            self._condition.notify_all()

    def submit(self, goal: str, priority: TaskPriority = TaskPriority.NORMAL) -> str:
        task = Task(
            task_id=str(uuid.uuid4())[:8],
            goal=goal or "",
            priority=priority,
        )
        with self._condition:
            self._queue.append(task)
            self._tasks[task.task_id] = task
            self._queue.sort(key=lambda t: (t.priority.value, t.created_at))
            self._condition.notify()
        return task.task_id

    def cancel(self, task_id: str) -> bool:
        with self._lock:
            task = self._tasks.get(task_id)
            if not task or task.status in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED):
                return False
            task.cancel_flag.set()
            task.status = TaskStatus.CANCELLED
            return True

    def status(self, task_id: str) -> dict | None:
        return self.get_status(task_id)

    def get_status(self, task_id: str) -> dict | None:
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return None
            return {
                "task_id": task.task_id,
                "goal": task.goal,
                "status": task.status.value,
                "result": task.result,
                "error": task.error,
                "priority": task.priority.value,
            }

    def wait_completed(self, task_id: str, timeout: float = 5.0) -> dict | None:
        deadline = time.time() + max(timeout, 0)
        while time.time() < deadline:
            with self._lock:
                task = self._tasks.get(task_id)
                if not task or task.status in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED):
                    return self.get_status(task_id)
            time.sleep(0.05)
        return self.get_status(task_id)

    def wait_running(self, task_id: str, timeout: float = 2.0) -> bool:
        deadline = time.time() + max(timeout, 0)
        while time.time() < deadline:
            with self._lock:
                task = self._tasks.get(task_id)
                if task and task.status == TaskStatus.RUNNING:
                    return True
            time.sleep(0.05)
        return False

    def get_all_statuses(self) -> list[dict]:
        with self._lock:
            return [
                {
                    "task_id": t.task_id,
                    "goal": t.goal[:50],
                    "status": t.status.value,
                    "priority": t.priority.value,
                }
                for t in self._tasks.values()
            ]

    def _worker_loop(self) -> None:
        while self._running:
            with self._condition:
                while self._running and not self._next_task():
                    self._condition.wait(timeout=1.0)
                task = self._next_task()
                if task:
                    task.status = TaskStatus.RUNNING
                    task.started_at = time.time()
                    self._active_count += 1
                    try:
                        self._queue.remove(task)
                    except ValueError:
                        pass

            if task:
                try:
                    task.result = self._run_resolve(task)
                    if task.cancel_flag.is_set():
                        task.status = TaskStatus.CANCELLED
                    else:
                        task.status = TaskStatus.COMPLETED
                except Exception as e:
                    task.status = TaskStatus.FAILED
                    task.error = str(e)
                with self._lock:
                    task.finished_at = time.time()
                    self._active_count -= 1
                with self._condition:
                    self._condition.notify()

    def _run_resolve(self, task: Task) -> str:
        if self._resolve is not None:
            return self._resolve(task.goal, task.cancel_flag)
        return f"executed: {task.goal}"

    def _next_task(self) -> Task | None:
        if self._active_count >= self._max_concurrent:
            return None
        for task in self._queue:
            if task.status == TaskStatus.PENDING and not task.cancel_flag.is_set():
                return task
        return None


_queue: TaskQueue | None = None
_queue_lock = threading.Lock()


def get_queue(max_concurrent: int = 1) -> TaskQueue:
    global _queue
    with _queue_lock:
        if _queue is None:
            _queue = TaskQueue(max_concurrent=max_concurrent)
            _queue.start()
    return _queue

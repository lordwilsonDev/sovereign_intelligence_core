from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Any


class TaskState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority:
    HIGH = 1
    NORMAL = 2
    LOW = 3


@dataclass(order=True)
class Task:
    priority: int
    created_at: float = field(compare=False)
    task_id: str = field(compare=False)
    goal: str = field(compare=False)
    status: TaskState = field(compare=False, default=TaskState.PENDING)
    result: Any = field(compare=False, default=None)
    error: str = field(compare=False, default="")
    cancel_flag: threading.Event = field(compare=False, default_factory=threading.Event)
    on_complete: Callable | None = field(compare=False, default=None)


class TaskQueue:
    def __init__(self, max_concurrent: int = 1) -> None:
        self._queue: list[Task] = []
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._tasks: dict[str, Task] = {}
        self._running = False
        self._worker: threading.Thread | None = None
        self._max_concurrent = max_concurrent
        self._active = 0
        self._resolve = self._default_resolve

    def start(self) -> None:
        with self._lock:
            if self._running:
                return
            self._running = True
            self._worker = threading.Thread(target=self._loop, daemon=True, name="agent-task-queue")
            self._worker.start()

    def stop(self) -> None:
        with self._condition:
            self._running = False
            self._condition.notify_all()

    def submit(self, goal: str, priority: int = TaskPriority.NORMAL, on_complete: Callable | None = None) -> str:
        import uuid

        task_id = uuid.uuid4().hex[:8]
        task = Task(
            priority=priority,
            created_at=time.time(),
            task_id=task_id,
            goal=goal,
            on_complete=on_complete,
        )
        with self._condition:
            self._queue.append(task)
            self._queue.sort(key=lambda t: (t.priority, t.created_at))
            self._tasks[task_id] = task
            self._condition.notify()
        return task_id

    def cancel(self, task_id: str) -> bool:
        with self._lock:
            task = self._tasks.get(task_id)
            if not task or task.status in {TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELLED}:
                return False
            task.cancel_flag.set()
            task.status = TaskState.CANCELLED
            return True

    def status(self, task_id: str) -> dict | None:
        with self._lock:
            t = self._tasks.get(task_id)
            if not t:
                return None
            return {"task_id": t.task_id, "goal": t.goal, "status": t.status.value, "error": t.error, "result": t.result}

    def pending_count(self) -> int:
        with self._lock:
            return sum(1 for t in self._queue if t.status == TaskState.PENDING)

    def wait_running(self, task_id: str, timeout: float = 1.0) -> bool:
        deadline = time.time() + timeout
        while time.time() < deadline:
            st = self.status(task_id)
            if st and st["status"] == TaskState.RUNNING.value:
                return True
            time.sleep(0.05)
        return False

    def wait_completed(self, task_id: str, timeout: float = 2.0) -> dict | None:
        deadline = time.time() + timeout
        while time.time() < deadline:
            st = self.status(task_id)
            if st and st["status"] in {TaskState.COMPLETED.value, TaskState.FAILED.value, TaskState.CANCELLED.value}:
                return st
            time.sleep(0.05)
        return None

    def _default_resolve(self, goal: str, cancel_flag: threading.Event | None = None) -> str:
        return "done"

    def _next(self) -> Task | None:
        if self._active >= self._max_concurrent:
            return None
        for t in self._queue:
            if t.status == TaskState.PENDING and not t.cancel_flag.is_set():
                return t
        return None

    def _loop(self) -> None:
        while True:
            with self._condition:
                while self._running and not self._next():
                    self._condition.wait(timeout=1.0)
                if not self._running:
                    break
                task = self._next()
                if task:
                    task.status = TaskState.RUNNING
                    self._active += 1
                    try:
                        self._queue.remove(task)
                    except ValueError:
                        pass

            if task:
                threading.Thread(target=self._run, args=(task,), daemon=True).start()

    def _run(self, task: Task) -> None:
        try:
            result = self._resolve(task.goal, cancel_flag=task.cancel_flag)
            with self._lock:
                if task.cancel_flag.is_set():
                    task.status = TaskState.CANCELLED
                else:
                    task.status = TaskState.COMPLETED
                    task.result = result
                self._active -= 1
            if task.on_complete and not task.cancel_flag.is_set():
                try:
                    task.on_complete(task.task_id, result)
                except Exception:
                    pass
        except Exception as exc:
            with self._lock:
                task.status = TaskState.FAILED
                task.error = str(exc)
                self._active -= 1
        with self._condition:
            self._condition.notify_all()

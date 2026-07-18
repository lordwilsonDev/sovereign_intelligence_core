from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, List


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    DLQ = "DLQ"


class Priority(int, Enum):
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3


@dataclass
class AURATask:
    task_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    goal: str = ""
    client_id: str = "default"
    priority: int = Priority.MEDIUM.value
    status: str = TaskStatus.PENDING.value
    created_at: float = field(default_factory=time.time)
    retry_count: int = 0
    max_retries: int = 3
    metadata: dict = field(default_factory=dict)


class Scheduler:
    def __init__(self) -> None:
        self._queue: List[tuple[int, float, AURATask]] = []
        self._lock = threading.Lock()
        self._dlq: List[AURATask] = []

    def submit(self, task: AURATask) -> AURATask:
        with self._lock:
            self._queue.append((int(task.priority), task.created_at, task))
            self._queue.sort(key=lambda x: (x[0], x[1]))
            task.status = TaskStatus.PENDING.value
        return task

    def next(self) -> AURATask | None:
        with self._lock:
            if not self._queue:
                return None
            _, _, task = self._queue.pop(0)
            task.status = TaskStatus.RUNNING.value
            return task

    def complete(self, task_id: str) -> None:
        with self._lock:
            self._queue = [item for item in self._queue if item[2].task_id != task_id]

    def retry(self, task: AURATask) -> None:
        with self._lock:
            if task.retry_count >= task.max_retries:
                task.status = TaskStatus.DLQ.value
                self._dlq.append(task)
            else:
                task.retry_count += 1
                task.status = TaskStatus.RETRYING.value
                self._queue.append((int(task.priority), task.created_at, task))
                self._queue.sort(key=lambda x: (x[0], x[1]))

    def dlq(self) -> List[AURATask]:
        with self._lock:
            return list(self._dlq)

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


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
class AuraTask:
    goal: str = ""
    task_id: str = field(default_factory=lambda: __import__("uuid").uuid4().hex[:8])
    client_id: str = "default"
    priority: int = Priority.MEDIUM.value
    status: str = TaskStatus.PENDING.value
    created_at: float = field(default_factory=time.time)
    retry_count: int = 0
    max_retries: int = 3
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "goal": self.goal,
            "client_id": self.client_id,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "metadata": self.metadata,
            "error": self.error,
        }


class Scheduler:
    def __init__(self, persistence: Any = None, worker_count: int = 1, fail_substring: str = "", max_retries: int = 3) -> None:
        self._persistence = persistence
        self._worker_count = max(1, int(worker_count))
        self._fail_substring = str(fail_substring)
        self._max_retries = max(1, int(max_retries))
        self._queue: List[tuple[int, float, Dict[str, Any]]] = []
        self._processed: List[Dict[str, Any]] = []

    def _to_dict(self, task: Any) -> Dict[str, Any]:
        if isinstance(task, dict):
            return task
        if hasattr(task, "to_dict"):
            return task.to_dict()
        return {
            "task_id": getattr(task, "task_id", ""),
            "goal": getattr(task, "goal", ""),
            "status": getattr(task, "status", TaskStatus.PENDING.value),
            "priority": int(getattr(task, "priority", Priority.MEDIUM.value)),
            "max_retries": int(getattr(task, "max_retries", 3)),
            "retry_count": int(getattr(task, "retry_count", 0)),
            "error": getattr(task, "error", ""),
            "created_at": getattr(task, "created_at", time.time()),
        }

    def enqueue(self, task: Any) -> None:
        item = self._to_dict(task)
        item["status"] = TaskStatus.PENDING.value
        item.setdefault("max_retries", self._max_retries)
        item.setdefault("retry_count", 0)
        self._queue.append((int(item.get("priority", 2)), float(item.get("created_at", time.time())), item))
        self._queue.sort(key=lambda x: (x[0], x[1]))

    def _process(self, item: Dict[str, Any]) -> None:
        item["status"] = TaskStatus.RUNNING.value
        if self._fail_substring and self._fail_substring in item.get("goal", ""):
            item["error"] = "forced failure"
            if int(item.get("retry_count", 0)) >= int(item.get("max_retries", self._max_retries)):
                item["status"] = TaskStatus.DLQ.value
                self._processed.append(item)
                return
            item["retry_count"] = int(item.get("retry_count", 0)) + 1
            item["status"] = TaskStatus.RETRYING.value
            self._queue.append((int(item.get("priority", 2)), float(item.get("created_at", time.time())), item))
            self._queue.sort(key=lambda x: (x[0], x[1]))
            return
        item["status"] = TaskStatus.COMPLETED.value
        item["error"] = ""
        self._processed.append(item)

    async def drain(self) -> List[Dict[str, Any]]:
        while self._queue:
            _, _, item = self._queue.pop(0)
            self._process(item)
        return list(self._processed)

    @property
    def history(self) -> List[Dict[str, Any]]:
        return [t for t in self._processed if t.get("status") == TaskStatus.COMPLETED.value]

    @property
    def dlq(self) -> List[Dict[str, Any]]:
        return [t for t in self._processed if t.get("status") == TaskStatus.DLQ.value]


async def run_scheduler(persistence: Any, task_count: int = 50, failure_rate: float = 0.1) -> Dict[str, Any]:
    scheduler = Scheduler(persistence=persistence, worker_count=4, fail_substring="fail-now")
    for i in range(max(1, int(task_count))):
        scheduler.enqueue(AuraTask(goal=f"test goal {i}"))
    scheduler.drain()
    return {
        "enqueued": int(task_count),
        "processed": len(scheduler.history) + len(scheduler.dlq),
        "dlq": scheduler.dlq,
        "status": "ok",
    }


def validate_output(task: Any, output: Dict[str, Any]) -> Dict[str, Any]:
    forbidden = ["rm -rf", "sudo rm", "drop table"]
    text = " ".join(str(output.get(k, "")) for k in ["message", "status"]) if isinstance(output, dict) else str(output)
    for token in forbidden:
        if token in text.lower():
            return {"ok": False, "layer": "deterministic", "message": "forbidden pattern"}
    confidence = 0.0
    if isinstance(output, dict) and "confidence" in output:
        try:
            confidence = float(output["confidence"])
        except (TypeError, ValueError):
            confidence = 0.0
    if confidence < 0.6:
        return {"ok": False, "layer": "rules", "message": "low confidence"}
    return {"ok": True, "layer": "deterministic", "message": "ok"}

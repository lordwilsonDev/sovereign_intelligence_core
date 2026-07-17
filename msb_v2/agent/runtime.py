from __future__ import annotations

import importlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional


def _split_callable_path(dotted: str) -> tuple[str, str]:
    """Return (`module_path`, `func_name`) from a dotted path.

    Supports separator-style dotted paths (`module.path.name`) and
    colon-style paths (`module.path:name`).
    """
    if ":" in dotted:
        module_path, _, func_name = dotted.rpartition(":")
        return module_path, func_name

    module_path, _, func_name = dotted.rpartition(".")
    if not module_path:
        raise ValueError(f"invalid callable path: {dotted}")
    return module_path, func_name


def _import_callable(dotted: str) -> Callable[..., Any]:
    module_path, func_name = _split_callable_path(dotted)
    module = importlib.import_module(module_path)
    if hasattr(module, func_name):
        return getattr(module, func_name)
    raise AttributeError(f"module '{module_path}' has no attribute '{func_name}'")


@dataclass
class AgentTask:
    task_id: str
    name: str
    payload: Dict[str, Any]
    status: str = "queued"
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class AgentRuntime:
    def __init__(self, worker_pool: Any) -> None:
        self._pool = worker_pool
        self._runs: Dict[str, List[AgentTask]] = {}

    def run(self, run_id: str, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        records: List[AgentTask] = []
        for task_def in tasks:
            task = AgentTask(
                task_id=task_def.get("task_id", str(uuid.uuid4())),
                name=task_def.get("name", "unnamed"),
                payload=task_def.get("payload", {}),
            )
            callable_path = task_def.get("callable")
            if not callable_path:
                task.status = "skipped"
                task.error = "missing_callable_path"
                records.append(task)
                continue
            try:
                fn = _import_callable(str(callable_path))
                task.result = fn(**task.payload)
                task.status = "completed"
            except Exception as exc:
                task.status = "failed"
                task.error = f"{exc.__class__.__name__}: {exc}"
            records.append(task)
        self._runs[run_id] = records
        return {
            "run_id": run_id,
            "count": len(records),
            "completed": sum(1 for t in records if t.status == "completed"),
            "failed": sum(1 for t in records if t.status == "failed"),
            "tasks": [
                {
                    "task_id": t.task_id,
                    "name": t.name,
                    "status": t.status,
                    "error": t.error,
                    "result": t.result,
                }
                for t in records
            ],
        }

    def run_status(self, run_id: str) -> Dict[str, Any]:
        tasks = self._runs.get(run_id, [])
        return {
            "run_id": run_id,
            "count": len(tasks),
            "completed": sum(1 for t in tasks if t.status == "completed"),
            "failed": sum(1 for t in tasks if t.status == "failed"),
            "tasks": [
                {
                    "task_id": t.task_id,
                    "name": t.name,
                    "status": t.status,
                    "error": t.error,
                    "result": t.result,
                }
                for t in tasks
            ],
        }


def _agent_echo(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"echo": payload}

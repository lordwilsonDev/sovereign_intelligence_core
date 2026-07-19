from __future__ import annotations

import importlib
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

from msb_v2.runtime.replay import replay_store


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
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat() + "Z")


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
        replay_store.record_run(
            run_id,
            [
                {
                    "task_id": t.task_id,
                    "name": t.name,
                    "status": t.status,
                    "error": t.error,
                    "result": t.result,
                }
                for t in records
            ],
        )
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

    def run_loop(self, run_id: str, loop_config: Dict[str, Any]) -> Dict[str, Any]:
        """VY-NEXUS-style 24-hour loop grounded on WorkerPool/RuntimeContext/EvolutionMemory."""
        max_iterations = min(int(loop_config.get("max_iterations", 24)), 24)
        interval_seconds = max(float(loop_config.get("interval_seconds", 60.0)), 0.0)
        task_template = loop_config.get("task_template", {})
        stop_on_error = bool(loop_config.get("stop_on_error", False))

        iterations: List[Dict[str, Any]] = []
        completed = 0
        failed = 0
        last_error: Optional[str] = None
        stopped_reason: Optional[str] = None

        for i in range(max_iterations):
            iteration_task = {
                "task_id": f"{run_id}-iter-{i + 1}",
                "name": task_template.get("name", "loop-iteration"),
                "callable": task_template.get("callable") or "msb_v2.agent.runtime:_agent_echo",
                "payload": {
                    "payload": {
                        "iteration": i + 1,
                        "run_id": run_id,
                        **(task_template.get("payload", {})),
                    }
                },
            }
            result = self.run(f"{run_id}-iter-{i + 1}", [iteration_task])
            task = result["tasks"][0]
            iteration = {
                "iteration": i + 1,
                "task_id": task["task_id"],
                "status": task["status"],
            }
            iterations.append(iteration)
            if task["status"] == "completed":
                completed += 1
            else:
                failed += 1
                last_error = task.get("error")
                if stop_on_error:
                    stopped_reason = f"stopped after {i + 1} iteration(s): {last_error}"
                    break
            if interval_seconds > 0 and i + 1 < max_iterations:
                time.sleep(interval_seconds)

        return {
            "run_id": run_id,
            "mode": "loop",
            "max_iterations": max_iterations,
            "iterations": iterations,
            "completed": completed,
            "failed": failed,
            "last_error": last_error,
            "stopped_reason": stopped_reason,
        }


def _agent_echo(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"echo": payload}

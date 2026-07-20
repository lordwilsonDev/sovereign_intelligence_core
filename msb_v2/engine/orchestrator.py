"""A small, deterministic dependency orchestrator.

This module deliberately has no framework dependency.  It provides the
execution contract that future prompt, memory, tool, and model nodes can use.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


PENDING = "pending"
RUNNING = "running"
SUCCEEDED = "succeeded"
FAILED = "failed"
BLOCKED = "blocked"


@dataclass
class Task:
    """One unit of work in a dependency graph.

    ``dependencies`` contains task IDs. ``action`` is optional so callers can
    construct a graph before attaching executable work.
    """

    id: str
    action: Callable[[], Any] | None = None
    status: str = PENDING
    dependencies: list[str] = field(default_factory=list)
    result: Any = None


def _safe(value: Any) -> Any:
    try:
        return value if isinstance(value, (bool, int, float, str)) else str(value)
    except Exception:
        return None


def orchestrate(
    tasks: list[Task],
    hook: Callable[[str, str, dict[str, Any] | None, str | None], dict[str, Any]] | None = None,
) -> list[Task]:
    """Run ready tasks until the graph is complete.

    Tasks execute in input order when several are ready. A failed task is
    retained as ``failed``; every descendant is marked ``blocked`` and is not
    executed. Invalid or cyclic dependency graphs raise ``ValueError``.
    """
    if not tasks:
        return []

    by_id = {task.id: task for task in tasks}
    if len(by_id) != len(tasks):
        raise ValueError("Task IDs must be unique")

    for task in tasks:
        unknown = set(task.dependencies) - by_id.keys()
        if unknown:
            names = ", ".join(sorted(unknown))
            raise ValueError(f"Task '{task.id}' has unknown dependencies: {names}")
        if task.status not in {PENDING, SUCCEEDED, FAILED, BLOCKED}:
            raise ValueError(f"Task '{task.id}' has invalid initial status: {task.status}")

    remaining = {task.id for task in tasks if task.status == PENDING}
    while remaining:
        progressed = False
        for task in tasks:
            if task.id not in remaining:
                continue

            dependencies = [by_id[dependency] for dependency in task.dependencies]
            if any(dependent.status in {FAILED, BLOCKED} for dependent in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                if hook:
                    hook("blocked", task.id, {"reason": "parent_failed_or_blocked"}, None)
                progressed = True
                continue
            if not all(dependent.status == SUCCEEDED for dependent in dependencies):
                continue

            task.status = RUNNING
            if hook:
                hook("dispatch", task.id, {"action": bool(task.action)}, None)
            try:
                task.result = task.action() if task.action else None
            except Exception as error:
                task.status = FAILED
                task.result = error
                if hook:
                    hook("error", task.id, {"error": str(error)}, None)
            else:
                task.status = SUCCEEDED
                if hook:
                    hook("result", task.id, {"result": _safe(task.result)}, None)
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks

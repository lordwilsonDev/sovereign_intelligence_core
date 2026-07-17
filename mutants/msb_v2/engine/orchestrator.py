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


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


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
mutants_x_orchestrate__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_orchestrate__mutmut)
def orchestrate(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_orig(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_1(tasks: list[Task]) -> list[Task]:
    """Run ready tasks until the graph is complete.

    Tasks execute in input order when several are ready. A failed task is
    retained as ``failed``; every descendant is marked ``blocked`` and is not
    executed. Invalid or cyclic dependency graphs raise ``ValueError``.
    """

    if tasks:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_2(tasks: list[Task]) -> list[Task]:
    """Run ready tasks until the graph is complete.

    Tasks execute in input order when several are ready. A failed task is
    retained as ``failed``; every descendant is marked ``blocked`` and is not
    executed. Invalid or cyclic dependency graphs raise ``ValueError``.
    """

    if not tasks:
        return []

    by_id = None
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_3(tasks: list[Task]) -> list[Task]:
    """Run ready tasks until the graph is complete.

    Tasks execute in input order when several are ready. A failed task is
    retained as ``failed``; every descendant is marked ``blocked`` and is not
    executed. Invalid or cyclic dependency graphs raise ``ValueError``.
    """

    if not tasks:
        return []

    by_id = {task.id: task for task in tasks}
    if len(by_id) == len(tasks):
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_4(tasks: list[Task]) -> list[Task]:
    """Run ready tasks until the graph is complete.

    Tasks execute in input order when several are ready. A failed task is
    retained as ``failed``; every descendant is marked ``blocked`` and is not
    executed. Invalid or cyclic dependency graphs raise ``ValueError``.
    """

    if not tasks:
        return []

    by_id = {task.id: task for task in tasks}
    if len(by_id) != len(tasks):
        raise ValueError(None)

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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_5(tasks: list[Task]) -> list[Task]:
    """Run ready tasks until the graph is complete.

    Tasks execute in input order when several are ready. A failed task is
    retained as ``failed``; every descendant is marked ``blocked`` and is not
    executed. Invalid or cyclic dependency graphs raise ``ValueError``.
    """

    if not tasks:
        return []

    by_id = {task.id: task for task in tasks}
    if len(by_id) != len(tasks):
        raise ValueError("XXTask IDs must be uniqueXX")

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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_6(tasks: list[Task]) -> list[Task]:
    """Run ready tasks until the graph is complete.

    Tasks execute in input order when several are ready. A failed task is
    retained as ``failed``; every descendant is marked ``blocked`` and is not
    executed. Invalid or cyclic dependency graphs raise ``ValueError``.
    """

    if not tasks:
        return []

    by_id = {task.id: task for task in tasks}
    if len(by_id) != len(tasks):
        raise ValueError("task ids must be unique")

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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_7(tasks: list[Task]) -> list[Task]:
    """Run ready tasks until the graph is complete.

    Tasks execute in input order when several are ready. A failed task is
    retained as ``failed``; every descendant is marked ``blocked`` and is not
    executed. Invalid or cyclic dependency graphs raise ``ValueError``.
    """

    if not tasks:
        return []

    by_id = {task.id: task for task in tasks}
    if len(by_id) != len(tasks):
        raise ValueError("TASK IDS MUST BE UNIQUE")

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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_8(tasks: list[Task]) -> list[Task]:
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
        unknown = None
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_9(tasks: list[Task]) -> list[Task]:
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
        unknown = set(task.dependencies) + by_id.keys()
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_10(tasks: list[Task]) -> list[Task]:
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
        unknown = set(None) - by_id.keys()
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_11(tasks: list[Task]) -> list[Task]:
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
            names = None
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_12(tasks: list[Task]) -> list[Task]:
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
            names = ", ".join(None)
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_13(tasks: list[Task]) -> list[Task]:
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
            names = "XX, XX".join(sorted(unknown))
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_14(tasks: list[Task]) -> list[Task]:
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
            names = ", ".join(sorted(None))
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_15(tasks: list[Task]) -> list[Task]:
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
            raise ValueError(None)
        if task.status not in {PENDING, SUCCEEDED, FAILED, BLOCKED}:
            raise ValueError(f"Task '{task.id}' has invalid initial status: {task.status}")

    remaining = {task.id for task in tasks if task.status == PENDING}
    while remaining:
        progressed = False
        for task in tasks:
            if task.id not in remaining:
                continue

            dependencies = [by_id[dependency] for dependency in task.dependencies]
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_16(tasks: list[Task]) -> list[Task]:
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
        if task.status in {PENDING, SUCCEEDED, FAILED, BLOCKED}:
            raise ValueError(f"Task '{task.id}' has invalid initial status: {task.status}")

    remaining = {task.id for task in tasks if task.status == PENDING}
    while remaining:
        progressed = False
        for task in tasks:
            if task.id not in remaining:
                continue

            dependencies = [by_id[dependency] for dependency in task.dependencies]
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_17(tasks: list[Task]) -> list[Task]:
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
            raise ValueError(None)

    remaining = {task.id for task in tasks if task.status == PENDING}
    while remaining:
        progressed = False
        for task in tasks:
            if task.id not in remaining:
                continue

            dependencies = [by_id[dependency] for dependency in task.dependencies]
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_18(tasks: list[Task]) -> list[Task]:
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

    remaining = None
    while remaining:
        progressed = False
        for task in tasks:
            if task.id not in remaining:
                continue

            dependencies = [by_id[dependency] for dependency in task.dependencies]
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_19(tasks: list[Task]) -> list[Task]:
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

    remaining = {task.id for task in tasks if task.status != PENDING}
    while remaining:
        progressed = False
        for task in tasks:
            if task.id not in remaining:
                continue

            dependencies = [by_id[dependency] for dependency in task.dependencies]
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_20(tasks: list[Task]) -> list[Task]:
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
        progressed = None
        for task in tasks:
            if task.id not in remaining:
                continue

            dependencies = [by_id[dependency] for dependency in task.dependencies]
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_21(tasks: list[Task]) -> list[Task]:
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
        progressed = True
        for task in tasks:
            if task.id not in remaining:
                continue

            dependencies = [by_id[dependency] for dependency in task.dependencies]
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_22(tasks: list[Task]) -> list[Task]:
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
            if task.id in remaining:
                continue

            dependencies = [by_id[dependency] for dependency in task.dependencies]
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_23(tasks: list[Task]) -> list[Task]:
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
                break

            dependencies = [by_id[dependency] for dependency in task.dependencies]
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_24(tasks: list[Task]) -> list[Task]:
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

            dependencies = None
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_25(tasks: list[Task]) -> list[Task]:
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
            if any(None):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_26(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status not in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_27(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = None
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_28(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(None)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_29(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = None
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_30(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = False
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_31(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                break
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_32(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_33(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(None):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_34(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status != SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_35(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                break

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_36(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = None
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_37(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_38(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = None
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_39(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = None
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_40(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = None
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_41(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(None)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_42(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = None

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_43(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = False

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_44(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_45(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = None
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_46(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(None)
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_47(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = "XX, XX".join(sorted(remaining))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_48(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(None))
            raise ValueError(f"Circular or unsatisfiable task dependencies: {cycle}")

    return tasks


def x_orchestrate__mutmut_49(tasks: list[Task]) -> list[Task]:
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
            if any(dependency.status in {FAILED, BLOCKED} for dependency in dependencies):
                task.status = BLOCKED
                remaining.remove(task.id)
                progressed = True
                continue
            if not all(dependency.status == SUCCEEDED for dependency in dependencies):
                continue

            task.status = RUNNING
            try:
                task.result = task.action() if task.action else None
            except Exception as error:  # Task failure is workflow state, not a graph error.
                task.status = FAILED
                task.result = error
            else:
                task.status = SUCCEEDED
            remaining.remove(task.id)
            progressed = True

        if not progressed:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(None)

    return tasks

mutants_x_orchestrate__mutmut['_mutmut_orig'] = x_orchestrate__mutmut_orig # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_1'] = x_orchestrate__mutmut_1 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_2'] = x_orchestrate__mutmut_2 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_3'] = x_orchestrate__mutmut_3 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_4'] = x_orchestrate__mutmut_4 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_5'] = x_orchestrate__mutmut_5 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_6'] = x_orchestrate__mutmut_6 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_7'] = x_orchestrate__mutmut_7 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_8'] = x_orchestrate__mutmut_8 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_9'] = x_orchestrate__mutmut_9 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_10'] = x_orchestrate__mutmut_10 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_11'] = x_orchestrate__mutmut_11 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_12'] = x_orchestrate__mutmut_12 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_13'] = x_orchestrate__mutmut_13 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_14'] = x_orchestrate__mutmut_14 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_15'] = x_orchestrate__mutmut_15 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_16'] = x_orchestrate__mutmut_16 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_17'] = x_orchestrate__mutmut_17 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_18'] = x_orchestrate__mutmut_18 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_19'] = x_orchestrate__mutmut_19 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_20'] = x_orchestrate__mutmut_20 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_21'] = x_orchestrate__mutmut_21 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_22'] = x_orchestrate__mutmut_22 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_23'] = x_orchestrate__mutmut_23 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_24'] = x_orchestrate__mutmut_24 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_25'] = x_orchestrate__mutmut_25 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_26'] = x_orchestrate__mutmut_26 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_27'] = x_orchestrate__mutmut_27 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_28'] = x_orchestrate__mutmut_28 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_29'] = x_orchestrate__mutmut_29 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_30'] = x_orchestrate__mutmut_30 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_31'] = x_orchestrate__mutmut_31 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_32'] = x_orchestrate__mutmut_32 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_33'] = x_orchestrate__mutmut_33 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_34'] = x_orchestrate__mutmut_34 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_35'] = x_orchestrate__mutmut_35 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_36'] = x_orchestrate__mutmut_36 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_37'] = x_orchestrate__mutmut_37 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_38'] = x_orchestrate__mutmut_38 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_39'] = x_orchestrate__mutmut_39 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_40'] = x_orchestrate__mutmut_40 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_41'] = x_orchestrate__mutmut_41 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_42'] = x_orchestrate__mutmut_42 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_43'] = x_orchestrate__mutmut_43 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_44'] = x_orchestrate__mutmut_44 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_45'] = x_orchestrate__mutmut_45 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_46'] = x_orchestrate__mutmut_46 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_47'] = x_orchestrate__mutmut_47 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_48'] = x_orchestrate__mutmut_48 # type: ignore # mutmut generated
mutants_x_orchestrate__mutmut['x_orchestrate__mutmut_49'] = x_orchestrate__mutmut_49 # type: ignore # mutmut generated

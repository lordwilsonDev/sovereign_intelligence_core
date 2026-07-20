"""Structured task scopes and error fusion for SAR.

Phase 1: ``TaskScope`` tracks spawned child tasks; cancellation of the
parent cancels the entire subtree. ``SquadErrorFusion`` collects exceptions
from children under an ``ExceptionGroup``-like envelope.
"""

from __future__ import annotations

import threading
from typing import Any, Callable, Dict, List, Optional, TypeVar

from msb_v2.concurrency.cancellable import CancellableOutput, Cancelled, Done, is_cancelled

T = TypeVar("T")


class ScopeCancelled(Exception):
    def __init__(self, reason: Optional[str] = None) -> None:
        super().__init__(reason or "task_scope_cancelled")
        self.reason = reason


class _ChildTask:
    def __init__(self, name: str, run: Callable[..., Any]) -> None:
        self.name = name
        self._run = run
        self.cancelled = False
        self.error: Optional[Exception] = None
        self.result: Any = None
        self._done = threading.Event()

    def cancel(self) -> None:
        self.cancelled = True

    def set_result(self, result: Any) -> None:
        self.result = result
        self._done.set()

    def set_error(self, exc: Exception) -> None:
        self.error = exc
        self._done.set()

    def wait(self, timeout: Optional[float] = None) -> bool:
        return self._done.wait(timeout=timeout)


class TaskScope:
    """Minimal structured concurrency scope for SAR profiles/squads."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._children: Dict[str, _ChildTask] = {}
        self._children_lock = threading.Lock()
        self.cancelled = False
        self._cancel_token = threading.Event()
        self._local = threading.local()

    @property
    def cancel_token(self) -> threading.Event:
        return self._cancel_token

    def enter(self) -> None:
        self._local.scope = self

    def current(self) -> Optional["TaskScope"]:
        return getattr(self._local, "scope", None)

    def spawn(self, name: str, run: Callable[[], Any]) -> _ChildTask:
        with self._children_lock:
            if self.cancelled:
                raise ScopeCancelled(reason="parent_scope_cancelled")
            task = _ChildTask(name=name, run=run)
            self._children[name] = task

        def _target() -> None:
            try:
                if task.cancelled:
                    raise ScopeCancelled(reason="child_cancelled_before_start")
                result = run()
                if self._cancel_token.is_set() or task.cancelled:
                    task.set_error(ScopeCancelled(reason="cancelled_during_execution"))
                else:
                    task.set_result(result)
            except Exception as exc:
                task.set_error(exc)

        thread = threading.Thread(target=_target, daemon=True)
        thread.start()
        return task

    def cancel(self) -> None:
        with self._children_lock:
            self.cancelled = True
            self._cancel_token.set()
            for task in self._children.values():
                task.cancel()

    def wait_all(self, timeout: Optional[float] = None) -> Dict[str, _ChildTask]:
        with self._children_lock:
            tasks = list(self._children.values())
        for task in tasks:
            task.wait(timeout=timeout)
        return {task.name: task for task in tasks}

    def results(self) -> CancellableOutput[Dict[str, Any]]:
        tasks = self.wait_all()
        errors: List[tuple[str, Exception]] = []
        out: Dict[str, Any] = {}
        for name, task in tasks.items():
            if task.error is not None:
                errors.append((name, task.error))
            elif task.result is not None and not is_cancelled(task.result):
                out[name] = task.result.value if isinstance(task.result, Done) else task.result
        if errors:
            fusion = SquadErrorFusion(self.name)
            for name, exc in errors:
                fusion.add(f"{fusion.scope}.{name}", exc)
            return Cancelled(reason="squad_error_fusion", metadata={"fusion": fusion.to_dict()})
        return Done(out)


class SquadErrorFusion:
    """Collect exceptions from multiple child tasks in one structure."""

    def __init__(self, scope: str) -> None:
        self.scope = scope
        self._exceptions: Dict[str, Exception] = {}

    def add(self, task_id: str, exc: Exception) -> None:
        self._exceptions[task_id] = exc

    @property
    def errors(self) -> Dict[str, Exception]:
        return dict(self._exceptions)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scope": self.scope,
            "count": len(self._exceptions),
            "tasks": [
                {"task_id": task_id, "error": repr(exc)}
                for task_id, exc in self._exceptions.items()
            ],
        }

    def exception_group(self) -> ScopeCancelled:
        return ScopeCancelled(
            reason="squad_fusion",
        )

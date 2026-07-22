"""
O_FUSION: a universal error-fusion operator for structured concurrency.

Implements the three fusion policies in the paper's Section 2:

  - FIRST_WINS  : first failure propagates; the rest are
                  attached as suppressed exceptions on the primary.
  - AGGREGATE   : all failures are collected into a single ExceptionGroup.
  - TREE        : preserves which task raised which error, as a dict keyed
                  by task name.
"""

from __future__ import annotations

import asyncio
import enum
from typing import Any, Coroutine, Optional


class FusionPolicy(enum.Enum):
    FIRST_WINS = "first_wins"
    AGGREGATE = "aggregate"
    TREE = "tree"


class _ErrorClassification:
    __slots__ = (
        "error",
        "weight",
        "sovereign_alert",
        "reversible",
        "payload_type",
        "scope_source",
    )

    def __init__(
        self,
        error: BaseException,
        weight: float,
        sovereign_alert: bool,
        reversible: bool,
        payload_type: str,
        scope_source: bool = False,
    ) -> None:
        self.error = error
        self.weight = weight
        self.sovereign_alert = sovereign_alert
        self.reversible = reversible
        self.payload_type = payload_type
        self.scope_source = scope_source


class FusedError(Exception):
    """Composite error for policies that don't have a native Python type to lean on."""

    def __init__(self, errors: list[BaseException], policy: FusionPolicy):
        self.errors = errors
        self.policy = policy
        self.tree: dict[str, BaseException] = {}
        super().__init__(
            f"{len(errors)} error(s) fused under policy={policy.value}"
        )
        if errors:
            self.__cause__ = errors[0]


class Scope:
    """Structured-concurrency scope with a configurable O_FUSION policy."""

    def __init__(
        self,
        policy: FusionPolicy = FusionPolicy.AGGREGATE,
        cancel_on_error: bool = True,
    ):
        self.policy = policy
        self.cancel_on_error = cancel_on_error
        self._tasks: list[asyncio.Task] = []
        self._task_names: dict[asyncio.Task, str] = {}

    async def __aenter__(self) -> "Scope":
        return self

    def spawn(self, coro: Coroutine[Any, Any, Any], name: Optional[str] = None) -> asyncio.Task:
        task = asyncio.ensure_future(coro)
        self._tasks.append(task)
        self._task_names[task] = name or f"task-{len(self._tasks)}"
        return task

    def _cancel_all(self) -> None:
        for t in self._tasks:
            if not t.done():
                t.cancel()

    async def __aexit__(self, exc_type, exc, tb) -> bool:
        self._errors: list[BaseException] = []
        if exc is not None:
            self._errors.append(exc)
            if self.cancel_on_error:
                self._cancel_all()

        pending = set(self._tasks)
        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                if task.cancelled():
                    continue
                task_exc = task.exception()
                if task_exc is not None:
                    self._errors.append(task_exc)
                    if self.cancel_on_error:
                        for t in pending:
                            if not t.done():
                                t.cancel()

        if self._errors:
            raise self._fuse(self._errors) from None

        return False

    def _fuse(self, errors: list[BaseException]) -> BaseException:
        classified = self._classify_errors(errors)
        weighted = self._weight_errors(classified)
        return self._synthesize_fusion(weighted)

    def _classify_errors(self, errors: list[BaseException]) -> list[_ErrorClassification]:
        classified: list[_ErrorClassification] = []
        body_errors = [
            e for e in errors
            if getattr(e, "_scope_body_error", False)
        ]
        tree_errors = [
            e for e in errors
            if getattr(e, "_scope_task_error", False)
        ]
        for error in errors:
            payload_type = type(error).__name__
            sovereign_alert = False
            reversible = True
            scope_source = error in body_errors
            if isinstance(error, SystemExit | KeyboardInterrupt | MemoryError | OSError):
                sovereign_alert = True
                reversible = False
            elif isinstance(error, asyncio.CancelledError):
                reversible = False
            elif isinstance(error, (RuntimeError, ValueError, TypeError)):
                reversible = True
            classified.append(_ErrorClassification(
                error=error,
                weight=0.0,
                sovereign_alert=sovereign_alert,
                reversible=reversible,
                payload_type=payload_type,
                scope_source=scope_source,
            ))
        return classified

    def _weight_errors(self, classified: list[_ErrorClassification]) -> list[_ErrorClassification]:
        for item in classified:
            if item.sovereign_alert:
                item.weight = 1.0
                continue
            if item.scope_source:
                item.weight = max(item.weight, 0.8)
            if isinstance(item.error, asyncio.CancelledError):
                item.weight = max(item.weight, 0.1)
            elif isinstance(item.error, (RuntimeError, ValueError, TypeError)):
                item.weight = max(item.weight, 0.55)
            else:
                item.weight = max(item.weight, 0.25)
        return classified

    def _synthesize_fusion(self, weighted: list[_ErrorClassification]) -> BaseException:
        primary = max(weighted, key=lambda item: item.weight)
        fused = [item.error for item in weighted if item.error is not primary.error]
        policy = self.policy
        if policy is FusionPolicy.FIRST_WINS:
            if fused:
                primary.error.__notes__ = getattr(primary.error, "__notes__", [])
                for error in fused:
                    primary.error.__notes__.append(
                        f"suppressed: {type(error).__name__}: {error}"
                    )
                primary.error.__suppressed__ = fused
            return primary.error

        if policy is FusionPolicy.AGGREGATE:
            return ExceptionGroup("O_FUSION: multiple task failures", [item.error for item in weighted])

        if policy is FusionPolicy.TREE:
            err = FusedError([item.error for item in weighted], policy)
            for task, name in self._task_names.items():
                if task.done() and not task.cancelled():
                    task_exc = task.exception()
                    if task_exc is not None:
                        err.tree[name] = task_exc
            body_errors = [item.error for item in weighted if item.scope_source]
            for i, error in enumerate(body_errors):
                err.tree.setdefault(f"__scope__[{i}]", error)
            return err

        raise ValueError(f"Unknown fusion policy: {policy}")

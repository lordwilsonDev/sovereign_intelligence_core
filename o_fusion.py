"""
O_FUSION: a universal error-fusion operator for structured concurrency.

Implements the three fusion policies surveyed in the paper's Section 2:

  - FIRST_WINS  : Kotlin/Java style. First failure propagates; the rest are
                  attached as suppressed exceptions on the primary.
  - AGGREGATE   : Trio/Python 3.11+ style. All failures are collected into
                  a single ExceptionGroup, catchable with `except*`.
  - TREE        : preserves which task raised which error, as a dict keyed
                  by task name -- useful when you need to know *which*
                  sibling failed, not just that something did.

The `Scope` class is a structured-concurrency primitive: no task spawned
inside it can outlive it (mirrors Trio's nursery / Kotlin's coroutineScope).
On the first failure, siblings are cancelled (cooperative cancellation --
see the paper's Section 9 on scheduler fairness for why this requires
tasks to actually hit an await point to notice).
"""

from __future__ import annotations

import asyncio
import enum
from typing import Any, Coroutine, Optional


class FusionPolicy(enum.Enum):
    FIRST_WINS = "first_wins"
    AGGREGATE = "aggregate"
    TREE = "tree"


class FusedError(Exception):
    """Composite error for policies that don't have a native Python type
    to lean on (TREE). Carries every underlying failure."""

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
    """A structured-concurrency scope with a configurable O_FUSION policy.

    Usage:
        async with Scope(policy=FusionPolicy.AGGREGATE) as scope:
            scope.spawn(worker_a(), name="a")
            scope.spawn(worker_b(), name="b")
        # by the time we're here, either both succeeded, or a fused
        # error has been raised representing every failure.
    """

    def __init__(
        self,
        policy: FusionPolicy = FusionPolicy.AGGREGATE,
        cancel_on_error: bool = True,
    ):
        self.policy = policy
        self.cancel_on_error = cancel_on_error
        self._tasks: list[asyncio.Task] = []
        self._task_names: dict[asyncio.Task, str] = {}
        self._errors: list[BaseException] = []

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
        # A failure in the `async with` body itself counts as a failure
        # of the scope, same as a spawned child failing.
        if exc is not None:
            self._errors.append(exc)
            if self.cancel_on_error:
                self._cancel_all()

        # Use an incremental FIRST_COMPLETED wait rather than gather(): gather
        # only reports results once *every* task has finished, so cancelling
        # a sibling in response to an early failure would happen too late to
        # matter (e.g. a sibling asleep for 5s would still sleep the full 5s).
        # Waiting on FIRST_COMPLETED lets us cancel remaining siblings the
        # instant any one task fails.
        pending = set(self._tasks)
        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                if task.cancelled():
                    # Expected: this task was cancelled because a sibling
                    # failed. Not itself a fusion-worthy error.
                    continue
                task_exc = task.exception()
                if task_exc is not None:
                    self._errors.append(task_exc)
                    if self.cancel_on_error:
                        for t in pending:
                            if not t.done():
                                t.cancel()

        if self._errors:
            raise self._fuse() from None

        return False

    def _fuse(self) -> BaseException:
        if self.policy is FusionPolicy.FIRST_WINS:
            primary, *rest = self._errors
            if rest:
                primary.__notes__ = getattr(primary, "__notes__", [])
                for e in rest:
                    primary.__notes__.append(f"suppressed: {type(e).__name__}: {e}")
                primary.__suppressed__ = rest  # non-standard, but inspectable
            return primary

        if self.policy is FusionPolicy.AGGREGATE:
            return ExceptionGroup("O_FUSION: multiple task failures", self._errors)

        if self.policy is FusionPolicy.TREE:
            err = FusedError(self._errors, self.policy)
            for task, name in self._task_names.items():
                if task.done() and not task.cancelled():
                    task_exc = task.exception()
                    if task_exc is not None:
                        err.tree[name] = task_exc
                # cancelled tasks contribute nothing to the tree -- being
                # cancelled isn't a failure of that task, it's fallout
            # Body-level exception (not from a named task) goes in under "__scope__"
            if exc_only_from_body := [e for e in self._errors if e not in err.tree.values()]:
                for i, e in enumerate(exc_only_from_body):
                    err.tree.setdefault(f"__scope__[{i}]", e)
            return err

        raise ValueError(f"Unknown fusion policy: {self.policy}")

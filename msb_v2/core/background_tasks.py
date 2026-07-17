from __future__ import annotations

import asyncio
import logging
from collections.abc import Coroutine
from typing import Any

logger = logging.getLogger(__name__)


class BackgroundTaskRegistry:
    def __init__(self, name: str = "background") -> None:
        self._name = name
        self._tasks: set[asyncio.Task[Any]] = set()

    def spawn(self, coro: Coroutine[Any, Any, Any], *, label: str | None = None) -> asyncio.Task[Any] | None:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            coro.close()
            logger.debug("BackgroundTaskRegistry[%s]: no running loop, cannot spawn %s", self._name, label or "task")
            return None

        task = asyncio.create_task(coro)
        self._tasks.add(task)
        task.add_done_callback(self._on_done)
        if label:
            try:
                task.set_name(label)
            except Exception:
                pass
        return task

    def _on_done(self, task: asyncio.Task[Any]) -> None:
        self._tasks.discard(task)
        if task.cancelled():
            return
        exc = task.exception()
        if exc is not None:
            logger.error(
                "BackgroundTaskRegistry[%s]: task %s failed: %s",
                self._name,
                task.get_name(),
                exc,
                exc_info=exc,
            )

    async def drain(self, timeout: float | None = None) -> None:
        if not self._tasks:
            return
        pending = list(self._tasks)
        logger.debug("BackgroundTaskRegistry[%s]: draining %d task(s)", self._name, len(pending))
        _, still_pending = await asyncio.wait(pending, timeout=timeout)
        if still_pending:
            logger.warning(
                "BackgroundTaskRegistry[%s]: %d task(s) did not finish within %ss",
                self._name,
                len(still_pending),
                timeout,
            )

    @property
    def pending_count(self) -> int:
        return len(self._tasks)

    def __len__(self) -> int:
        return len(self._tasks)

from __future__ import annotations

import logging
import threading
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)


class BackgroundTaskRegistry:
    def __init__(self, name: str = "background") -> None:
        self._name = name
        self._async_tasks: set[Any] = set()
        self._threads: list[threading.Thread] = []
        self._lock = threading.Lock()

    def spawn(self, coro: Any, *, label: str | None = None) -> Any | None:
        try:
            import asyncio  # noqa: F401
            loop = asyncio.get_running_loop()
        except Exception:
            logger.debug("BackgroundTaskRegistry[%s]: no running loop, cannot spawn %s", self._name, label or "task")
            return None
        try:
            task = loop.create_task(coro)
            self._async_tasks.add(task)
            task.add_done_callback(lambda t: self._async_tasks.discard(t))
            if label:
                try:
                    task.set_name(label)
                except Exception:
                    pass
            return task
        except Exception as exc:
            logger.debug("BackgroundTaskRegistry[%s]: spawn failed: %s", self._name, exc)
            return None

    def register_thread(self, target: Callable[[], None], *, interval: float = 1.0, label: str | None = None) -> threading.Thread:
        stop_event = threading.Event()

        def _loop() -> None:
            while not stop_event.wait(interval):
                try:
                    target()
                except Exception as exc:
                    logger.debug("BackgroundTaskRegistry[%s]: thread %s error: %s", self._name, label or target, exc)

        thread = threading.Thread(target=_loop, daemon=True, name=label or f"{self._name}-thread")
        with self._lock:
            self._threads.append((thread, stop_event))
        thread.start()
        logger.debug("BackgroundTaskRegistry[%s]: registered thread %s", self._name, thread.name)
        return thread

    def stop_all_threads(self, *, timeout: float = 2.0) -> None:
        with self._lock:
            threads = list(self._threads)
        for thread, stop_event in threads:
            stop_event.set()
            if thread.is_alive():
                thread.join(timeout=timeout)

    @property
    def pending_count(self) -> int:
        return len(self)

    def __len__(self) -> int:
        return len(self._async_tasks) + len(self._threads)

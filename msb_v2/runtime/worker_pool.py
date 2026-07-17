from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from queue import Queue
from typing import Any, Callable, Dict, Optional


@dataclass
class WorkItem:
    job_id: str
    func: Callable[..., Any]
    args: tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    finished_at: Optional[float] = None
    error: Optional[BaseException] = None
    result: Any = None


class WorkerPool:
    def __init__(self, concurrency: int = 4) -> None:
        if concurrency < 1:
            raise ValueError("concurrency must be >= 1")
        self.concurrency = concurrency
        self._queue: Queue[Optional[WorkItem]] = Queue()
        self._workers: list[threading.Thread] = []
        self._lock = threading.Lock()
        self._status = {
            "concurrency": concurrency,
            "active": 0,
            "idle": concurrency,
            "queue_size": 0,
            "completed": 0,
            "errors": 0,
        }
        self._running = False
        self._stop_event = threading.Event()

    def start(self) -> None:
        with self._lock:
            if self._running:
                return
            self._running = True
            for _ in range(self.concurrency):
                worker = threading.Thread(target=self._worker_loop, daemon=True)
                worker.start()
                self._workers.append(worker)

    def stop(self, *, wait: bool = True) -> None:
        self._stop_event.set()
        for _ in self._workers:
            self._queue.put(None)
        if wait:
            for worker in self._workers:
                worker.join(timeout=2.0)
        with self._lock:
            self._running = False
            self._workers.clear()

    def submit(self, job_id: str, func: Callable[..., Any], *args: Any, **kwargs: Any) -> WorkItem:
        item = WorkItem(job_id=job_id, func=func, args=args, kwargs=kwargs)
        self._queue.put(item)
        with self._lock:
            self._status["queue_size"] = self._queue.qsize()
        return item

    def submit_and_wait(self, job_id: str, func: Callable[..., Any], *args: Any, **kwargs: Any) -> WorkItem:
        item = self.submit(job_id, func, *args, **kwargs)
        item.future = getattr(self, "_future", None)
        timeout = 30.0
        start = time.time()
        while item.finished_at is None and (time.time() - start) < timeout:
            time.sleep(0.01)
        return item

    def status(self) -> Dict[str, Any]:
        with self._lock:
            return dict(self._status)

    def _worker_loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                item = self._queue.get(timeout=0.5)
            except Exception:
                continue
            if item is None:
                self._queue.task_done()
                break
            with self._lock:
                self._status["idle"] -= 1
                self._status["active"] += 1
                self._status["queue_size"] = self._queue.qsize()
                item.started_at = time.time()
            try:
                item.result = item.func(*item.args, **item.kwargs)
                with self._lock:
                    self._status["completed"] += 1
            except BaseException as exc:  # pragma: no cover - surfaced via item.error
                item.error = exc
                with self._lock:
                    self._status["errors"] += 1
            finally:
                item.finished_at = time.time()
                with self._lock:
                    self._status["active"] -= 1
                    self._status["idle"] += 1
                    self._status["queue_size"] = self._queue.qsize()
                self._queue.task_done()

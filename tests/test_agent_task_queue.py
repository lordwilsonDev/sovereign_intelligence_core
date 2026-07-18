from __future__ import annotations

import threading
import time

import pytest

from msb_v2.agent.task_queue import TaskPriority, TaskQueue


def test_completion_status_is_observable() -> None:
    q = TaskQueue(max_concurrent=1)
    q.start()
    tid = q.submit("task-1", priority=TaskPriority.NORMAL)
    status = q.wait_completed(tid, timeout=2.0)
    assert status is not None
    assert status["status"] == "completed"
    assert status["result"] == "done"
    q.stop()


def test_running_state_observable_before_completion() -> None:
    q = TaskQueue(max_concurrent=1)
    blocker = threading.Event()

    original = q._resolve

    def resolve(goal: str, cancel_flag=None) -> str:
        blocker.wait(timeout=10)
        return "done"

    q._resolve = resolve
    q.start()
    tid = q.submit("blocked")
    try:
        assert q.wait_running(tid, timeout=1.0) is True
        status = q.status(tid)
        assert status is not None
        assert status["status"] == "running"
    finally:
        blocker.set()
        q.stop()
        q._resolve = original


def test_queue_does_not_advance_cancelled_task() -> None:
    q = TaskQueue(max_concurrent=1)
    blocker = threading.Event()

    original = q._resolve

    def resolve(goal: str, cancel_flag=None) -> str:
        blocker.wait(timeout=10)
        return "done"

    q._resolve = resolve
    q.start()
    tid = q.submit("will-cancel")
    assert q.wait_running(tid, timeout=1.0) is True
    assert q.cancel(tid) is True
    status = q.status(tid)
    assert status is not None
    assert status["status"] == "cancelled"
    blocker.set()
    q.stop()
    q._resolve = original


def test_no_completed_before_work_done() -> None:
    q = TaskQueue(max_concurrent=1)
    blocker = threading.Event()
    original = q._resolve

    def resolve(goal: str, cancel_flag=None) -> str:
        blocker.wait(timeout=10)
        return "done"

    q._resolve = resolve
    q.start()
    tid = q.submit("delayed")
    assert q.wait_running(tid, timeout=1.0) is True
    status = q.status(tid)
    assert status is not None
    assert status["status"] == "running"
    assert status["result"] is None
    blocker.set()
    q.stop()
    q._resolve = original

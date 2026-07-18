from __future__ import annotations

import threading

from msb_v2.agent.task_queue import TaskPriority, TaskQueue


def test_queue_submit_and_status() -> None:
    q = TaskQueue()
    q.start()
    tid = q.submit("hello", priority=TaskPriority.HIGH)
    s = q.get_status(tid)
    assert s is not None
    assert s["status"] == "pending"
    assert s["priority"] == "high"
    q.stop()


def test_queue_cancel() -> None:
    q = TaskQueue()
    q.start()
    tid = q.submit("bye")
    ok = q.cancel(tid)
    assert ok is True
    s = q.get_status(tid)
    assert s["status"] == "cancelled"
    q.stop()

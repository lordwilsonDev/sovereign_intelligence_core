from __future__ import annotations

from msb_v2.aura.dlq import DeadLetterQueue


def test_dlq_enqueue_and_snapshot() -> None:
    dlq = DeadLetterQueue(maxlen=5)
    entry = dlq.enqueue({"task": "t1"}, reason="timeout")
    assert entry.entry_id == "dlq-1"
    assert entry.reason == "timeout"
    snap = dlq.snapshot()
    assert len(snap) == 1
    assert snap[0]["payload"] == {"task": "t1"}


def test_dlq_drain_removes_items() -> None:
    dlq = DeadLetterQueue(maxlen=5)
    dlq.enqueue({"task": "t1"})
    dlq.enqueue({"task": "t2"})
    assert len(dlq) == 2
    drained = dlq.drain(limit=1)
    assert len(drained) == 1
    assert len(dlq) == 1


def test_dlq_maxlen_drops_oldest() -> None:
    dlq = DeadLetterQueue(maxlen=2)
    dlq.enqueue({"task": "t1"})
    dlq.enqueue({"task": "t2"})
    dlq.enqueue({"task": "t3"})
    assert len(dlq) == 2
    snap = dlq.snapshot()
    assert snap[0]["payload"] == {"task": "t2"}
    assert snap[1]["payload"] == {"task": "t3"}

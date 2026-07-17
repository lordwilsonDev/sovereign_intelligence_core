from __future__ import annotations

import threading
import time
from pathlib import Path

from msb_v2.runtime.config import RuntimeConfig
from msb_v2.runtime.context import RuntimeContext
from msb_v2.runtime.capabilities import CapabilityEvent
from msb_v2.runtime.event_log import PersistentEventLog
from msb_v2.runtime.health import HealthManager
from msb_v2.runtime.resources import ResourceManager
from msb_v2.runtime.worker_pool import WorkerPool


def test_persistent_event_log_writes_and_queries(tmp_path: Path) -> None:
    db_path = str(tmp_path / "events.sqlite")
    log = PersistentEventLog(db_path, flush_interval=0.01, batch_size=10)
    log.start()
    try:
        log.append("test.topic", "unit", {"key": "value"})
        time.sleep(0.05)
        rows = log.query(limit=10)
        assert len(rows) == 1
        assert rows[0]["event_type"] == "test.topic"
        assert rows[0]["source"] == "unit"
        assert "key" in rows[0]["payload"]
    finally:
        log.stop()


def test_persistent_event_log_stop_flushes_remaining(tmp_path: Path) -> None:
    db_path = str(tmp_path / "events2.sqlite")
    log = PersistentEventLog(db_path, flush_interval=0.05, batch_size=100)
    log.start()
    log.append("flush.test", "unit", {"batch": "end"})
    time.sleep(0.01)
    log.stop()
    rows = log.query(limit=10)
    assert len(rows) == 1
    assert rows[0]["event_type"] == "flush.test"


def test_worker_pool_handles_more_jobs_than_concurrency() -> None:
    pool = WorkerPool(concurrency=2)
    pool.start()
    try:
        def slow_job(ident: str) -> str:
            time.sleep(0.05)
            return ident

        for i in range(5):
            pool.submit(f"job-{i}", slow_job, f"job-{i}")

        deadline = time.time() + 2.0
        while (pool.status()["queue_size"] > 0 or pool.status()["active"] > 0) and time.time() < deadline:
            time.sleep(0.05)

        status = pool.status()
        assert status["completed"] == 5
        assert status["errors"] == 0
        assert status["queue_size"] == 0
    finally:
        pool.stop()


def test_worker_pool_status_updates() -> None:
    pool = WorkerPool(concurrency=1)
    pool.start()
    try:
        barrier = threading.Barrier(2)
        pool.submit("sync", barrier.wait)

        deadline = time.time() + 0.5
        while pool.status()["active"] < 1 and time.time() < deadline:
            time.sleep(0.05)

        status = pool.status()
        assert status["active"] >= 1
        assert status["idle"] == 0
    finally:
        pool.stop()


def test_runtime_context_summary_contains_worker_and_log(tmp_path: Path) -> None:
    db_path = str(tmp_path / "runtime_status.sqlite")
    context = RuntimeContext(RuntimeConfig(event_log_path=db_path, worker_concurrency=2, event_log_flush_interval=0.01, event_log_batch_size=10))
    context.event_log.start()
    context.workers.start()
    try:
        context.event_log.append("status.test", "unit", {"hello": "world"})
        time.sleep(0.05)
        summary = context.summary()
        assert summary["app"] == "msb-v2"
        assert "worker_pool" in summary
        assert summary["event_log"]["enabled"] is True
        assert len(summary["event_log"]["last_events"]) >= 1
    finally:
        context.stop()


def test_runtime_config_includes_event_and_worker_fields() -> None:
    cfg = RuntimeConfig(
        event_log_path="./runtime_events.db",
        event_log_flush_interval=0.2,
        event_log_batch_size=50,
        worker_concurrency=8,
    )
    data = cfg.to_dict()
    assert data["event_log_path"] == "./runtime_events.db"
    assert data["event_log_flush_interval"] == 0.2
    assert data["event_log_batch_size"] == 50
    assert data["worker_concurrency"] == 8


def test_runtime_context_replay_returns_events(tmp_path: Path) -> None:
    db_path = str(tmp_path / "replay.sqlite")
    context = RuntimeContext(RuntimeConfig(event_log_path=db_path, event_log_flush_interval=0.01, event_log_batch_size=10))
    context.event_log.start()
    context.event_log.append("replay.test", "unit", {"step": 1})
    time.sleep(0.05)
    replayed = context.replay_events(limit=10)
    assert len(replayed) == 1
    assert replayed[0]["event_type"] == "replay.test"
    context.stop()


def test_health_manager_records_and_surfaces_latest() -> None:
    health = HealthManager(check_interval=0.01)
    health.record("ok", detail="booted", module="runtime")
    latest = health.latest()
    assert latest["status"] == "ok"
    assert latest["detail"] == "booted"
    assert latest["metadata"]["module"] == "runtime"
    summary = health.summary()
    assert "health" in summary
    assert summary["capabilities"]["event_log"] == "enabled"


def test_resource_manager_acquire_release_and_snapshot() -> None:
    resources = ResourceManager(max_memory_mb=100)
    assert resources.acquire("job-1", estimated_mb=25) is True
    snapshot = resources.snapshot()
    assert snapshot["active_jobs"] == 1
    assert snapshot["reserved_memory_mb"] == 25
    resources.release("job-1")
    assert resources.snapshot()["active_jobs"] == 0


def test_runtime_context_record_capability_event() -> None:
    context = RuntimeContext()
    event = context.record_capability(CapabilityEvent(module="demo", capability="plan", status="skipped", detail="no model"))
    assert event.status == "skipped"
    latest = context.health.latest()
    assert latest["metadata"]["capability"] == "plan"

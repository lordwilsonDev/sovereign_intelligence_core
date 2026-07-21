from __future__ import annotations

import json
from pathlib import Path


def pytest_addoption(parser: Any) -> None:
    parser.addoption("--anomaly-low", action="store_true")
from typing import Any, Dict

import pytest

from msb_v2.scth.db import TelemetryStore, _hash_row
from msb_v2.scth.ingestion import ingest_event
from msb_v2.scth.metrics import record_run, JOB_RUNS_TOTAL
from msb_v2.scth.query import QueryEngine
from msb_v2.scth.anomaly import AnomalyDetector


@pytest.fixture()
def store(tmp_path: Path) -> TelemetryStore:
    db = tmp_path / "scth_telemetry.db"
    return TelemetryStore(db_path=db)


@pytest.fixture()
def query_engine(store: TelemetryStore) -> QueryEngine:
    return QueryEngine(store=store)


def test_append_run_and_query(store: TelemetryStore) -> None:
    event = {
        "run_id": "run-1",
        "job_id": "build",
        "status": "SUCCESS",
        "timestamp_start": "2026-01-01T00:00:00+00:00",
        "timestamp_end": "2026-01-01T00:00:01+00:00",
        "duration_ms": 1000,
        "custom_metrics": {"tests_passed": 10},
        "resource_usage": {"cpu_percent": 2.5, "memory_mb": 120.0},
    }
    store.append_run(event)
    run = store.get_run("run-1")
    assert run["status"] == "SUCCESS"
    assert run["cpu_percent"] == 2.5
    assert run["memory_mb"] == 120.0
    result = store.query_runs(job_id="build")
    assert result["count"] == 1
    assert result["runs"][0]["custom_metrics"]["tests_passed"] == 10


def test_ingest_records_metrics(store: TelemetryStore) -> None:
    event = {"run_id": "run-metrics", "job_id": "heartbeat", "status": "SUCCESS", "duration_ms": 500}
    ingest_event(event, store=store)
    runs = store.query_runs(job_id="heartbeat")
    assert runs["count"] == 1


def test_anomaly_detector() -> None:
    runs = [
        {"run_id": "r1", "job_id": "j1", "status": "SUCCESS", "duration_ms": 1000, "cpu_percent": 2, "memory_mb": 100, "ingestion_ts": "2026-01-01T00:00:00+00:00"},
        {"run_id": "r2", "job_id": "j1", "status": "SUCCESS", "duration_ms": 1000, "cpu_percent": 2, "memory_mb": 100, "ingestion_ts": "2026-01-01T00:00:01+00:00"},
        {"run_id": "r3", "job_id": "j1", "status": "FAILED", "duration_ms": 1000, "cpu_percent": 2, "memory_mb": 100, "ingestion_ts": "2026-01-01T00:00:02+00:00"},
        {"run_id": "r4", "job_id": "j1", "status": "FAILED", "duration_ms": 1000, "cpu_percent": 2, "memory_mb": 100, "ingestion_ts": "2026-01-01T00:00:03+00:00"},
        {"run_id": "r5", "job_id": "j1", "status": "FAILED", "duration_ms": 1000, "cpu_percent": 2, "memory_mb": 100, "ingestion_ts": "2026-01-01T00:00:04+00:00"},
        {"run_id": "r6", "job_id": "j1", "status": "SUCCESS", "duration_ms": 1000, "cpu_percent": 2, "memory_mb": 100, "ingestion_ts": "2026-01-01T00:00:05+00:00"},
    ]
    anomalies = AnomalyDetector().detect(runs)
    assert any(item.kind == "failure_cluster" for item in anomalies)
    assert any(item.kind == "memory_creep" for item in anomalies) is False


def test_chain_validation(store: TelemetryStore) -> None:
    store.append_run({"run_id": "run-a", "job_id": "a", "status": "SUCCESS"})
    store.append_run({"run_id": "run-b", "job_id": "a", "status": "FAILED"})
    validation = store.validate_chain()
    assert validation["valid"] is True
    assert validation["chain_length"] == 2

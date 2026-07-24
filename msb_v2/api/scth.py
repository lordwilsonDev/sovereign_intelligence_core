from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import APIRouter, BackgroundTasks, Request
from pydantic import BaseModel

from msb_v2.scth.db import TelemetryStore
from msb_v2.scth.ingestion import ingest_event
from msb_v2.scth.metrics import record_run, bump_ingestion_error
from msb_v2.scth.query import QueryEngine
from msb_v2.scth.retention import apply_retention

router = APIRouter()
_store = TelemetryStore(db_path=Path(os.getenv("SCTH_DB_PATH", "data/scth_telemetry.db")))
_queries = QueryEngine(_store)


class EventIn(BaseModel):
    job_id: str
    run_id: str
    timestamp_start: Optional[str] = None
    timestamp_end: Optional[str] = None
    status: str
    duration_ms: Optional[int] = None
    exit_code: Optional[int] = None
    stdout_tail: Optional[str] = None
    stderr_tail: Optional[str] = None
    resource_usage: Optional[Dict[str, Any]] = None
    cpu_percent: Optional[float] = None
    memory_mb: Optional[float] = None
    custom_metrics: Optional[Dict[str, Any]] = None
    quarantine: Optional[int] = 0


@router.post("/ingest")
def scth_ingest(event: EventIn, request: Request) -> Dict[str, Any]:
    payload = event.model_dump()
    try:
        record_run(payload)
        result = ingest_event(payload)
    except Exception:
        bump_ingestion_error()
        raise
    return result


@router.get("/runs")
def scth_runs(
    job_id: Optional[str] = None,
    status: Optional[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    limit: int = 50,
) -> Dict[str, Any]:
    return _queries.query_runs(job_id=job_id, status=status, start=start, end=end, limit=limit)


@router.get("/summary")
def scth_summary(job_id: Optional[str] = None, period: str = "daily") -> Dict[str, Any]:
    return _queries.summaries(job_id=job_id, period=period)


@router.get("/anomalies")
def scth_anomalies(
    job_id: Optional[str] = None,
    limit: int = 50,
) -> Dict[str, Any]:
    return _queries.anomalies(job_id=job_id, limit=limit)


@router.post("/query")
def scth_query(payload: Dict[str, Any]) -> Dict[str, Any]:
    return _queries.run_anomaly_detection(job_id=payload.get("job_id"))


@router.get("/status")
def scth_status() -> Dict[str, Any]:
    status = _queries.status()
    chain = _store.validate_chain()
    status["merkle_chain"] = chain
    return status


@router.post("/retention")
def scth_retention(background_tasks: BackgroundTasks) -> Dict[str, Any]:
    result = _apply_retention()
    return result


def _apply_retention() -> Dict[str, Any]:
    return apply_retention(_store)

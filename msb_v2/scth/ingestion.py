from __future__ import annotations

from typing import Any, Dict

from msb_v2.scth.anomaly import AnomalyDetector
from msb_v2.scth.db import TelemetryStore


def ingest_event(event: Dict[str, Any], store: TelemetryStore | None = None) -> Dict[str, Any]:
    if store is None:
        store = TelemetryStore()
    validated = dict(event)
    status = str(validated.get("status", "")).upper()
    if status == "FAILED":
        validated["quarantine"] = 1
    result = store.append_run(validated)
    _detect_and_store_anomalies(store, validated)
    return result


def _detect_and_store_anomalies(store: TelemetryStore, event: Dict[str, Any]) -> None:
    try:
        job_id = event.get("job_id")
        if not job_id:
            return
        rows = store.query_runs(job_id=job_id, limit=100).get("runs", [])
        anomalies = AnomalyDetector().detect(rows)
        for anomaly in anomalies:
            store.append_anomaly(
                anomaly_id=f"{job_id}:{anomaly.kind}:{event.get('run_id','')}",
                job_id=job_id,
                kind=anomaly.kind,
                detail=anomaly.detail,
                run_id=event.get("run_id"),
            )
    except Exception:
        pass

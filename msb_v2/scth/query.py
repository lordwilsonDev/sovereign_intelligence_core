from __future__ import annotations

from typing import Any, Dict, List

from msb_v2.scth.db import TelemetryStore
from msb_v2.scth.anomaly import AnomalyDetector


class QueryEngine:
    def __init__(self, store: TelemetryStore) -> None:
        self._store = store
        self._detector = AnomalyDetector()

    def query_runs(
        self,
        job_id: str | None = None,
        status: str | None = None,
        start: str | None = None,
        end: str | None = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        return self._store.query_runs(job_id=job_id, status=status, start=start, end=end, limit=limit)

    def anomalies(self, job_id: str | None = None, limit: int = 50) -> Dict[str, Any]:
        # Lazy import to avoid circulars if any.
        from msb_v2.scth.db import TelemetryStore
        store = self._store
        cursor = store._conn.cursor()
        if job_id:
            cursor.execute("SELECT * FROM anomalies WHERE job_id = ? ORDER BY detected_at DESC LIMIT ?", (job_id, limit))
        else:
            cursor.execute("SELECT * FROM anomalies ORDER BY detected_at DESC LIMIT ?", (limit,))
        rows = [dict(row) for row in cursor.fetchall()]
        return {"anomalies": rows, "count": len(rows)}

    def summaries(self, job_id: str | None = None, period: str = "daily") -> Dict[str, Any]:
        rows = self._store.query_runs(job_id=job_id, limit=1000)["runs"]
        bucket: Dict[str, Dict[str, Any]] = {}
        for row in rows:
            ts = row.get("ingestion_ts") or row.get("timestamp_start") or ""
            if not ts:
                continue
            key = ts[:10] if period == "daily" else ts[:7]
            bucket.setdefault(key, {"count": 0, "success": 0, "failed": 0, "durations": []})
            bucket[key]["count"] += 1
            if str(row.get("status")) == "SUCCESS":
                bucket[key]["success"] += 1
            else:
                bucket[key]["failed"] += 1
            bucket[key]["durations"].append(float(row.get("duration_ms") or 0) / 1000.0)
        summaries = []
        for key, values in sorted(bucket.items()):
            durations = values["durations"]
            summaries.append(
                {
                    "period": key,
                    "count": values["count"],
                    "success": values["success"],
                    "failed": values["failed"],
                    "avg_duration_seconds": (sum(durations) / len(durations)) if durations else None,
                    "max_duration_seconds": max(durations) if durations else None,
                }
            )
        return {"summaries": summaries, "count": len(summaries)}

    def run_anomaly_detection(self, job_id: str | None = None) -> Dict[str, Any]:
        rows = self._store.query_runs(job_id=job_id, limit=1000)["runs"]
        anomalies = self._detector.detect(rows)
        return {"anomalies": [anomaly.__dict__ for anomaly in anomalies], "count": len(anomalies)}

    def status(self) -> Dict[str, Any]:
        db_size = self._store.db_path().stat().st_size if self._store.db_path().exists() else 0
        rows = self._store.query_runs(limit=1000)["runs"]
        ingestion_rate = len(rows)
        return {"db_size_bytes": db_size, "recent_ingestion_count": ingestion_rate}

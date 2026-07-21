from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


DEFAULT_DB_PATH = Path(os.getenv("SCTH_DB_PATH", "data/scth_telemetry.db"))
DEFAULT_RETENTION_DAYS = int(os.getenv("SCTH_RETENTION_DAYS", "90"))


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _hash_row(payload: Dict[str, Any], prev_hash: Optional[str]) -> str:
    base = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256((base + (prev_hash or "")).encode()).hexdigest()


class TelemetryStore:
    def __init__(
        self,
        db_path: Path = DEFAULT_DB_PATH,
        retention_days: int = DEFAULT_RETENTION_DAYS,
    ) -> None:
        self._db_path = db_path
        self._retention_days = retention_days
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self._db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._initialize()

    def _initialize(self) -> None:
        cursor = self._conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_runs (
            run_id TEXT PRIMARY KEY,
            job_id TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp_start TEXT,
            timestamp_end TEXT,
            duration_ms INTEGER,
            exit_code INTEGER,
            stdout_tail TEXT,
            stderr_tail TEXT,
            cpu_percent REAL,
            memory_mb REAL,
            custom_metrics TEXT,
            quarantine INTEGER DEFAULT 0,
            ingestion_hash TEXT NOT NULL,
            ingestion_ts TEXT NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS merkle_chain (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            prev_hash TEXT,
            payload_json TEXT NOT NULL,
            row_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS anomalies (
            anomaly_id TEXT PRIMARY KEY,
            job_id TEXT NOT NULL,
            detected_at TEXT NOT NULL,
            kind TEXT NOT NULL,
            detail TEXT,
            run_id TEXT
        )
        """)
        self._conn.commit()

    def _last_row_hash(self) -> Optional[str]:
        cursor = self._conn.cursor()
        cursor.execute("SELECT row_hash FROM merkle_chain ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        return row[0] if row else None

    def append_run(self, event: Dict[str, Any]) -> Dict[str, Any]:
        event.setdefault("run_id", _utc_now())
        event.setdefault("quarantine", 0)
        event.setdefault("ingestion_ts", _utc_now())
        cursor = self._conn.cursor()
        prev_hash = self._last_row_hash()
        payload = dict(event)
        payload["custom_metrics"] = json.dumps(payload.get("custom_metrics") or {})
        row_hash = _hash_row(payload, prev_hash)
        cursor.execute(
            """
            INSERT OR REPLACE INTO job_runs
            (run_id, job_id, status, timestamp_start, timestamp_end, duration_ms, exit_code,
             stdout_tail, stderr_tail, cpu_percent, memory_mb, custom_metrics, quarantine, ingestion_hash, ingestion_ts)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.get("run_id"),
                payload.get("job_id"),
                payload.get("status"),
                payload.get("timestamp_start"),
                payload.get("timestamp_end"),
                payload.get("duration_ms"),
                payload.get("exit_code"),
                payload.get("stdout_tail"),
                payload.get("stderr_tail"),
                payload.get("resource_usage", {}).get("cpu_percent") if isinstance(payload.get("resource_usage"), dict) else payload.get("cpu_percent"),
                payload.get("resource_usage", {}).get("memory_mb") if isinstance(payload.get("resource_usage"), dict) else payload.get("memory_mb"),
                payload.get("custom_metrics"),
                payload.get("quarantine", 0),
                row_hash,
                payload.get("ingestion_ts"),
            ),
        )
        cursor.execute(
            "INSERT INTO merkle_chain (run_id, prev_hash, payload_json, row_hash, created_at) VALUES (?, ?, ?, ?, ?)",
            (payload.get("run_id"), prev_hash, json.dumps(payload, sort_keys=True, default=str), row_hash, _utc_now()),
        )
        self._conn.commit()
        return {"run_id": payload.get("run_id"), "ingestion_hash": row_hash}

    def get_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM job_runs WHERE run_id = ?", (run_id,))
        row = cursor.fetchone()
        if not row:
            return None
        result = dict(row)
        result["custom_metrics"] = json.loads(result.get("custom_metrics") or "{}")
        return result

    def query_runs(
        self,
        job_id: Optional[str] = None,
        status: Optional[str] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        cursor = self._conn.cursor()
        conditions = []
        params: list[Any] = []
        if job_id:
            conditions.append("job_id = ?")
            params.append(job_id)
        if status:
            conditions.append("status = ?")
            params.append(status)
        if start:
            conditions.append("timestamp_start >= ?")
            params.append(start)
        if end:
            conditions.append("timestamp_end <= ?")
            params.append(end)
        query = "SELECT * FROM job_runs"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY ingestion_ts DESC LIMIT ?"
        params.append(limit)
        cursor.execute(query, params)
        rows = [dict(row) for row in cursor.fetchall()]
        for row in rows:
            row["custom_metrics"] = json.loads(row.get("custom_metrics") or "{}")
        return {"runs": rows, "count": len(rows)}

    def validate_chain(self) -> Dict[str, Any]:
        cursor = self._conn.cursor()
        cursor.execute("SELECT run_id, prev_hash, payload_json, row_hash FROM merkle_chain ORDER BY id ASC")
        rows = cursor.fetchall()
        invalid: list[str] = []
        for row in rows:
            run_id, prev_hash, payload_json, expected_row_hash = row
            payload = json.loads(payload_json) if payload_json else {}
            expected = _hash_row(payload, prev_hash)
            if expected != expected_row_hash:
                invalid.append(run_id)
        return {"valid": len(invalid) == 0, "invalid_run_ids": invalid, "chain_length": len(rows)}

    def db_path(self) -> Path:
        return self._db_path

    def close(self) -> None:
        self._conn.close()

    def delete_runs_before(self, threshold_iso: str) -> int:
        cursor = self._conn.cursor()
        cursor.execute("SELECT run_id FROM job_runs WHERE timestamp_start IS NOT NULL AND timestamp_start <= ?", (threshold_iso,))
        rows = cursor.fetchall()
        cursor.execute("DELETE FROM job_runs WHERE timestamp_start IS NOT NULL AND timestamp_start <= ?", (threshold_iso,))
        self._conn.commit()
        return len(rows)

    def append_anomaly(self, anomaly_id: str, job_id: str, kind: str, detail: Optional[str], run_id: Optional[str], detected_at: Optional[str] = None) -> Dict[str, Any]:
        detected_at = detected_at or _utc_now()
        cursor = self._conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO anomalies (anomaly_id, job_id, detected_at, kind, detail, run_id) VALUES (?, ?, ?, ?, ?, ?)",
            (anomaly_id, job_id, detected_at, kind, detail, run_id),
        )
        self._conn.commit()
        return {"anomaly_id": anomaly_id, "job_id": job_id, "kind": kind}

    def query_anomalies(self, job_id: Optional[str] = None, limit: int = 50) -> Dict[str, Any]:
        cursor = self._conn.cursor()
        params: list[Any] = []
        query = "SELECT * FROM anomalies"
        if job_id:
            query += " WHERE job_id = ?"
            params.append(job_id)
        query += " ORDER BY detected_at DESC LIMIT ?"
        params.append(limit)
        cursor.execute(query, params)
        rows = [dict(row) for row in cursor.fetchall()]
        return {"anomalies": rows, "count": len(rows)}


import json

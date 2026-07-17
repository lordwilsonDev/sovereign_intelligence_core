from __future__ import annotations

import json
import sqlite3
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class EventRecord:
    event_id: str
    event_type: str
    source: str
    payload: str
    timestamp_ms: int
    status: str = "pending"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EventRecord":
        return cls(
            event_id=data["event_id"],
            event_type=data["event_type"],
            source=data["source"],
            payload=data["payload"],
            timestamp_ms=data["timestamp_ms"],
            status=data.get("status", "pending"),
        )


class PersistentEventLog:
    def __init__(self, db_path: str, *, flush_interval: float = 0.1, batch_size: int = 100) -> None:
        self.db_path = str(Path(db_path).expanduser())
        self.flush_interval = flush_interval
        self.batch_size = max(1, batch_size)
        self._batch: List[Dict[str, Any]] = []
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._shutdown = threading.Event()

    def start(self) -> None:
        with self._lock:
            if self._running:
                return
            self._running = True
            self._shutdown.clear()
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            with sqlite3.connect(self.db_path) as db:
                db.execute(
                    """
                    CREATE TABLE IF NOT EXISTS events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        event_id TEXT UNIQUE NOT NULL,
                        event_type TEXT NOT NULL,
                        source TEXT NOT NULL,
                        payload TEXT NOT NULL,
                        timestamp INTEGER NOT NULL,
                        status TEXT DEFAULT 'pending',
                        processed_at INTEGER,
                        error TEXT
                    )
                    """
                )
                db.commit()
            self._thread = threading.Thread(target=self._flush_loop, daemon=True)
            self._thread.start()

    def stop(self, *, timeout: float = 2.0) -> None:
        self._shutdown.set()
        with self._condition:
            self._condition.notify_all()
        if self._thread is not None:
            self._thread.join(timeout=timeout)
        with self._lock:
            self._running = False
            self._flush_remaining()

    def append(self, event_type: str, source: str, payload: Dict[str, Any]) -> EventRecord:
        record = EventRecord(
            event_id=f"{int(time.time()*1000)}-{sum(hash(str(k)) for k in sorted(payload.keys()))}",
            event_type=event_type,
            source=source,
            payload=json.dumps(payload, default=str),
            timestamp_ms=int(time.time() * 1000),
            status="pending",
        )
        with self._condition:
            self._batch.append(
                {
                    "event_id": record.event_id,
                    "event_type": record.event_type,
                    "source": record.source,
                    "payload": record.payload,
                    "timestamp_ms": record.timestamp_ms,
                    "status": record.status,
                }
            )
            if len(self._batch) >= self.batch_size:
                self._condition.notify()
        return record

    def query(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as db:
            db.row_factory = sqlite3.Row
            cursor = db.execute(
                "SELECT * FROM events ORDER BY timestamp DESC LIMIT ? OFFSET ?",
                (limit, offset),
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def _flush_loop(self) -> None:
        while True:
            with self._condition:
                if not self._running and not self._batch:
                    break
                self._condition.wait(timeout=self.flush_interval)
                if not self._batch:
                    if self._shutdown.is_set():
                        break
                    continue
                batch = self._batch[: self.batch_size]
                del self._batch[: len(batch)]
            self._write_batch(batch)
            if self._shutdown.is_set() and not self._batch:
                break

    def _write_batch(self, batch: List[Dict[str, Any]]) -> None:
        with sqlite3.connect(self.db_path) as db:
            db.executemany(
                "INSERT OR IGNORE INTO events (event_id, event_type, source, payload, timestamp, status) VALUES (?, ?, ?, ?, ?, ?)",
                [
                    (item["event_id"], item["event_type"], item["source"], item["payload"], item["timestamp_ms"], item["status"])
                    for item in batch
                ],
            )
            db.commit()

    def _flush_remaining(self) -> None:
        if not self._batch:
            return
        batch = self._batch[:]
        self._batch.clear()
        if batch:
            self._write_batch(batch)

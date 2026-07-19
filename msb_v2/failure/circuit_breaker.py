from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass(frozen=True)
class GraphNode:
    node_id: str
    label: str
    node_type: str = "concept"
    weight: float = 0.5


@dataclass(frozen=True)
class GraphEdge:
    source: str
    target: str
    relation: str
    weight: float = 0.5


class CircuitBreakerStateStore:
    def __init__(self, path: str = "./circuit_breaker.db") -> None:
        self.path = str(Path(path).resolve())
        self._initialize()

    def _initialize(self) -> None:
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS circuit_breaker (
                    service TEXT PRIMARY KEY,
                    state TEXT NOT NULL,
                    failure_count INTEGER NOT NULL,
                    last_failure TEXT
                )
                """
            )
            conn.execute("CREATE TABLE IF NOT EXISTS failure_log (id INTEGER PRIMARY KEY AUTOINCREMENT, service TEXT NOT NULL, message TEXT NOT NULL, recorded_at TEXT NOT NULL)")
            conn.commit()

    def record_failure(self, service: str, error: str) -> None:
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                INSERT INTO circuit_breaker (service, state, failure_count, last_failure)
                VALUES (?, 'OPEN', COALESCE((SELECT failure_count FROM circuit_breaker WHERE service = ?), 0) + 1, ?)
                ON CONFLICT(service) DO UPDATE SET
                    state='OPEN',
                    failure_count=circuit_breaker.failure_count + 1,
                    last_failure=excluded.last_failure
                """,
                (service, service, error),
            )
            conn.execute("INSERT INTO failure_log (service, message, recorded_at) VALUES (?, ?, datetime('now'))", (service, error))
            conn.commit()

    def reset(self, service: str) -> None:
        with sqlite3.connect(self.path) as conn:
            conn.execute("DELETE FROM circuit_breaker WHERE service = ?", (service,))
            conn.commit()

    def get_state(self, service: str) -> dict:
        with sqlite3.connect(self.path) as conn:
            row = conn.execute("SELECT service, state, failure_count, last_failure FROM circuit_breaker WHERE service = ?", (service,)).fetchone()
            if not row:
                return {"service": service, "state": "CLOSED", "failure_count": 0, "last_failure": None}
            return dict(zip(["service", "state", "failure_count", "last_failure"], row))

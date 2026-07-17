from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class DriftSignal:
    proposal_id: str
    source: str
    event_kind: str
    created_at: str
    evidence: Dict[str, Any]
    status: str = "pending"


class EvolutionScanner:
    def __init__(self, db_path: str = "/Users/lordwilson/msb-v2/.artifacts/evolution_store.sqlite", *, window_limit: int = 1000) -> None:
        self.db_path = str(Path(db_path).expanduser())
        self.window_limit = max(1, window_limit)
        self._init_db()

    def _init_db(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS drift_events (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  proposal_id TEXT UNIQUE NOT NULL,
                  source TEXT NOT NULL,
                  event_kind TEXT NOT NULL,
                  evidence TEXT NOT NULL,
                  status TEXT DEFAULT 'pending',
                  created_at TEXT NOT NULL
                )
                """
            )
            db.commit()

    def window(self, event_type: str, *, since: Optional[str] = None) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as db:
            db.row_factory = sqlite3.Row
            clauses = ["event_type = ?"]
            args: list[Any] = [event_type]
            if since:
                clauses.append("timestamp >= ?")
                args.append(since)
            cursor = db.execute(
                f"SELECT * FROM events WHERE {' AND '.join(clauses)} ORDER BY timestamp DESC LIMIT ?",
                (*args, self.window_limit),
            )
            return [dict(row) for row in cursor.fetchall()]

    def save_drift(self, drift: DriftSignal) -> None:
        with sqlite3.connect(self.db_path) as db:
            db.execute(
                """
                INSERT OR IGNORE INTO drift_events (proposal_id, source, event_kind, evidence, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (drift.proposal_id, drift.source, drift.event_kind, __import__("json").dumps(drift.evidence), drift.status, drift.created_at),
            )
            db.commit()

    def pending(self, *, limit: int = 100) -> List[DriftSignal]:
        with sqlite3.connect(self.db_path) as db:
            db.row_factory = sqlite3.Row
            cursor = db.execute(
                "SELECT * FROM drift_events WHERE status = 'pending' ORDER BY created_at DESC LIMIT ?",
                (limit,),
            )
            rows = cursor.fetchall()
        signals = []
        for row in rows:
            signals.append(
                DriftSignal(
                    proposal_id=row["proposal_id"],
                    source=row["source"],
                    event_kind=row["event_kind"],
                    created_at=row["created_at"],
                    evidence=__import__("json").loads(row["evidence"]),
                    status=row["status"],
                )
            )
        return signals

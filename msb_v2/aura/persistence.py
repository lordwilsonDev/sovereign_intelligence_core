from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional


class Persistence:
    def __init__(self, db_path: str = ":memory:") -> None:
        self.db_path = db_path
        self._is_postgres = str(db_path).startswith("postgresql://")
        self._pg = None
        if self._is_postgres:
            try:
                import psycopg2  # type: ignore
                self._pg = psycopg2
            except ImportError as exc:
                raise RuntimeError("PostgreSQL persistence requires psycopg2. Install it or use SQLite.") from exc
        self._local = threading.local()
        self._replay_path = (Path(db_path).parent if Path(db_path).parent.exists() else Path(".")) / f"{Path(db_path).name}.offline-replay.jsonl"
        self._replay_lock = threading.Lock()
        self._init()

    def _conn(self) -> Any:
        if self._is_postgres:
            conn = self._pg.connect(self.db_path)
            conn.row_factory = _DictRow  # psycopg2 doesn't set row_factory by default
            return conn
        conn: sqlite3.Connection | None = getattr(self._local, "conn", None)
        if conn is None:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            self._local.conn = conn
            self._init()
        return conn

    def _init(self) -> None:
        with self._conn() as conn:
            if self._is_postgres:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                      task_id TEXT PRIMARY KEY,
                      status TEXT NOT NULL,
                      goal TEXT NOT NULL,
                      client_id TEXT DEFAULT 'default',
                      priority INTEGER DEFAULT 2,
                      created_at REAL NOT NULL,
                      retry_count INTEGER DEFAULT 0,
                      max_retries INTEGER DEFAULT 3,
                      metadata TEXT DEFAULT '{}'
                    )
                """)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS events (
                      event_id TEXT PRIMARY KEY,
                      timestamp REAL NOT NULL,
                      session_id TEXT NOT NULL,
                      phase TEXT NOT NULL,
                      actor TEXT DEFAULT 'AURA',
                      tool_name TEXT,
                      latency_ms REAL,
                      status TEXT DEFAULT 'SUCCESS',
                      payload TEXT DEFAULT '{}'
                    )
                """)
            else:
                conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                  task_id TEXT PRIMARY KEY,
                  status TEXT NOT NULL,
                  goal TEXT NOT NULL,
                  client_id TEXT DEFAULT 'default',
                  priority INTEGER DEFAULT 2,
                  created_at REAL NOT NULL,
                  retry_count INTEGER DEFAULT 0,
                  max_retries INTEGER DEFAULT 3,
                  metadata TEXT DEFAULT '{}'
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                  event_id TEXT PRIMARY KEY,
                  timestamp REAL NOT NULL,
                  session_id TEXT NOT NULL,
                  phase TEXT NOT NULL,
                  actor TEXT DEFAULT 'AURA',
                  tool_name TEXT,
                  latency_ms REAL,
                  status TEXT DEFAULT 'SUCCESS',
                  payload TEXT DEFAULT '{}'
                )
                """
            )
            conn.commit()

    def save_task(self, task: Dict[str, Any]) -> None:
        try:
            with self._conn() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO tasks(task_id, status, goal, client_id, priority, created_at, retry_count, max_retries, metadata) VALUES(?,?,?,?,?,?,?,?,?)",
                    (
                        str(task["task_id"]),
                        str(task.get("status", "")),
                        str(task["goal"]),
                        str(task.get("client_id", "default")),
                        int(task.get("priority", 2)),
                        float(task["created_at"]),
                        int(task.get("retry_count", 0)),
                        int(task.get("max_retries", 3)),
                        json.dumps(task.get("metadata", {})),
                    ),
                )
                conn.commit()
        except Exception:
            self._enqueue_replay({"type": "task", "payload": task})

    def save_event(self, event: Dict[str, Any]) -> None:
        phase = event.get("phase")
        if hasattr(phase, "value"):
            event = dict(event)
            event["phase"] = phase.value
        try:
            with self._conn() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO events(event_id, timestamp, session_id, phase, actor, tool_name, latency_ms, status, payload) VALUES(?,?,?,?,?,?,?,?,?)",
                    (
                        str(event.get("event_id", "")),
                        float(event.get("timestamp", 0)),
                        str(event.get("session_id", "")),
                        str(event.get("phase", "")),
                        str(event.get("actor", "AURA")),
                        str(event.get("tool_name") or ""),
                        float(event.get("latency_ms") or 0),
                        str(event.get("status", "SUCCESS")),
                        json.dumps(event.get("payload", {})),
                    ),
                )
                conn.commit()
        except Exception:
            self._enqueue_replay({"type": "event", "payload": event})

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        with self._conn() as conn:
            row = conn.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,)).fetchone()
        if not row:
            return None
        data = dict(row)
        data["metadata"] = json.loads(data.get("metadata") or "{}")
        return data

    def recent_events(self, session_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM events WHERE session_id=? ORDER BY timestamp DESC LIMIT ?",
                (session_id, limit),
            ).fetchall()
        out: List[Dict[str, Any]] = []
        for row in rows:
            data = dict(row)
            data["payload"] = json.loads(data.get("payload") or "{}")
            out.append(data)
        return out

    def _enqueue_replay(self, record: Dict[str, Any]) -> None:
        with self._replay_lock:
            try:
                self._replay_path.write_text(
                    json.dumps(record, default=str) + "\n",
                    encoding="utf-8",
                )
            except Exception:
                pass

    def replay_offline(self) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []
        if not self._replay_path.exists():
            return records
        try:
            lines = self._replay_path.read_text(encoding="utf-8").splitlines()
            for line in lines:
                if not line.strip():
                    continue
                try:
                    records.append(json.loads(line))
                except Exception:
                    continue
        except Exception:
            pass
        return records


class _DictRow:
    def __init__(self, cursor: Any, row: Any) -> None:
        self._cursor = cursor
        self._row = row
        self._mapping = {d[0]: row[i] for i, d in enumerate(cursor.description)}

    def __getitem__(self, key: str) -> Any:
        return self._mapping[key]

    def keys(self) -> List[str]:
        return list(self._mapping.keys())

    def get(self, key: str, default: Any = None) -> Any:
        return self._mapping.get(key, default)

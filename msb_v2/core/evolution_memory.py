from __future__ import annotations

import json
import sqlite3
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class EvolutionMemory:
    def __init__(self, db_path: str = "evolution_memory.db") -> None:
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS proposals (
                    proposal_id TEXT PRIMARY KEY,
                    module TEXT,
                    patch_hash TEXT,
                    change_type TEXT,
                    result TEXT,
                    failure_reason TEXT,
                    lesson TEXT,
                    metrics_before TEXT,
                    metrics_after TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS evolution_events (
                    event_id TEXT PRIMARY KEY,
                    proposal_id TEXT,
                    stage TEXT,
                    observation TEXT,
                    metric_delta TEXT,
                    decision TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (proposal_id) REFERENCES proposals(proposal_id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS capability_baseline (
                    id INTEGER PRIMARY KEY,
                    test_name TEXT,
                    expected_value REAL,
                    tolerance REAL,
                    timestamp DATETIME
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_proposal_module ON proposals(module)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_proposal_result ON proposals(result)")

    def record_proposal(
        self,
        proposal: Dict[str, Any],
        result: str,
        reason: str,
        lesson: str,
        metrics_before: Dict[str, Any],
        metrics_after: Dict[str, Any],
    ) -> str:
        module = proposal.get("module") or proposal.get("worst_module", {}).get("path", "")
        patch_hash = proposal.get("patch_hash", "")
        change_type = proposal.get("change_type", "refactor")
        base = f"{module}:{patch_hash}:{change_type}"
        proposal_id = proposal.get("proposal_id") or hashlib.sha256(base.encode()).hexdigest()[:8]
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO proposals
                (proposal_id, module, patch_hash, change_type, result, failure_reason, lesson,
                 metrics_before, metrics_after, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """,
                (
                    proposal_id,
                    module,
                    patch_hash,
                    change_type,
                    result,
                    reason,
                    lesson,
                    json.dumps(metrics_before),
                    json.dumps(metrics_after),
                ),
            )
        return proposal_id

    def record_event(
        self,
        proposal_id: str,
        stage: str,
        observation: str,
        metric_delta: Dict[str, Any],
        decision: str,
    ) -> None:
        event_id = f"{proposal_id}-{stage}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO evolution_events
                (event_id, proposal_id, stage, observation, metric_delta, decision, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """,
                (event_id, proposal_id, stage, observation, json.dumps(metric_delta), decision),
            )

    def get_proposal(self, proposal_id: str) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute("SELECT * FROM proposals WHERE proposal_id = ?", (proposal_id,)).fetchone()
            return dict(row) if row else None

    def get_events(self, proposal_id: str) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM evolution_events WHERE proposal_id = ? ORDER BY timestamp", (proposal_id,)).fetchall()
            return [dict(row) for row in rows]

    def get_similar_proposals(self, module: str, change_type: Optional[str] = None) -> List[Dict[str, Any]]:
        query = "SELECT * FROM proposals WHERE module = ?"
        params: List[str] = [module]
        if change_type:
            query += " AND change_type = ?"
            params.append(change_type)
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(query, params).fetchall()
            return [dict(row) for row in rows]

    def get_historical_confidence(self, module: str, change_type: Optional[str] = None) -> float:
        similar = self.get_similar_proposals(module, change_type)
        if not similar:
            return 1.0
        failures = sum(1 for p in similar if p["result"] == "rejected")
        successes = sum(1 for p in similar if p["result"] == "accepted")
        total = failures + successes
        if total == 0:
            return 1.0
        return successes / total

    def set_capability_baseline(self, test_name: str, expected_value: float, tolerance: float = 0.05) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO capability_baseline (test_name, expected_value, tolerance, timestamp)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                """,
                (test_name, expected_value, tolerance),
            )

    def get_capability_baseline(self, test_name: str) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                """
                SELECT test_name, expected_value, tolerance FROM capability_baseline
                WHERE test_name = ? ORDER BY timestamp DESC LIMIT 1
                """,
                (test_name,),
            ).fetchone()
        return dict(row) if row else None

    def get_all_capability_baselines(self) -> Dict[str, Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT test_name, expected_value, tolerance FROM capability_baseline
                ORDER BY timestamp DESC
                """
            ).fetchall()
        result: Dict[str, Dict[str, Any]] = {}
        for row in rows:
            if row["test_name"] not in result:
                result[row["test_name"]] = {"expected": row["expected_value"], "tolerance": row["tolerance"]}
        return result

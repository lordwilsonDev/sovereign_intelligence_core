from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import Any, Dict, Optional

from msb_v2.core.evolution_memory import EvolutionMemory


class FalsificationMirror:
    """Compares live capability results to baselines and computes Reality Coherence (R_i)."""

    COHERENCE_THRESHOLD = 0.8

    def __init__(self, memory: EvolutionMemory) -> None:
        self.memory = memory
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.memory.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS falsification_checks (
                    check_id TEXT PRIMARY KEY,
                    category TEXT,
                    live_score REAL,
                    baseline_expected REAL,
                    baseline_tolerance REAL,
                    r_i REAL,
                    status TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_falsification_category ON falsification_checks(category)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_falsification_status ON falsification_checks(status)
            """)

    @staticmethod
    def compute_r_i(live: float, expected: float, tolerance: float) -> float:
        """Compute Reality Coherence Term. 1.0 == perfect agreement."""
        delta = abs(live - expected)
        if delta <= tolerance:
            return 1.0
        denom = max(abs(expected), abs(live), tolerance, 1e-9)
        return max(0.0, min(1.0, 1.0 - (delta / denom)))

    def evaluate(self, category: str, live_score: float) -> Dict[str, Any]:
        baseline = self.memory.get_capability_baseline(category)
        if baseline is None:
            return {
                "category": category,
                "live_score": live_score,
                "status": "NO_BASELINE",
                "r_i": None,
            }

        expected = float(baseline.get("expected", baseline.get("expected_value", 0.0)))
        tolerance = float(baseline.get("tolerance", 0.0))
        r_i = self.compute_r_i(live_score, expected, tolerance)
        status = "COHERENT" if r_i >= self.COHERENCE_THRESHOLD else "FALSIFIED"

        check_id = f"{category}-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        with sqlite3.connect(self.memory.db_path) as conn:
            conn.execute(
                """
                INSERT INTO falsification_checks
                (check_id, category, live_score, baseline_expected, baseline_tolerance, r_i, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    check_id,
                    category,
                    live_score,
                    expected,
                    tolerance,
                    r_i,
                    status,
                ),
            )

        return {
            "check_id": check_id,
            "category": category,
            "live_score": live_score,
            "baseline_expected": expected,
            "baseline_tolerance": tolerance,
            "delta": round(live_score - expected, 4),
            "r_i": round(r_i, 4),
            "status": status,
        }

    def evaluate_batch(self, capability_results: Dict[str, Any]) -> Dict[str, Any]:
        outcomes: Dict[str, Any] = {"checks": [], "falsified": []}
        for category, summary in capability_results.get("summary", {}).items():
            live = float(summary.get("average_score", 0.0))
            check = self.evaluate(category, live)
            outcomes["checks"].append(check)
            if check.get("status") == "FALSIFIED":
                outcomes["falsified"].append(check)
        outcomes["coherence_rate"] = round(
            sum(1 for c in outcomes["checks"] if c.get("status") == "COHERENT")
            / max(len(outcomes["checks"]), 1),
            4,
        )
        return outcomes

    def history(self, category: Optional[str] = None, status: Optional[str] = None) -> list[dict]:
        query = "SELECT * FROM falsification_checks"
        params: list[Any] = []
        clauses: list[str] = []
        if category is not None:
            clauses.append("category = ?")
            params.append(category)
        if status is not None:
            clauses.append("status = ?")
            params.append(status)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY timestamp DESC"
        with sqlite3.connect(self.memory.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]

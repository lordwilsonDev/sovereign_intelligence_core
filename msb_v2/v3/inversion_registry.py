from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class Hypothesis:
    hypothesis_id: str
    assumption: str
    inversion: str
    constraint_check: bool = True
    confidence: float = 0.0
    status: str = "draft"


@dataclass
class Experiment:
    experiment_id: str
    hypothesis_id: str
    procedure: str
    expected_outcome: str
    observed_outcome: str
    evidence_score: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class InversionRegistry:
    def __init__(self, db_path: str = ":memory:") -> None:
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init()

    def _init(self) -> None:
        cur = self._conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS hypotheses (hypothesis_id TEXT PRIMARY KEY, "
            "assumption TEXT, inversion TEXT, constraint_check INTEGER, "
            "confidence REAL, status TEXT)"
        )
        cur.execute(
            "CREATE TABLE IF NOT EXISTS experiments (experiment_id TEXT PRIMARY KEY, "
            "hypothesis_id TEXT, procedure TEXT, expected_outcome TEXT, "
            "observed_outcome TEXT, evidence_score REAL, created_at TEXT)"
        )
        self._conn.commit()

    def add_hypothesis(self, hypothesis: Hypothesis) -> None:
        cur = self._conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO hypotheses VALUES (?,?,?,?,?,?)",
            (
                hypothesis.hypothesis_id,
                hypothesis.assumption,
                hypothesis.inversion,
                1 if hypothesis.constraint_check else 0,
                hypothesis.confidence,
                hypothesis.status,
            ),
        )
        self._conn.commit()

    def add_experiment(self, experiment: Experiment) -> None:
        cur = self._conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO experiments VALUES (?,?,?,?,?,?,?)",
            (
                experiment.experiment_id,
                experiment.hypothesis_id,
                experiment.procedure,
                experiment.expected_outcome,
                experiment.observed_outcome,
                experiment.evidence_score,
                experiment.created_at,
            ),
        )
        self._conn.commit()

    def get_hypothesis(self, hypothesis_id: str) -> Optional[Dict[str, Any]]:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM hypotheses WHERE hypothesis_id = ?", (hypothesis_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def experiments_for(self, hypothesis_id: str) -> List[Dict[str, Any]]:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM experiments WHERE hypothesis_id = ? ORDER BY created_at", (hypothesis_id,))
        return [dict(r) for r in cur.fetchall()]

    def summary(self) -> Dict[str, Any]:
        cur = self._conn.cursor()
        cur.execute("SELECT COUNT(*) FROM hypotheses")
        hypothesis_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM experiments")
        experiment_count = cur.fetchone()[0]
        cur.execute("SELECT AVG(evidence_score) FROM experiments")
        avg_score = cur.fetchone()[0] or 0.0
        return {
            "hypothesis_count": hypothesis_count,
            "experiment_count": experiment_count,
            "avg_evidence_score": round(float(avg_score), 4),
        }


_registry: InversionRegistry | None = None


def get_registry() -> InversionRegistry:
    global _registry
    if _registry is None:
        _registry = InversionRegistry()
    return _registry

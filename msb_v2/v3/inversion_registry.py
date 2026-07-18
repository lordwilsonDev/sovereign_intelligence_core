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


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    experiment_id: str
    supports: bool = True
    score: float = 0.5
    note: str = ""


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
            "hypothesis_id TEXT, procedure TEXT, expected_outcome TEXT, observed_outcome TEXT, "
            "evidence_score REAL, created_at TEXT)"
        )
        cur.execute(
            "CREATE TABLE IF NOT EXISTS evidence (evidence_id TEXT PRIMARY KEY, "
            "experiment_id TEXT, supports INTEGER, score REAL, note TEXT)"
        )
        self._conn.commit()

    def add_hypothesis(self, hypothesis: Hypothesis) -> Hypothesis:
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
        return hypothesis

    def register_hypothesis(self, title: str, description: str = "", assumptions: Optional[List[str]] = None) -> Hypothesis:
        assumptions = assumptions or []
        assumption = title
        inversion = f"What if the opposite is true: {assumption}"
        hypothesis = Hypothesis(
            hypothesis_id=f"hyp-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            assumption=assumption,
            inversion=inversion,
            constraint_check=True,
            confidence=0.5,
            status="draft",
        )
        return self.add_hypothesis(hypothesis)

    def add_experiment(self, experiment: Experiment) -> Experiment:
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
        return experiment

    def register_experiment(self, hypothesis_id: str, description: str = "") -> Experiment:
        experiment = Experiment(
            experiment_id=f"exp-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            hypothesis_id=hypothesis_id,
            procedure=description,
            expected_outcome=description,
            observed_outcome="",
        )
        return self.add_experiment(experiment)

    def add_evidence(self, experiment_id: str, supports: bool = True, score: float = 0.5, note: str = "") -> Evidence:
        evidence = Evidence(
            evidence_id=f"ev-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            experiment_id=experiment_id,
            supports=supports,
            score=score,
            note=note,
        )
        cur = self._conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO evidence VALUES (?,?,?,?,?)",
            (evidence.evidence_id, evidence.experiment_id, 1 if evidence.supports else 0, evidence.score, evidence.note),
        )
        self._conn.commit()
        return evidence

    def get_hypothesis(self, hypothesis_id: str) -> Optional[Dict[str, Any]]:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM hypotheses WHERE hypothesis_id = ?", (hypothesis_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def experiments_for(self, hypothesis_id: str) -> List[Dict[str, Any]]:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM experiments WHERE hypothesis_id = ? ORDER BY created_at", (hypothesis_id,))
        return [dict(r) for r in cur.fetchall()]

    def list_hypotheses(self) -> List[Hypothesis]:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM hypotheses ORDER BY rowid DESC")
        out = []
        for row in cur.fetchall():
            out.append(
                Hypothesis(
                    hypothesis_id=row["hypothesis_id"],
                    assumption=row["assumption"],
                    inversion=row["inversion"],
                    constraint_check=bool(row["constraint_check"]),
                    confidence=float(row["confidence"] or 0.0),
                    status=row["status"],
                )
            )
        return out

    def list_experiments(self) -> List[Experiment]:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM experiments ORDER BY rowid DESC")
        out = []
        for row in cur.fetchall():
            out.append(
                Experiment(
                    experiment_id=row["experiment_id"],
                    hypothesis_id=row["hypothesis_id"],
                    procedure=row["procedure"],
                    expected_outcome=row["expected_outcome"],
                    observed_outcome=row["observed_outcome"],
                    evidence_score=float(row["evidence_score"] or 0.0),
                    created_at=row["created_at"],
                )
            )
        return out

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

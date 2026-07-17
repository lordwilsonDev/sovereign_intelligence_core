from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class CalibrationRecord:
    record_id: str
    statement_id: str
    trace_id: Optional[str]
    decision_id: Optional[str]
    predicted_confidence: float
    actual: bool
    brier: float
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat() + "Z")

    def payload(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "statement_id": self.statement_id,
            "trace_id": self.trace_id,
            "decision_id": self.decision_id,
            "predicted_confidence": self.predicted_confidence,
            "actual": self.actual,
            "brier": self.brier,
            "created_at": self.created_at,
        }


class CalibrationStore:
    def __init__(self) -> None:
        self._records: List[CalibrationRecord] = []
        self._sequence = 0

    def record(self, statement_id: str, confidence: float, actual: bool, trace_id: Optional[str] = None, decision_id: Optional[str] = None) -> CalibrationRecord:
        self._sequence += 1
        record_id = f"calibration-{self._sequence:04d}"
        brier = float((confidence - float(actual)) ** 2)
        record = CalibrationRecord(
            record_id=record_id,
            statement_id=statement_id,
            trace_id=trace_id,
            decision_id=decision_id,
            predicted_confidence=confidence,
            actual=actual,
            brier=brier,
        )
        self._records.append(record)
        return record

    def summary(self, window: int = 100) -> Dict[str, Any]:
        recent = self._records[-window:]
        total = len(recent)
        if not total:
            return {"count": 0, "accuracy": None, "avg_brier": None, "bins": []}
        accuracy = sum(1 for r in recent if r.actual) / total
        avg_brier = sum(r.brier for r in recent) / total
        bins = [
            {
                "bin_start": start,
                "bin_end": end,
                "count": sum(1 for r in recent if start <= r.predicted_confidence < end),
                "accuracy": sum(1 for r in recent if start <= r.predicted_confidence < end and r.actual) / max(1, sum(1 for r in recent if start <= r.predicted_confidence < end)),
            }
            for start, end in [(0.0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.01)]
        ]
        return {"count": total, "accuracy": accuracy, "avg_brier": avg_brier, "bins": bins}

    def list_records(self, window: int = 100) -> List[Dict[str, Any]]:
        return [r.payload() for r in self._records[-window:]]

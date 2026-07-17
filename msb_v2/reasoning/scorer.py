from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass(frozen=True)
class ConfidenceAssessment:
    trace_id: Optional[str]
    statement_id: Optional[str]
    score: float
    confidence: float
    concurrence: float
    dissent: float
    entropy: float
    ground_truth_accepted: Optional[bool]
    notes: str = ""
    ts: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat() + "Z")

    def payload(self) -> dict[str, object]:
        return {
            "trace_id": self.trace_id,
            "statement_id": self.statement_id,
            "score": self.score,
            "confidence": self.confidence,
            "concurrence": self.concurrence,
            "dissent": self.dissent,
            "entropy": self.entropy,
            "ground_truth_accepted": self.ground_truth_accepted,
            "notes": self.notes,
            "ts": self.ts,
        }


def score_from_events(events: list[dict[str, Any]]) -> ConfidenceAssessment:
    trace_id = None
    statement_id = None
    tool_calls = 0
    memory_reads = 0
    human = 0
    errors = 0
    concurrence = 0.0
    dissent = 0.0

    for event in events:
        trace_id = event.get("trace_id") or trace_id
        statement_id = event.get("event_id") or statement_id
        kind = event.get("kind")
        payload = event.get("payload") or {}
        verdict = payload.get("verdict")
        if kind in ("tool", "tool_result"):
            tool_calls += 1
            if verdict == "rejected":
                dissent += 0.5
        elif kind == "memory_read":
            memory_reads += 1
            concurrence += 1.0
            if verdict == "rejected":
                dissent += 0.5
        elif kind == "human":
            human += 1
            if verdict == "rejected":
                dissent += 1.0
        elif kind == "error":
            errors += 1
            dissent += 1.0

    score = max(0.0, min(1.0, 0.5 + 0.15 * tool_calls + 0.15 * memory_reads + 0.35 * human - 0.4 * errors - 0.2 * dissent))
    confidence = max(0.0, min(1.0, 0.6 + 0.12 * memory_reads + 0.25 * human - 0.25 * errors - 0.2 * dissent))
    entropy = max(0.0, dissent / max(1, tool_calls + memory_reads + human + 1))
    return ConfidenceAssessment(
        trace_id=trace_id,
        statement_id=statement_id,
        score=score,
        confidence=confidence,
        concurrence=concurrence,
        dissent=dissent,
        entropy=entropy,
        ground_truth_accepted=None,
        notes="",
    )

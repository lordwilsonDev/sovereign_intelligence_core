from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


def _extract_identities(events):
    trace_id = None
    statement_id = None
    for event in events:
        trace_id = event.get("trace_id") or trace_id
        statement_id = event.get("event_id") or statement_id
    return trace_id, statement_id


def _aggregate_events(events):
    tool_calls = 0
    memory_reads = 0
    human = 0
    errors = 0
    concurrence = 0.0
    dissent = 0.0
    for event in events:
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
    return {
        "tool_calls": tool_calls,
        "memory_reads": memory_reads,
        "human": human,
        "errors": errors,
        "concurrence": concurrence,
        "dissent": dissent,
    }


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _compute_score(m):
    return _clamp(0.5 + 0.15 * m["tool_calls"] + 0.15 * m["memory_reads"] + 0.35 * m["human"] - 0.4 * m["errors"] - 0.2 * m["dissent"])


def _compute_confidence(m):
    return _clamp(0.6 + 0.12 * m["memory_reads"] + 0.25 * m["human"] - 0.25 * m["errors"] - 0.2 * m["dissent"])


def _compute_entropy(m):
    return _clamp(m["dissent"] / max(1, m["tool_calls"] + m["memory_reads"] + m["human"] + 1))


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
    trace_id, statement_id = _extract_identities(events)
    m = _aggregate_events(events)
    score = _compute_score(m)
    confidence = _compute_confidence(m)
    entropy = _compute_entropy(m)
    return ConfidenceAssessment(
        trace_id=trace_id,
        statement_id=statement_id,
        score=score,
        confidence=confidence,
        concurrence=m["concurrence"],
        dissent=m["dissent"],
        entropy=entropy,
        ground_truth_accepted=None,
        notes="",
    )

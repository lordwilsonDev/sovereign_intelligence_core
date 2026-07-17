from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def _sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class EventKind(str, Enum):
    EXECUTION = "execution"
    MEMORY = "memory"
    TOOL = "tool"
    TOOL_RESULT = "tool_result"
    MEMORY_READ = "memory_read"
    MEMORY_WRITE = "memory_write"
    HUMAN = "human"
    SYSTEM = "system"
    ERROR = "error"
    RECOVERY = "recovery"
    CONFIDENCE_ASSESSMENT = "confidence_assessment"
    DRIFT = "drift"
    ALERT = "alert"


@dataclass(frozen=True)
class ExecutionEvent:
    event_id: str
    sequence: int
    kind: EventKind
    source: str
    payload: dict[str, object] = field(default_factory=dict)
    trace_id: str | None = None
    decision_id: str | None = None
    ts: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    previous_hash: str | None = None
    integrity_hash: str | None = None


@dataclass(frozen=True)
class ConfidenceAssessment:
    trace_id: Optional[str]
    statement_id: Optional[str]
    score: float
    confidence: float
    concurrence: float
    dissent: float
    entropy: float
    ground_truth_accepted: bool
    notes: str = ""
    ts: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


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
        if kind == "tool":
            tool_calls += 1
        elif kind == "memory_read":
            memory_reads += 1
            concurrence += 1.0
        elif kind == "human":
            human += 1
        elif kind == "error":
            errors += 1
            dissent += 1.0

    score = max(0.0, min(1.0, 0.5 + 0.15 * tool_calls + 0.2 * memory_reads - 0.25 * errors))
    confidence = max(0.0, min(1.0, 0.6 + 0.1 * memory_reads + 0.15 * human - 0.2 * errors))
    entropy = max(0.0, dissent / max(1, tool_calls + memory_reads + human))
    return ConfidenceAssessment(
        trace_id=trace_id,
        statement_id=statement_id,
        score=score,
        confidence=confidence,
        concurrence=concurrence,
        dissent=dissent,
        entropy=entropy,
        ground_truth_accepted=False,
    )


class EventStreamStore:
    def __init__(self) -> None:
        self._events: list[ExecutionEvent] = []
        self._sequences: dict[str, int] = {}
        self._baselines: dict[str, dict[str, Any]] = {}
        self._last_hash: str | None = None

    def _event_digest(self, event: ExecutionEvent) -> str:
        body = {
            "event_id": event.event_id,
            "sequence": event.sequence,
            "kind": event.kind.value,
            "source": event.source,
            "payload": event.payload,
            "trace_id": event.trace_id,
            "decision_id": event.decision_id,
            "ts": event.ts,
            "previous_hash": event.previous_hash,
        }
        return _sha256_hex(_canonical_json(body))

    def append(self, event: ExecutionEvent) -> ExecutionEvent:
        seq_key = event.trace_id or event.decision_id or "__global__"
        self._sequences[seq_key] = self._sequences.get(seq_key, 0) + 1
        seq = self._sequences[seq_key]
        previous_hash = self._last_hash
        integrity_hash = self._event_digest(
            ExecutionEvent(
                event_id=event.event_id,
                sequence=seq,
                kind=event.kind,
                source=event.source,
                payload=event.payload,
                trace_id=event.trace_id,
                decision_id=event.decision_id,
                ts=event.ts,
                previous_hash=previous_hash,
            )
        )
        normalized = ExecutionEvent(
            event_id=event.event_id,
            sequence=seq,
            kind=event.kind,
            source=event.source,
            payload=event.payload,
            trace_id=event.trace_id,
            decision_id=event.decision_id,
            ts=event.ts,
            previous_hash=previous_hash,
            integrity_hash=integrity_hash,
        )
        self._events.append(normalized)
        self._last_hash = integrity_hash
        return normalized

    def events_for_trace(self, trace_id: str) -> list[ExecutionEvent]:
        return [e for e in self._events if e.trace_id == trace_id]

    def events_for_decision(self, decision_id: str) -> list[ExecutionEvent]:
        return [e for e in self._events if e.decision_id == decision_id]

    def global_stream(self, limit: int = 100) -> list[ExecutionEvent]:
        return self._events[-limit:]

    def materialize_trace(self, trace_id: str) -> list[dict[str, Any]]:
        events = self.events_for_trace(trace_id)
        return [
            {
                "event_id": e.event_id,
                "sequence": e.sequence,
                "kind": e.kind.value,
                "source": e.source,
                "payload": e.payload,
                "ts": e.ts,
            }
            for e in events
        ]

    def verify_continuity(self, trace_id: str) -> dict[str, Any]:
        events = self.events_for_trace(trace_id)
        sequences = [e.sequence for e in events]
        expected = list(range(1, len(sequences) + 1))
        if not sequences:
            return {"trace_id": trace_id, "continuous": True, "count": 0}
        is_continuous = sequences == expected
        gaps = [i for i, s in enumerate(sequences) if s != expected[i]] if not is_continuous else []
        return {
            "trace_id": trace_id,
            "continuous": is_continuous,
            "count": len(events),
            "first_seq": sequences[0] if sequences else None,
            "last_seq": sequences[-1] if sequences else None,
            "gaps": gaps,
        }

    def set_baseline(self, trace_id: str, assessment: dict[str, Any]) -> dict[str, Any]:
        baseline = {
            "trace_id": trace_id,
            "baseline": {
                "score": assessment.get("score"),
                "confidence": assessment.get("confidence"),
                "entropy": assessment.get("entropy"),
            },
        }
        self._baselines[trace_id] = baseline
        return baseline

    def get_baseline(self, trace_id: str) -> dict[str, Any]:
        return self._baselines.get(trace_id, {})

    def measure_drift(self, trace_id: str, assessment: dict[str, Any]) -> dict[str, Any]:
        baseline = self.get_baseline(trace_id).get("baseline")
        if not baseline:
            return {"trace_id": trace_id, "drifted": False, "reason": "no baseline"}

        delta_score = float(assessment.get("score", 0.0)) - float(baseline.get("score", 0.0))
        delta_confidence = float(assessment.get("confidence", 0.0)) - float(baseline.get("confidence", 0.0))
        delta_entropy = float(assessment.get("entropy", 0.0)) - float(baseline.get("entropy", 0.0))
        threshold = 0.15
        drifted = abs(delta_score) > threshold or abs(delta_entropy) > threshold
        drift_event = ExecutionEvent(
            event_id=f"{trace_id}-drift",
            sequence=len(self.events_for_trace(trace_id)) + 1,
            kind=EventKind.DRIFT,
            source="scorer.drift",
            payload={
                "baseline": baseline,
                "current": {
                    "score": assessment.get("score"),
                    "confidence": assessment.get("confidence"),
                    "entropy": assessment.get("entropy"),
                },
                "delta": {
                    "score": delta_score,
                    "confidence": delta_confidence,
                    "entropy": delta_entropy,
                },
                "drifted": drifted,
            },
            trace_id=trace_id,
        )
        self.append(drift_event)
        return {"trace_id": trace_id, "drifted": drifted, "delta": drift_event.payload, "event_id": drift_event.event_id}

    def verify_integrity(self, decision_id: str) -> dict[str, Any]:
        events = self.events_for_decision(decision_id)
        if not events:
            return {"decision_id": decision_id, "valid": False, "broken_at": None, "expected_hash": None, "actual_hash": None}
        expected = events[0].integrity_hash
        actual = self._event_digest(events[0])
        if events[0].previous_hash is not None and expected != actual:
            return {"decision_id": decision_id, "valid": False, "broken_at": events[0].event_id, "expected_hash": expected, "actual_hash": actual}
        return {"decision_id": decision_id, "valid": True, "broken_at": None, "expected_hash": expected, "actual_hash": actual}

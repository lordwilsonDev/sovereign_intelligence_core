from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class IntegrityCheck:
    decision_id: str
    valid: bool
    broken_at: Optional[str]
    expected_hash: Optional[str]
    actual_hash: Optional[str]
    continuity: Dict[str, Any]


class IntegrityVerifier:
    def __init__(self, stream: Any) -> None:
        self.stream = stream

    def verify_decision(self, decision_id: str) -> IntegrityCheck:
        raw = self.stream.verify_integrity(decision_id)
        expected = raw.get("expected_hash")
        actual = raw.get("actual_hash") or self._digest_last(decision_id)
        valid = expected is None or expected == actual
        return IntegrityCheck(
            decision_id=raw["decision_id"],
            valid=valid,
            broken_at=None if valid else raw.get("broken_at"),
            expected_hash=expected,
            actual_hash=actual,
            continuity=self._continuity(self.stream.events_for_decision(decision_id)),
        )

    def verify_trace(self, trace_id: str) -> Dict[str, Any]:
        return self.stream.verify_continuity(trace_id)

    def batch_verify(self, decision_ids: List[str]) -> Dict[str, Any]:
        results = []
        for did in decision_ids:
            check = self.verify_decision(did)
            results.append(
                {
                    "decision_id": check.decision_id,
                    "valid": check.valid,
                    "broken_at": check.broken_at,
                    "expected_hash": check.expected_hash,
                    "actual_hash": check.actual_hash,
                    "continuity": check.continuity,
                }
            )
        return {"count": len(results), "results": results}

    def _continuity(self, events: List[Any]) -> Dict[str, Any]:
        sequences = [getattr(e, "sequence", None) or 0 for e in events]
        expected = list(range(1, len(sequences) + 1))
        if not sequences:
            return {"continuous": True, "count": 0, "gaps": []}
        continuous = sequences == expected
        gaps = [] if continuous else [i for i, s in enumerate(sequences) if s != expected[i]]
        return {
            "continuous": continuous,
            "count": len(events),
            "first_seq": sequences[0] if sequences else None,
            "last_seq": sequences[-1] if sequences else None,
            "gaps": gaps,
        }

    def _digest_last(self, decision_id: str) -> Optional[str]:
        events = self.stream.events_for_decision(decision_id)
        if not events:
            return None
        return self._digest_event(events[0])

    def _digest_event(self, event: Any) -> Optional[str]:
        return event.integrity_hash or getattr(event, "integrity_hash", None)

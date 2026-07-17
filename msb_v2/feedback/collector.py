from __future__ import annotations

import json as _json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from msb_v2.memory.types import MemoryKind, MemoryRecord, MemoryConfidence


@dataclass
class CorrectionEvent:
    original_query: str
    original_answer: str
    corrected_answer: str
    user_id: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
    context: Dict[str, Any] = field(default_factory=dict)
    verification_report_hash: Optional[str] = None


class FeedbackCollector:
    def __init__(self, event_bus: Any, memory_store: Any) -> None:
        self.event_bus = event_bus
        self.memory_store = memory_store

    def start(self) -> None:
        self.event_bus.subscribe("user_correction", self._on_correction)

    def stop(self) -> None:
        self.event_bus.clear("user_correction")

    def _on_correction(self, event: Any) -> None:
        payload = getattr(event, "payload", {}) or {}
        try:
            correction = CorrectionEvent(
                original_query=payload["original_query"],
                original_answer=payload["original_answer"],
                corrected_answer=payload["corrected_answer"],
                user_id=payload.get("user_id"),
                context=payload.get("context", {}),
                verification_report_hash=payload.get("verification_report_hash"),
            )
            self.memory_store.add(
                MemoryRecord(
                    id=f"feedback-{int(correction.timestamp * 1000)}",
                    kind=MemoryKind.EPISODIC,
                    content=self._content(correction),
                    confidence=MemoryConfidence(),
                    tags=["feedback", "correction"],
                    provenance=correction.verification_report_hash or "",
                )
            )
        except Exception:
            pass

    def ingest_direct(self, payload: Dict[str, Any]) -> Optional[str]:
        record_id = f"direct-fb-{int(time.time() * 1000)}"
        try:
            self.memory_store.add(
                MemoryRecord(
                    id=record_id,
                    kind=MemoryKind.EPISODIC,
                    content=_json.dumps(
                        {
                            "type": "feedback",
                            "source": payload.get("source", "direct"),
                            "summary": payload.get("summary", ""),
                            "payload": payload,
                            "timestamp": time.time(),
                            "user_id": payload.get("user_id"),
                        }
                    ),
                    confidence=MemoryConfidence(),
                    tags=["feedback", "direct"],
                )
            )
        except Exception:
            record_id = None
        return record_id

    def summary(self) -> Dict[str, Any]:
        try:
            items = self.memory_store.search("feedback", limit=50)
        except Exception:
            items = []
        return {
            "feedback_count": len(items),
            "latest": [getattr(item, "id", None) for item in items[:5]],
        }

    @staticmethod
    def _content(correction: CorrectionEvent) -> str:
        data = {
            "type": "correction",
            "original_query": correction.original_query,
            "original_answer": correction.original_answer,
            "corrected_answer": correction.corrected_answer,
            "user_id": correction.user_id,
            "timestamp": correction.timestamp,
            "context": correction.context,
            "verification_report_hash": correction.verification_report_hash,
        }
        return _json.dumps(data)

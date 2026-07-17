from __future__ import annotations

from typing import Any, Dict, Optional

from msb_v2.verification.capability_registry import CapabilityRegistry
from msb_v2.verification.evidence import EvidenceEngine
from msb_v2.feedback.collector import FeedbackCollector


class VerificationFeedbackExtension:
    """Opt-in extension holding verification + feedback components."""

    def __init__(self) -> None:
        self.capability_registry = CapabilityRegistry()
        self.feedback_collector: Optional[FeedbackCollector] = None
        self.evidence_engine: Optional[EvidenceEngine] = None

    def wire(self, *, memory_client: Any, event_bus: Any) -> None:
        self.feedback_collector = FeedbackCollector(
            event_bus=event_bus,
            memory_store=memory_client,
        )
        self.evidence_engine = EvidenceEngine(
            registry=self.capability_registry,
            memory_client=memory_client,
        )

    def start(self) -> None:
        if self.feedback_collector is not None:
            self.feedback_collector.start()

    def stop(self) -> None:
        if self.feedback_collector is not None:
            self.feedback_collector.stop()

    def summary(self) -> Dict[str, Any]:
        if self.feedback_collector is None:
            return {"feedback_count": 0, "latest": []}
        return self.feedback_collector.summary()

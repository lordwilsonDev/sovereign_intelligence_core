from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from msb_v2.reasoning.integrity import EventKind, EventStreamStore


@dataclass(frozen=True)
class ReasoningMetrics:
    total_traces: int = 0
    active_traces: int = 0
    total_events: int = 0
    avg_score: float = 0.0
    avg_confidence: float = 0.0
    avg_entropy: float = 0.0
    drift_count: int = 0
    counterfactual_count: int = 0
    assessment_count: int = 0
    error_count: int = 0
    tool_call_count: int = 0
    memory_read_count: int = 0
    human_feedback_count: int = 0
    budget_breaches: int = 0
    budget_health: float = 1.0
    ts: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat() + "Z")

    def payload(self) -> dict[str, object]:
        return {
            "total_traces": self.total_traces,
            "active_traces": self.active_traces,
            "total_events": self.total_events,
            "avg_score": round(self.avg_score, 4),
            "avg_confidence": round(self.avg_confidence, 4),
            "avg_entropy": round(self.avg_entropy, 4),
            "drift_count": self.drift_count,
            "counterfactual_count": self.counterfactual_count,
            "assessment_count": self.assessment_count,
            "error_count": self.error_count,
            "tool_call_count": self.tool_call_count,
            "memory_read_count": self.memory_read_count,
            "human_feedback_count": self.human_feedback_count,
            "budget_breaches": self.budget_breaches,
            "budget_health": round(self.budget_health, 4),
            "ts": self.ts,
        }


@dataclass(frozen=True)
class MemoryMetrics:
    total_memories: int = 0
    active_memories: int = 0
    archived_memories: int = 0
    avg_source_reliability: float = 0.0
    verification_rate: float = 0.0
    ts: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat() + "Z")

    def payload(self) -> dict[str, object]:
        return {
            "total_memories": self.total_memories,
            "active_memories": self.active_memories,
            "archived_memories": self.archived_memories,
            "avg_source_reliability": round(self.avg_source_reliability, 4),
            "verification_rate": round(self.verification_rate, 4),
            "ts": self.ts,
        }


class MetricsStore:
    def __init__(self) -> None:
        self.reasoning = ReasoningMetrics()
        self.memory = MemoryMetrics()

    def recompute(self, stream: EventStreamStore, memory_store: Any | None = None) -> tuple[ReasoningMetrics, MemoryMetrics]:
        events = stream.global_stream(limit=10000)
        trace_ids: set[str] = set()
        scores: list[float] = []
        confidences: list[float] = []
        entropies: list[float] = []
        drift_count = 0
        counterfactual_count = 0
        assessment_count = 0
        error_count = 0
        tool_call_count = 0
        memory_read_count = 0
        human_feedback_count = 0
        budget_breach = False

        for event in events:
            trace_id = event.trace_id or event.decision_id
            if trace_id:
                trace_ids.add(trace_id)
            if event.kind == EventKind.CONFIDENCE_ASSESSMENT:
                assessment_count += 1
                payload = event.payload or {}
                if "score" in payload:
                    scores.append(float(payload["score"]))
                if "confidence" in payload:
                    confidences.append(float(payload["confidence"]))
                if "entropy" in payload:
                    entropies.append(float(payload["entropy"]))
            elif event.kind == EventKind.DRIFT:
                drift_count += 1
            elif event.kind == EventKind.ERROR:
                error_count += 1
            elif event.kind == EventKind.TOOL:
                tool_call_count += 1
            elif event.kind == EventKind.MEMORY_READ:
                memory_read_count += 1
            elif event.kind == EventKind.HUMAN:
                human_feedback_count += 1
            elif event.kind == EventKind.ALERT:
                source = str(event.source or "")
                payload = event.payload or {}
                if "budget" in source or "budget" in str(payload):
                    budget_breach = True

        reasoning = ReasoningMetrics(
            total_traces=len(trace_ids),
            active_traces=len(trace_ids),
            total_events=len(events),
            avg_score=sum(scores) / len(scores) if scores else 0.0,
            avg_confidence=sum(confidences) / len(confidences) if confidences else 0.0,
            avg_entropy=sum(entropies) / len(entropies) if entropies else 0.0,
            drift_count=drift_count,
            counterfactual_count=counterfactual_count,
            assessment_count=assessment_count,
            error_count=error_count,
            tool_call_count=tool_call_count,
            memory_read_count=memory_read_count,
            human_feedback_count=human_feedback_count,
            budget_breaches=1 if budget_breach else 0,
            budget_health=0.0 if budget_breach else 1.0,
        )

        memory = MemoryMetrics()
        if memory_store is not None:
            all_memories = memory_store.all() if hasattr(memory_store, "all") else []
            if all_memories:
                active = [m for m in all_memories if getattr(getattr(m, "status", None), "value", getattr(m, "status", "")) == "active"]
                archived = [m for m in all_memories if getattr(getattr(m, "status", None), "value", getattr(m, "status", "")) == "archived"]
                verified = [m for m in all_memories if getattr(getattr(m, "confidence", None), "verified", False)]
                rels = [getattr(getattr(m, "confidence", None), "source_reliability", 0.0) for m in all_memories]
                memory = MemoryMetrics(
                    total_memories=len(all_memories),
                    active_memories=len(active),
                    archived_memories=len(archived),
                    avg_source_reliability=sum(rels) / len(rels) if rels else 0.0,
                    verification_rate=len(verified) / len(all_memories) if all_memories else 0.0,
                )

        self.reasoning = reasoning
        self.memory = memory
        return reasoning, memory

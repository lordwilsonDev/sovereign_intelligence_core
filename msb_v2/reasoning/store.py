from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from msb_v2.reasoning.types import (
    ReasoningTrace,
    ReasoningStatus,
)


@dataclass(frozen=True)
class ReasoningRef:
    decision_id: str
    trace_id: str | None = None
    memory_ids: tuple[str, ...] = ()
    action: str = ""
    evidence: tuple[str, ...] = ()


SEED: list[ReasoningTrace] = []


class ReasoningStore:
    """Append-only reasoning trace store backed by memory."""

    def __init__(self, traces: list[ReasoningTrace] | None = None) -> None:
        self._traces: dict[str, ReasoningTrace] = {t.trace_id: t for t in (traces or SEED)}
        self._refs: dict[str, list[ReasoningRef]] = {}
        self._sequence = 0

    def add_trace(self, trace: ReasoningTrace) -> ReasoningTrace:
        if trace.trace_id in self._traces:
            raise KeyError(f"trace already exists: {trace.trace_id}")
        now = datetime.utcnow().isoformat() + "Z"
        normalized = ReasoningTrace(
            trace_id=trace.trace_id,
            title=trace.title,
            status=trace.status,
            steps=trace.steps,
            decision_id=trace.decision_id,
            memory_ids=trace.memory_ids,
            conclusion=trace.conclusion,
            created_at=trace.created_at or now,
            updated_at=trace.updated_at or now,
            metadata=trace.metadata,
        )
        if not normalized.steps:
            raise ValueError("trace requires at least one step")
        self._traces[normalized.trace_id] = normalized
        if normalized.decision_id:
            self._refs.setdefault(normalized.decision_id, []).append(
                ReasoningRef(decision_id=normalized.decision_id, trace_id=normalized.trace_id, memory_ids=normalized.memory_ids)
            )
        for mid in normalized.memory_ids:
            self._refs.setdefault(mid, []).append(
                ReasoningRef(decision_id=normalized.decision_id or "", trace_id=normalized.trace_id, memory_ids=(mid,))
            )
        return normalized

    def get_trace(self, trace_id: str) -> ReasoningTrace:
        try:
            return self._traces[trace_id]
        except KeyError:
            raise KeyError(f"trace not found: {trace_id}")

    def list_traces(self, status: ReasoningStatus | None = None) -> list[ReasoningTrace]:
        traces = list(self._traces.values())
        if status is not None:
            traces = [t for t in traces if t.status == status]
        return sorted(traces, key=lambda t: t.created_at)

    def set_status(self, trace_id: str, status: ReasoningStatus) -> ReasoningTrace:
        trace = self.get_trace(trace_id)
        updated = ReasoningTrace(
            trace_id=trace.trace_id,
            title=trace.title,
            status=status,
            steps=trace.steps,
            decision_id=trace.decision_id,
            memory_ids=trace.memory_ids,
            conclusion=trace.conclusion,
            created_at=trace.created_at,
            updated_at=datetime.utcnow().isoformat() + "Z",
            metadata=trace.metadata,
        )
        self._traces[trace_id] = updated
        return updated

    def backfill_decision(self, trace_id: str, decision_id: str) -> ReasoningTrace:
        trace = self.get_trace(trace_id)
        if not trace.decision_id:
            updated = ReasoningTrace(
                trace_id=trace.trace_id,
                title=trace.title,
                status=trace.status,
                steps=trace.steps,
                decision_id=decision_id,
                memory_ids=trace.memory_ids,
                conclusion=trace.conclusion,
                created_at=trace.created_at,
                updated_at=datetime.utcnow().isoformat() + "Z",
                metadata=trace.metadata,
            )
            self._traces[trace_id] = updated
            trace = updated
            self._refs.setdefault(decision_id, []).append(
                ReasoningRef(decision_id=decision_id, trace_id=trace_id, memory_ids=trace.memory_ids)
            )
        return trace

    def refs_for(self, ref_id: str) -> list[ReasoningRef]:
        return list(self._refs.get(ref_id, []))

    def next_trace_id(self) -> str:
        self._sequence += 1
        return f"rtrace-{self._sequence:04d}"

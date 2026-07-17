from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class PhaseSpan:
    phase: str
    started_at: str
    finished_at: str = ""
    duration_ms: float = 0.0
    evidence_count: int = 0
    assumption_count: int = 0
    tool_calls: int = 0
    result: str = "unknown"
    metadata: dict[str, Any] = field(default_factory=dict)


class PhaseTracer:
    def __init__(self) -> None:
        self.spans: list[PhaseSpan] = []

    def begin(self, phase: str, **meta: Any) -> PhaseSpan:
        span = PhaseSpan(
            phase=phase,
            started_at=datetime.now(timezone.utc).isoformat(),
            metadata=meta or {},
        )
        self.spans.append(span)
        return span

    def end(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def export(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "phase": s.phase,
                    "started_at": s.started_at,
                    "finished_at": s.finished_at,
                    "duration_ms": s.duration_ms,
                    "evidence_count": s.evidence_count,
                    "assumption_count": s.assumption_count,
                    "tool_calls": s.tool_calls,
                    "result": s.result,
                    "metadata": s.metadata,
                }
            )
        return out

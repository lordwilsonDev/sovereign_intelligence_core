from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Span:
    trace_id: str
    name: str
    agent: str
    status: str = "started"
    started_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    finished_at: str = ""
    attributes: Dict[str, Any] = field(default_factory=dict)


class BasicTracer:
    def __init__(self) -> None:
        self.spans: List[Span] = []
        self.traces: Dict[str, List[Span]] = {}

    def start(self, trace_id: str, name: str, agent: str, attributes: Optional[Dict[str, Any]] = None) -> Span:
        span = Span(trace_id=trace_id, name=name, agent=agent, attributes=attributes or {})
        self.spans.append(span)
        self.traces.setdefault(trace_id, []).append(span)
        return span

    def finish(self, span: Span, status: str = "ok", error: Optional[str] = None) -> Dict[str, Any]:
        span.status = status
        span.finished_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        if error:
            span.attributes["error"] = error
        return {
            "trace_id": span.trace_id,
            "span": span.name,
            "agent": span.agent,
            "status": span.status,
            "started_at": span.started_at,
            "finished_at": span.finished_at,
            "attributes": span.attributes,
        }

    def metrics(self) -> Dict[str, Any]:
        return {
            "span_count": len(self.spans),
            "trace_count": len(self.traces),
            "avg_trace_spans": (len(self.spans) / len(self.traces)) if self.traces else 0,
            "ok_count": sum(1 for s in self.spans if s.status == "ok"),
            "error_count": sum(1 for s in self.spans if s.status != "ok" and s.status != "started"),
        }

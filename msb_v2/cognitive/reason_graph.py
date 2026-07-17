from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class ReasonGraph:
    trace_id: str
    title: str
    steps: List[Dict[str, Any]]
    score: float
    confidence: float
    entropy: float
    conclusion: str = ""


def from_trace(trace: Any) -> ReasonGraph:
    steps = [
        {
            "step_index": step.step_index,
            "claim": step.claim,
            "evidence_refs": list(step.evidence_refs),
            "assumptions": list(step.assumptions),
            "confidence": step.confidence,
        }
        for step in getattr(trace, "steps", [])
    ]
    return ReasonGraph(
        trace_id=trace.trace_id,
        title=getattr(trace, "title", ""),
        steps=steps,
        score=getattr(trace, "metadata", {}).get("score", 0.0),
        confidence=getattr(trace, "metadata", {}).get("confidence", 0.0),
        entropy=getattr(trace, "metadata", {}).get("entropy", 0.0),
        conclusion=trace.conclusion or "",
    )


def from_traces(traces: List[Any]) -> List[ReasonGraph]:
    return [from_trace(trace) for trace in traces]

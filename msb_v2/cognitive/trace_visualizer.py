from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class TraceStepView:
    step_index: int
    claim: str
    confidence: float
    verdict: str = ""
    risk: str = "low"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_index": self.step_index,
            "claim": self.claim,
            "confidence": self.confidence,
            "verdict": self.verdict,
            "risk": self.risk,
        }


@dataclass
class TraceVisualization:
    trace_id: str
    title: str
    status: str
    conclusion: str
    score: float
    confidence: float
    entropy: float
    steps: List[TraceStepView]
    critical_path: List[int]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "title": self.title,
            "status": self.status,
            "conclusion": self.conclusion,
            "score": self.score,
            "confidence": self.confidence,
            "entropy": self.entropy,
            "steps": [step.to_dict() for step in self.steps],
            "critical_path": self.critical_path,
        }


@dataclass
class ConfidenceTimeline:
    trace_id: str
    events: List[Dict[str, Any]]
    milestones: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "events": self.events,
            "milestones": self.milestones,
        }

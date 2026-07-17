from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class EvidenceReport:
    query: str
    answer: str
    confidence: float = 0.0
    consistency: float = 0.0
    novelty: float = 0.0
    trace_depth: int = 0
    verification_score: float = 0.0
    falsification_score: float = 0.0
    uncertainty: float = 0.0
    memory_support: List[str] = field(default_factory=list)
    tool_support: List[str] = field(default_factory=list)
    human_validation: Optional[bool] = None
    provenance: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
    additional_metrics: Dict[str, float] = field(default_factory=dict)

    def compute_hash(self) -> str:
        data = {
            "query": self.query,
            "answer": self.answer,
            "confidence": self.confidence,
            "consistency": self.consistency,
            "novelty": self.novelty,
            "trace_depth": self.trace_depth,
            "verification_score": self.verification_score,
            "falsification_score": self.falsification_score,
            "uncertainty": self.uncertainty,
            "memory_support": sorted(self.memory_support),
            "tool_support": sorted(self.tool_support),
            "human_validation": self.human_validation,
            "provenance": sorted(self.provenance),
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


class EvidenceEngine:
    def __init__(self, registry: Any, memory_client: Any) -> None:
        self.registry = registry
        self.memory = memory_client
        self._cache: Dict[str, EvidenceReport] = {}

    def evaluate(self, query: str, answer: str, trace: Dict[str, Any]) -> EvidenceReport:
        confidence = float(trace.get("confidence", 0.8))
        consistency = self._compute_consistency(query, answer)
        novelty = self._compute_novelty(query, answer)
        trace_depth = len(trace.get("steps", []))
        benchmark_scores = self.registry.get_scores()
        avg_score = sum(benchmark_scores.values()) / len(benchmark_scores) if benchmark_scores else 0.5

        report = EvidenceReport(
            query=query,
            answer=answer,
            confidence=confidence,
            consistency=consistency,
            novelty=novelty,
            trace_depth=trace_depth,
            verification_score=avg_score,
            falsification_score=1.0 - confidence,
            uncertainty=(1.0 - confidence) * 0.5 + (1.0 - consistency) * 0.5,
            memory_support=self._retrieve_memory_support(query),
            tool_support=list(trace.get("tool_calls", [])),
            provenance=list(trace.get("provenance", [])),
            additional_metrics={"avg_benchmark": avg_score},
        )
        self._cache[report.compute_hash()] = report
        return report

    def _compute_consistency(self, query: str, answer: str) -> float:
        return 0.9

    def _compute_novelty(self, query: str, answer: str) -> float:
        return 0.5

    def _retrieve_memory_support(self, query: str) -> List[str]:
        try:
            return [m.id for m in self.memory.search(query, limit=5)]
        except Exception:
            return []

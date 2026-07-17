from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class DecisionNode:
    decision_id: str
    trace_id: Optional[str]
    status: str
    source: str = ""
    score: float = 0.0
    confidence: float = 0.0
    entropy: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ReasonEdge:
    source_id: str
    target_id: str
    weight: float = 1.0
    kind: str = "supports"


class DependencyGraph:
    def __init__(self) -> None:
        self._nodes: Dict[str, DecisionNode] = {}
        self._edges: List[ReasonEdge] = []

    def add(self, node: DecisionNode) -> None:
        self._nodes[node.decision_id] = node

    def link(self, edge: ReasonEdge) -> None:
        if edge.source_id not in self._nodes or edge.target_id not in self._nodes:
            raise KeyError("both source and target decisions must exist")
        self._edges.append(edge)

    def predecessors(self, decision_id: str) -> List[DecisionNode]:
        return [self._nodes[e.source_id] for e in self._edges if e.target_id == decision_id]

    def successors(self, decision_id: str) -> List[DecisionNode]:
        return [self._nodes[e.target_id] for e in self._edges if e.source_id == decision_id]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": [
                {
                    "decision_id": node.decision_id,
                    "trace_id": node.trace_id,
                    "status": node.status,
                    "source": node.source,
                    "score": node.score,
                    "confidence": node.confidence,
                    "entropy": node.entropy,
                }
                for node in self._nodes.values()
            ],
            "edges": [
                {
                    "source": edge.source_id,
                    "target": edge.target_id,
                    "weight": edge.weight,
                    "kind": edge.kind,
                }
                for edge in self._edges
            ],
        }


DecisionGraph = DependencyGraph
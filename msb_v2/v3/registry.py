from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class AutonomyLevel(str, Enum):
    OBSERVE = "observe"
    RECOMMEND = "recommend"
    DRAFT = "draft"
    CONFIRM = "execute_with_confirmation"
    POLICY = "execute_within_policy"
    AUTONOMOUS = "autonomous_execution"


@dataclass(frozen=True)
class CapabilityNode:
    capability_id: str
    name: str
    description: str
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    cost_estimate: float = 0.0
    latency_p95_ms: float = 0.0
    reliability: float = 1.0
    failure_modes: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    confidence: float = 0.0
    version: str = "0.1.0"
    autonomy_level: AutonomyLevel = AutonomyLevel.POLICY
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


class CapabilityRegistry:
    def __init__(self) -> None:
        self._nodes: Dict[str, CapabilityNode] = {}

    def register(self, node: CapabilityNode) -> CapabilityNode:
        self._nodes[node.capability_id] = node
        return node

    def get(self, capability_id: str) -> Optional[CapabilityNode]:
        return self._nodes.get(capability_id)

    def list(self) -> List[CapabilityNode]:
        return list(self._nodes.values())

    def dependencies(self, capability_id: str) -> List[CapabilityNode]:
        node = self.get(capability_id)
        if node is None:
            return []
        return [self._nodes[d] for d in node.dependencies if d in self._nodes]

    def summary(self) -> Dict[str, Any]:
        return {
            "count": len(self._nodes),
            "by_autonomy": self._autonomy_counts(),
            "avg_confidence": self._avg(lambda n: n.confidence),
            "avg_reliability": self._avg(lambda n: n.reliability),
        }

    def _autonomy_counts(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for node in self._nodes.values():
            counts[node.autonomy_level.value] = counts.get(node.autonomy_level.value, 0) + 1
        return counts

    def _avg(self, fn) -> float:
        vals = [fn(n) for n in self._nodes.values() if n is not None]
        return round(sum(vals) / len(vals), 4) if vals else 0.0


_registry: CapabilityRegistry | None = None


def get_registry() -> CapabilityRegistry:
    global _registry
    if _registry is None:
        _registry = CapabilityRegistry()
        _registry.register(CapabilityNode(
            capability_id="cap:brain:run",
            name="Brain Run",
            description="Unified cognitive entrypoint",
            inputs=["query", "intent"],
            outputs=["task_id", "trace_id", "metrics"],
            cost_estimate=0.01,
            latency_p95_ms=120.0,
            reliability=0.99,
            confidence=0.9,
            autonomy_level=AutonomyLevel.POLICY,
        ))
        _registry.register(CapabilityNode(
            capability_id="cap:runtime:snapshot",
            name="Runtime Snapshot",
            description="Snapshot and rollback runtime state",
            inputs=["tag", "source"],
            outputs=["tag"],
            cost_estimate=0.02,
            latency_p95_ms=250.0,
            reliability=0.98,
            failure_modes=["non_copyable_path", "disk_full"],
            dependencies=["cap:runtime:status"],
            confidence=0.85,
            autonomy_level=AutonomyLevel.CONFIRM,
        ))
        _registry.register(CapabilityNode(
            capability_id="cap:agent:plan",
            name="Agent Plan",
            description="Decompose goal into plan",
            inputs=["goal"],
            outputs=["steps"],
            cost_estimate=0.01,
            latency_p95_ms=80.0,
            reliability=0.97,
            confidence=0.8,
            autonomy_level=AutonomyLevel.POLICY,
        ))
    return _registry

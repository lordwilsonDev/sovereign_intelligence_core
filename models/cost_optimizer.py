from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from models.registry import RegisteredModel


@dataclass
class TaskRequirements:
    task_type: str
    latency_budget_ms: float = 2000.0
    confidence_threshold: float = 0.8
    max_cost: Optional[float] = None


@dataclass
class ModelScore:
    model: str
    provider: str
    cost: float
    estimated_latency_ms: float
    confidence: float
    capability_fit: float
    capabilities: List[str] = field(default_factory=list)


class CostOptimizer:
    def __init__(self, default_cap: float = 0.75) -> None:
        self.default_cap = default_cap

    def score(self, model: "RegisteredModel", req: TaskRequirements) -> ModelScore:
        latency_score = max(0.0, min(1.0, 1.0 - (req.latency_budget_ms - self._estimate_latency(model)) / req.latency_budget_ms))
        confidence_score = max(0.0, min(1.0, 1.0 - model.capabilities.cost_per_1k_tokens / max(req.confidence_threshold, 0.01)))
        capability_keys = ["reasoning", "extraction", "classification", "coding"]
        capability_hits = [k for k in capability_keys if getattr(model.capabilities, k, False)]
        capability_fit = float(len(capability_hits) / max(len(capability_keys), 1))
        return ModelScore(
            model=model.name,
            provider=model.provider,
            cost=model.capabilities.cost_per_1k_tokens,
            estimated_latency_ms=self._estimate_latency(model),
            confidence=round(confidence_score, 4),
            capability_fit=round(capability_fit, 4),
            capabilities=capability_hits,
        )

    def _estimate_latency(self, model: "RegisteredModel") -> float:
        return 250.0 if model.provider == "local" else 900.0

#!/usr/bin/env python3
"""
ROUTER OBSERVER – records meta-routing decisions for calibration, debugging, and falsification tracking.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from cognitive_compiler.meta_router_v2 import MetaRoutingResult


@dataclass
class RoutingObservation:
    query: str
    primary: str
    secondary: Optional[str]
    order: str
    confidence: float
    justification: str
    rerouted: bool
    temperature_score: float
    elapsed_s: float


class RouterObserver:
    def __init__(self, log_path: str = "runtime/meta_routing_observations.jsonl"):
        self.log_path = log_path
        self.buffer: List[RoutingObservation] = []

    def record(self, result: "MetaRoutingResult", query: str) -> None:
        obs = RoutingObservation(
            query=query,
            primary=result.decision.primary,
            secondary=result.decision.secondary,
            order=result.decision.order,
            confidence=result.decision.confidence,
            justification=result.decision.justification,
            rerouted=result.rerouted,
            temperature_score=result.temperature.score,
            elapsed_s=result.elapsed_s,
        )
        self.buffer.append(obs)
        self._flush(obs)

    def summarize(self, last_n: int = 20) -> Dict[str, float]:
        recent = self.buffer[-last_n:]
        if not recent:
            return {"count": 0.0, "rerouted_rate": 0.0, "hybrid_rate": 0.0, "avg_confidence": 0.0}
        hybrid = [r for r in recent if r.secondary]
        rerouted = [r for r in recent if r.rerouted]
        avg_conf = sum(r.confidence for r in recent) / len(recent)
        return {
            "count": len(recent),
            "rerouted_rate": len(rerouted) / len(recent),
            "hybrid_rate": len(hybrid) / len(recent),
            "avg_confidence": round(avg_conf, 2),
        }

    def _flush(self, obs: RoutingObservation) -> None:
        os.makedirs(os.path.dirname(self.log_path) or ".", exist_ok=True)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "query": obs.query,
                "primary": obs.primary,
                "secondary": obs.secondary,
                "order": obs.order,
                "confidence": obs.confidence,
                "justification": obs.justification,
                "rerouted": obs.rerouted,
                "temperature_score": obs.temperature_score,
                "elapsed_s": obs.elapsed_s,
            }) + "\n")

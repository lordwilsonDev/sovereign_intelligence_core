#!/usr/bin/env python3
"""
ROUTER OBSERVER – records meta-routing decisions for calibration, debugging, and falsification tracking.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

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

    def record(self, result: Any, query: str) -> None:
        routing = result.decision if hasattr(result, "decision") else result
        if hasattr(routing, "primary"):
            primary = routing.primary or "base_are"
            secondary = routing.secondary
            order = routing.order or "serial"
            confidence = routing.confidence or 0.0
            justification = routing.justification or ""
            rerouted = bool(getattr(routing, "rerouted", False))
        elif isinstance(routing, dict):
            primary = routing.get("primary") or "base_are"
            secondary = routing.get("secondary")
            order = routing.get("order") or "serial"
            confidence = routing.get("confidence") or 0.0
            justification = routing.get("justification") or ""
            rerouted = bool(routing.get("rerouted"))
        else:
            return
        if hasattr(result, "temperature") and hasattr(result.temperature, "score"):
            temp_score = result.temperature.score
        elif isinstance(result, dict):
            temp_score = result.get("temperature", {}).get("score", 0.0)
        else:
            temp_score = 0.0
        elapsed = getattr(result, "elapsed_s", result.get("elapsed_s", 0.0) if isinstance(result, dict) else 0.0)
        obs = RoutingObservation(
            query=query,
            primary=primary,
            secondary=secondary,
            order=order,
            confidence=confidence,
            justification=justification,
            rerouted=rerouted,
            temperature_score=temp_score,
            elapsed_s=elapsed,
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

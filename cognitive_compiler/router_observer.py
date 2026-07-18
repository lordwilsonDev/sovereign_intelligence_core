from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


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
    primary_execution_time_s: float = 0.0
    secondary_execution_time_s: float = 0.0
    primary_retries: int = 0
    secondary_retries: int = 0
    primary_fallback_reason: Optional[str] = None
    secondary_fallback_reason: Optional[str] = None
    primary_error_class: Optional[str] = None
    secondary_error_class: Optional[str] = None
    primary_tags: List[str] = field(default_factory=list)
    secondary_tags: List[str] = field(default_factory=list)


class RouterObserver:
    def __init__(self, log_path: str = "runtime/meta_routing_observations.jsonl") -> None:
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

        temp_score = 0.0
        elapsed = 0.0
        if hasattr(result, "temperature") and hasattr(result.temperature, "score"):
            temp_score = result.temperature.score
            elapsed = getattr(result, "elapsed_s", 0.0)
        elif isinstance(result, dict):
            temp_score = result.get("temperature", {}).get("score", 0.0)
            elapsed = result.get("elapsed_s", 0.0)

        primary_exec = 0.0
        secondary_exec = 0.0
        primary_retries = 0
        secondary_retries = 0
        primary_fallback = None
        secondary_fallback = None
        primary_error = None
        secondary_error = None
        primary_tags = []
        secondary_tags = []
        telemetry = result.get("telemetry") if isinstance(result, dict) else None
        if telemetry:
            pt = telemetry.get("primary") or {}
            st = telemetry.get("secondary") or {}
            primary_exec = float(pt.get("execution_time_s") or 0.0)
            secondary_exec = float(st.get("execution_time_s") or 0.0)
            primary_retries = int(pt.get("retries") or 0)
            secondary_retries = int(st.get("retries") or 0)
            primary_fallback = pt.get("fallback_reason")
            secondary_fallback = st.get("fallback_reason")
            primary_error = pt.get("error_class")
            secondary_error = st.get("error_class")
            primary_tags = list(pt.get("tags") or [primary])
            secondary_tags = list(st.get("tags") or ([secondary] if secondary else []))

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
            primary_execution_time_s=primary_exec,
            secondary_execution_time_s=secondary_exec,
            primary_retries=primary_retries,
            secondary_retries=secondary_retries,
            primary_fallback_reason=primary_fallback,
            secondary_fallback_reason=secondary_fallback,
            primary_error_class=primary_error,
            secondary_error_class=secondary_error,
            primary_tags=primary_tags,
            secondary_tags=secondary_tags,
        )
        self.buffer.append(obs)
        self._flush(obs)

    def summarize(self, last_n: int = 20) -> Dict[str, Any]:
        recent = self.buffer[-last_n:]
        if not recent:
            return {
                "count": 0.0,
                "rerouted_rate": 0.0,
                "hybrid_rate": 0.0,
                "avg_confidence": 0.0,
                "avg_primary_execution_time_s": 0.0,
                "avg_secondary_execution_time_s": 0.0,
                "primary_error_rate": 0.0,
                "secondary_error_rate": 0.0,
                "fallback_rate": 0.0,
            }
        hybrid = [r for r in recent if r.secondary]
        rerouted = [r for r in recent if r.rerouted]
        avg_conf = sum(r.confidence for r in recent) / len(recent)
        avg_primary_time = sum(r.primary_execution_time_s for r in recent) / len(recent)
        avg_secondary_time = sum(r.secondary_execution_time_s for r in recent) / len(recent)
        primary_errors = sum(1 for r in recent if r.primary_error_class and r.primary_error_class != "ok")
        secondary_errors = sum(1 for r in recent if r.secondary_error_class and r.secondary_error_class != "ok")
        fallbacks = sum(1 for r in recent if r.primary_fallback_reason)
        return {
            "count": len(recent),
            "rerouted_rate": len(rerouted) / len(recent),
            "hybrid_rate": len(hybrid) / len(recent),
            "avg_confidence": round(avg_conf, 2),
            "avg_primary_execution_time_s": round(avg_primary_time, 4),
            "avg_secondary_execution_time_s": round(avg_secondary_time, 4),
            "primary_error_rate": primary_errors / len(recent),
            "secondary_error_rate": secondary_errors / len(recent),
            "fallback_rate": fallbacks / len(recent),
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
                "primary_execution_time_s": obs.primary_execution_time_s,
                "secondary_execution_time_s": obs.secondary_execution_time_s,
                "primary_retries": obs.primary_retries,
                "secondary_retries": obs.secondary_retries,
                "primary_fallback_reason": obs.primary_fallback_reason,
                "secondary_fallback_reason": obs.secondary_fallback_reason,
                "primary_error_class": obs.primary_error_class,
                "secondary_error_class": obs.secondary_error_class,
                "primary_tags": obs.primary_tags,
                "secondary_tags": obs.secondary_tags,
            }) + "\n")

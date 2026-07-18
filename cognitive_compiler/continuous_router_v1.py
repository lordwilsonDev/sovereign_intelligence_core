#!/usr/bin/env python3
"""
CONTINUOUS ROUTING MODULE (CRM) v1.0
Outputs soft probability distributions over harnesses and composes weighted harness protocols.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

from cognitive_compiler.meta_coordinator_v3_2 import AxiomInversionEngine


@dataclass
class CRMRouting:
    harness_weights: Dict[str, float]
    primary: str
    secondary: Optional[str] = None
    degrade_to_discrete: bool = False
    confidence: float = 0.0


class ContinuousRoutingModule:
    """
    v1.0 soft router.
    """

    def __init__(self, ail: Optional[AxiomInversionEngine] = None):
        self.ail = ail or AxiomInversionEngine()
        self.harnesses = ["research", "building", "complex_reasoning", "base_are"]

    def route(self, query: str, context: Dict[str, Any] = None) -> CRMRouting:
        context = context or {}
        q = query.lower()
        weights = {h: 0.05 for h in self.harnesses}  # small prior

        self._add_keyword_signal(weights, q)
        self._add_structure_signal(weights, q, context)
        self._add_override(weights, context)
        self._normalize(weights)

        primary = max(weights, key=weights.get)
        secondary = sorted(weights, key=weights.get, reverse=True)[1]
        top = weights[primary]
        second = weights[secondary]
        confidence = round(top - second, 2)
        degrade = top < 0.30 or confidence <= 0.0

        if degrade:
            discrete = self._fallback_discrete(q)
            return CRMRouting(
                harness_weights=weights,
                primary=discrete.primary,
                secondary=discrete.secondary,
                degrade_to_discrete=True,
                confidence=discrete.confidence
            )

        return CRMRouting(
            harness_weights=weights,
            primary=primary,
            secondary=secondary if second > 0.15 else None,
            confidence=confidence
        )

    def _add_keyword_signal(self, weights: Dict[str, float], q: str):
        signals = {
            "research": sum(q.count(m) for m in ["research", "investigate", "study", "experiment", "hypothesis", "theory", "literature"]),
            "building": sum(q.count(m) for m in ["design", "build", "architect", "plan", "implement", "create", "api", "system"]),
            "complex_reasoning": sum(q.count(m) for m in ["ethics", "philosophy", "strategy", "concept", "paradox", "reconcile", "tension"]),
        }
        for h, s in signals.items():
            weights[h] += s * 0.25

    def _add_structure_signal(self, weights: Dict[str, float], q: str, context: Dict[str, Any]):
        if context.get("artifact_request") or any(k in q for k in ["produce", "deliver", "output", "plan"]):
            weights["building"] += 0.2
        if context.get("uncertainty") or any(k in q for k in ["why", "what causes", "investigate", "unknown"]):
            weights["research"] += 0.2
        if context.get("abstract") or any(k in q for k in ["should", "ethics", "meaning", "resolve"]):
            weights["complex_reasoning"] += 0.2

    def _add_override(self, weights: Dict[str, float], context: Dict[str, Any]):
        override = context.get("preferred_harness")
        if override and override in weights:
            weights[override] += 0.5

    def _normalize(self, weights: Dict[str, float]):
        total = sum(weights.values())
        if total > 0:
            for h in weights:
                weights[h] = round(weights[h] / total, 3)

    def _fallback_discrete(self, query: str) -> CRMRouting:
        q = query.lower()
        scores = {}
        buckets = {
            "research": ["research", "investigate", "study", "experiment", "hypothesis", "theory"],
            "building": ["design", "build", "architect", "plan", "implement", "create"],
            "complex_reasoning": ["ethics", "philosophy", "strategy", "concept", "paradox"],
        }
        for h, markers in buckets.items():
            scores[h] = sum(q.count(m) for m in markers)
        if not scores or max(scores.values()) == 0:
            return CRMRouting(harness_weights={"base_are": 1.0}, primary="base_are", confidence=0.7)
        primary = max(scores, key=scores.get)
        secondary = sorted(scores, key=scores.get, reverse=True)[1]
        primary_score = scores[primary]
        total = sum(scores.values())
        conf = round(primary_score / total, 2) if total else 0.7
        return CRMRouting(harness_weights={h: round(s / total, 3) for h, s in scores.items()}, primary=primary, secondary=secondary, confidence=conf)

    def compose_protocol(self, routing: CRMRouting) -> Dict[str, Any]:
        if routing.degrade_to_discrete:
            return {
                "mode": "discrete",
                "primary": routing.primary,
                "secondary": routing.secondary,
                "confidence": routing.confidence,
                "weights": routing.harness_weights
            }
        steps = []
        for h, w in sorted(routing.harness_weights.items(), key=lambda x: x[1], reverse=True):
            if w > 0.10:
                steps.append({"harness": h, "weight": w, "action": "integrate" if w < 0.5 else "primary_execute"})
        return {
            "mode": "continuous",
            "weights": routing.harness_weights,
            "steps": steps,
            "primary": routing.primary,
            "secondary": routing.secondary,
            "confidence": routing.confidence
        }

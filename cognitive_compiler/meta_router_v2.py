#!/usr/bin/env python3
"""
META-ROUTING HARNESS v2.0 – Axiomatic Reasoning Engine (ARE)
Persistent meta-layer that classifies tasks, launches harnesses, and monitors
cognitive temperature for dynamic re-routing.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

from cognitive_compiler.shared_cognitive_state import SharedCognitiveState


# ===========================================================================
# DATA STRUCTURES
# ===========================================================================

@dataclass
class HarnessDecision:
    primary: str
    secondary: Optional[str] = None
    order: str = "serial"  # serial | parallel
    confidence: float = 0.0
    justification: str = ""
    transition_predicate: Optional[str] = None
    rerouted: bool = False


@dataclass
class CognitiveTemperature:
    uncertainty_spike: bool = False
    logic_loop_failures: int = 0
    assumption_reconsiderations: int = 0
    current_harness: str = "base_are"
    score: float = 0.0  # 0..1, higher = more likely mismatch


@dataclass
class MetaRoutingResult:
    decision: HarnessDecision
    scs: SharedCognitiveState
    temperature: CognitiveTemperature
    rerouted: bool = False
    elapsed_s: float = 0.0


# ===========================================================================
# META-ROUTING HARNESS
# ===========================================================================

class MetaRoutingHarness:
    """
    v2.0 persistent meta-layer.
    """

    def __init__(self):
        self.keyword_map = {
            "research": ["research", "investigate", "study", "experiment", "hypothesis", "literature", "theory", "market research", "competitive analysis", "adoption forecast"],
            "building": ["design", "build", "architect", "plan", "implement", "create", "api", "system"],
            "complex_reasoning": ["ethics", "philosophy", "strategy", "concept", "paradox", "reconcile", "tension"],
            "desktop": ["desktop", "automation", "click", "type", "launch", "open app", "screenshot", "mouse", "ui", "finder", "browser", "electron"],
            "career": ["career", "job", "cv", "resume", "cover letter", "evaluate", "offer", "salary", "scan job", "portal", "ATS", "tracker"],
            "telegram": ["telegram", "artifact", "chart", "recipe", "shopping list", "miniapp", "webapp", "web app", "html", "widget"],
            "agentic-dev": ["agentic", "software development", "feature", "bug fix", "system design", "code review", "inversion", "MoIE", "developer"],
            "empirical-grounding": ["grounding", "empirical", "assumption", "falsif", "integrity", "reality test", "FTS", "debt", "startup viability", "cost model", "falsifiable prediction", "ethical risk"],
            "sovereign-finetune": ["fine-tune", "finetune", "model build", "dataset distillation", "train model", "unsloth", "SFT"],
            "base_are": [],
        }
        self.blocked_secondary_requires = {"NEURALAGENT_USER_ACCESS_TOKEN", "NEURALAGENT_THREAD_ID"}
        self.non_task_domains = {"desktop": ["ui", "screenshot", "mouse", "click", "launch", "open app", "finder", "browser"]}
        self.triviality_threshold_words = 10

    def _detect_explicit_override(self, context: Dict[str, Any]) -> Optional[str]:
        explicit = context.get("preferred_harness")
        if explicit:
            return explicit
        return None

    def _score_harness_matches(self, query: str) -> Dict[str, int]:
        q = query.lower()
        scores: Dict[str, int] = {}
        for harness, markers in self.keyword_map.items():
            if not markers:
                continue
            scores[harness] = sum(1 for m in markers if m in q)
        return scores

    def _resolve_classification(self, scores: Dict[str, int], query: str) -> HarnessDecision:
        q = query.lower()
        words = q.split()

        if len(words) < self.triviality_threshold_words and not any(
            marker in q for markers in self.keyword_map.values() for marker in markers
        ):
            return HarnessDecision(
                primary="base_are",
                confidence=0.9,
                justification="Trivial query: short, no domain markers"
            )

        if not scores or max(scores.values()) == 0:
            return HarnessDecision(primary="base_are", confidence=0.8, justification="No domain markers matched")

        best = max(scores, key=scores.get)
        best_score = scores[best]
        second = sorted(scores, key=scores.get, reverse=True)[1] if len(scores) > 1 else None
        second_score = scores.get(second, 0)

        total = sum(scores.values())
        confidence = best_score / total if total else 0.8

        if second and second_score > 0 and (best_score - second_score) <= 1:
            order = self._determine_order(best, second, q)
            return HarnessDecision(
                primary=best,
                secondary=second,
                order=order,
                confidence=min(confidence + 0.1, 0.79),
                justification=f"Close tie between {best} and {second}; hybrid with {order} execution"
            )

        if confidence >= 0.8:
            return HarnessDecision(primary=best, confidence=confidence, justification=f"Clear keyword match to {best}")
        if confidence >= 0.6:
            return HarnessDecision(primary=best, secondary=second, confidence=confidence, justification=f"Weak match; adding {second} support")
        return HarnessDecision(primary="base_are", confidence=confidence, justification="Low match; defaulting to base ARE")

    def classify(self, query: str, context: Dict[str, Any] = None) -> HarnessDecision:
        context = context or {}

        explicit = self._detect_explicit_override(context)
        if explicit:
            return HarnessDecision(
                primary=explicit,
                confidence=0.95,
                justification="User explicit override"
            )

        scores = self._score_harness_matches(query or "")
        return self._resolve_classification(scores, query or "")

    def _determine_order(self, primary: str, secondary: str, query: str) -> str:
        if self._is_serial_order(primary, secondary):
            return "serial"
        return "parallel"

    _NON_TELEGRAM_SERIAL_ORDER_PAIRS = frozenset({
        ("desktop", "building"),
        ("building", "desktop"),
        ("desktop", "research"),
        ("research", "desktop"),
        ("desktop", "complex_reasoning"),
        ("research", "complex_reasoning"),
        ("building", "complex_reasoning"),
    })
    _ALWAYS_SERIAL_HARNESSES = frozenset({"career", "telegram"})

    def _is_serial_order(self, primary: str, secondary: str) -> bool:
        if primary in self._ALWAYS_SERIAL_HARNESSES or secondary in self._ALWAYS_SERIAL_HARNESSES:
            return True
        return (primary, secondary) in self._NON_TELEGRAM_SERIAL_ORDER_PAIRS

    def monitor(self, scs: SharedCognitiveState) -> CognitiveTemperature:
        temp = CognitiveTemperature(current_harness=scs.routing_decision.get("primary", "base_are"))
        temp.logic_loop_failures = sum(1 for rec in scs.harness_history for _ in rec.unresolved_tensions)
        temp.assumption_reconsiderations = len(scs.open_assumptions)
        temp.uncertainty_spike = len(scs.moie_state.open_disputes) > 2
        temp.score = min(1.0, (temp.logic_loop_failures * 0.15) + (temp.assumption_reconsiderations * 0.05) + (0.3 if temp.uncertainty_spike else 0.0))
        return temp

    def execute(self, query: str, context: Optional[Dict[str, Any]] = None) -> MetaRoutingResult:
        start = time.time()
        context = context if context is not None else {}
        scs = SharedCognitiveState(problem_statement=query, context=context)
        decision = self.classify(query, context)
        scs.routing_decision = {
            "primary": decision.primary,
            "secondary": decision.secondary,
            "order": decision.order,
            "confidence": decision.confidence,
            "justification": decision.justification,
        }
        temperature = self.monitor(scs)
        rerouted = False
        if temperature.score > 0.5 and decision.primary != "base_are":
            prev = decision.primary
            decision.primary = "base_are"
            decision.secondary = prev
            decision.confidence = 0.6
            decision.justification += f"; rerouted by meta-layer due to cognitive temperature {temperature.score:.2f}"
            scs.routing_decision["primary"] = decision.primary
            scs.routing_decision["secondary"] = decision.secondary
            rerouted = True
        elapsed = round(time.time() - start, 4)
        return MetaRoutingResult(decision=decision, scs=scs, temperature=temperature, rerouted=rerouted, elapsed_s=elapsed)

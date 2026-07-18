#!/usr/bin/env python3
"""
HARNESS DISPATCHER v1.0
Dispatches queries to RESEARCH, BUILDING, COMPLEX REASONING, BASE ARE, or HYBRID.
Now accepts Shared Cognitive State (SCS) for hybrid handoff continuity.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from cognitive_compiler.shared_cognitive_state import SharedCognitiveState
from cognitive_compiler.meta_router_v2 import MetaRoutingHarness, MetaRoutingResult
from cognitive_compiler.research_harness_v1 import ResearchHarness
from cognitive_compiler.building_harness_v1 import BuildingHarness
from cognitive_compiler.meta_coordinator_v3_2 import MetaIntelligenceCoordinator, QueryType, IntelligenceLayer
from cognitive_compiler.cognitive_compiler_verifier_v1 import CognitiveCompilerVerifier


class HarnessDispatcher:
    """
    v1.0 dispatcher with SCS-aware hybrid execution.
    """

    def __init__(self, coordinator: Optional[MetaIntelligenceCoordinator] = None):
        self.meta = MetaRoutingHarness()
        self.research = ResearchHarness()
        self.building = BuildingHarness()
        self.coordinator = coordinator or MetaIntelligenceCoordinator(worker_count=2)
        self.verifier = CognitiveCompilerVerifier()

    def dispatch(self, query: str, context: Dict[str, Any] = None, scs: Optional[SharedCognitiveState] = None) -> Dict[str, Any]:
        context = context or {}
        meta = self.meta.execute(query, context)
        scs = scs or SharedCognitiveState(problem_statement=query)
        scs.routing_decision = {
            "primary": meta.decision.primary,
            "secondary": meta.decision.secondary,
            "order": meta.decision.order,
            "confidence": meta.decision.confidence,
            "justification": meta.decision.justification,
        }
        scs.context = context
        primary = meta.decision.primary
        secondary = meta.decision.secondary
        order = meta.decision.order
        result: Dict[str, Any] = {
            "routing": {
                "primary": primary,
                "secondary": secondary,
                "order": order,
                "confidence": meta.decision.confidence,
                "justification": meta.decision.justification,
                "rerouted": meta.rerouted,
            },
            "primary_output": None,
            "secondary_output": None,
            "scs_snapshot": scs.to_prompt_context(),
            "temperature": {
                "score": meta.temperature.score,
                "logic_loop_failures": meta.temperature.logic_loop_failures,
                "uncertainty_spike": meta.temperature.uncertainty_spike,
            },
            "telemetry": {
                "primary": {"execution_time_s": 0.0, "retries": 0, "fallback_reason": None, "error_class": None, "tags": [primary]},
                "secondary": {"execution_time_s": 0.0, "retries": 0, "fallback_reason": None, "error_class": None, "tags": [secondary]},
                "routing_confidence": meta.decision.confidence,
                "elapsed_s": meta.elapsed_s,
            },
            "elapsed_s": meta.elapsed_s,
        }

        if primary == "base_are":
            result["primary_output"] = self._base_are(query, context)
            scs.add_harness_output("base_are", result["primary_output"])
            return result

        start = time.time()
        primary_payload = self._run_primary(primary, query, context)
        elapsed = round(time.time() - start, 4)
        result["telemetry"]["primary"]["execution_time_s"] = elapsed
        result["telemetry"]["primary"]["tags"] = self._tags_for(primary)
        result["elapsed_s"] = elapsed + meta.elapsed_s
        result["primary_output"] = primary_payload
        scs.add_harness_output(primary, primary_payload)

        verification = self.verifier.verify(result, context)
        if verification is not None and not verification.ok:
            result["primary_output"] = {"verification": "blocked", "issues": verification.issues, "risk": verification.risk}
            result.setdefault("telemetry", {})["primary"]["error_class"] = "verification"
            result.setdefault("telemetry", {})["primary"]["fallback_reason"] = f"axiom_risk={verification.risk:.2f}"
            return self._post_process(result, meta)
            handoff_prompt = (
                "You are continuing a hybrid reasoning session.\n" + scs.to_prompt_context() +
                "\nIntegrate the prior reasoning and complete the secondary protocol."
            )
            secondary_start = time.time()
            secondary_payload = self._run_secondary(secondary, query, context, handoff_prompt)
            result["telemetry"]["secondary"]["execution_time_s"] = round(time.time() - secondary_start, 4)
            result["telemetry"]["secondary"]["tags"] = self._tags_for(secondary)
            result["secondary_output"] = secondary_payload
            scs.add_harness_output(secondary, secondary_payload)

        return self._post_process(result, meta)

    def _base_are(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        try:
            layer_map = {
                "graph": IntelligenceLayer.GRAPH,
                "memory": IntelligenceLayer.MEMORY,
                "decision": IntelligenceLayer.DECISION,
                "bus": IntelligenceLayer.BUS,
            }
            layers = [layer_map.get(k, IntelligenceLayer.COORDINATOR) for k in context.get("layers", ["graph", "memory", "decision"])]
            res = self.coordinator.query(
                query_type=QueryType.SYNTHESIZE,
                layers=layers,
                parameters={"query": query, **context},
                priority=context.get("priority", 5),
                timeout=context.get("timeout", 10.0),
            )
            return res.to_dict()
        except Exception as e:
            return {"error": str(e), "query": query}

    def _tags_for(self, harness: Optional[str]) -> List[str]:
        if not harness:
            return []
        mapping = {
            "research": ["research", "evidence-first"],
            "building": ["building", "implementation-first"],
            "desktop": ["desktop", "automation"],
            "career": ["career", "evaluation"],
            "telegram": ["telegram", "artifact", "miniapp", "visualization"],
            "base_are": ["base-are", "reasoning"],
        }
        return mapping.get(harness, [harness])

    def _run_primary(self, primary: Optional[str], query: str, context: Dict[str, Any]) -> Any:
        if primary == "research":
            return self.research.execute(query)
        if primary == "building":
            return self.building.execute(query, constraints=context.get("constraints", []))
        if primary == "desktop":
            from cognitive_compiler.desktop_harness_v1 import DesktopHarness
            return DesktopHarness().execute(query, timeout_s=float(context.get("timeout_s", 600.0)))
        if primary == "career":
            from cognitive_compiler.career_harness_v1 import CareerHarness
            project_root = context.get("career_project_root")
            return CareerHarness(project_root=project_root).execute(
                query,
                context={
                    "career_company": context.get("career_company", "Unknown"),
                    "career_role": context.get("career_role", "Unknown"),
                    "career_jd": context.get("career_jd", query),
                    "career_score": context.get("career_score"),
                    "confidence": context.get("confidence", 0.0),
                },
            ).payload
        if primary == "telegram":
            from cognitive_compiler.telegram_artifact_harness_v1 import TelegramArtifactHarness
            return TelegramArtifactHarness().execute(query, context=context).payload
        return self._base_are(query, context)

    def _run_secondary(self, secondary: Optional[str], query: str, context: Dict[str, Any], handoff_prompt: str) -> Any:
        if secondary == "research":
            return self.research.execute(query + "\n\nContext: " + context.get("problem_statement", query))
        if secondary == "building":
            return self.building.execute(query, constraints=context.get("constraints", []))
        if secondary == "desktop":
            from cognitive_compiler.desktop_harness_v1 import DesktopHarness
            return DesktopHarness().execute(query, timeout_s=float(context.get("timeout_s", 600.0)))
        if secondary == "career":
            from cognitive_compiler.career_harness_v1 import CareerHarness
            project_root = context.get("career_project_root")
            return CareerHarness(project_root=project_root).execute(
                query,
                context={
                    "career_company": context.get("career_company", "Unknown"),
                    "career_role": context.get("career_role", "Unknown"),
                    "career_jd": context.get("career_jd", query),
                    "career_score": context.get("career_score"),
                    "confidence": context.get("confidence", 0.0),
                },
            ).payload
        if secondary == "telegram":
            from cognitive_compiler.telegram_artifact_harness_v1 import TelegramArtifactHarness
            return TelegramArtifactHarness().execute(query, context=context).payload
        return self._base_are(handoff_prompt, context)

    def _post_process(self, result: Dict[str, Any], meta: MetaRoutingResult) -> Dict[str, Any]:
        if "memory_bytes" not in result["telemetry"]["primary"]:
            try:
                import sys as _sys
                result["telemetry"]["primary"]["memory_bytes"] = _sys.getsizeof(result)
            except Exception:
                pass
        return result

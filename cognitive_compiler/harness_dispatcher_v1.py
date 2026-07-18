#!/usr/bin/env python3
"""
HARNESS DISPATCHER v1.0
Dispatches queries to RESEARCH, BUILDING, COMPLEX REASONING, BASE ARE, or HYBRID.
Now accepts Shared Cognitive State (SCS) for hybrid handoff continuity.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from cognitive_compiler.shared_cognitive_state import SharedCognitiveState
from cognitive_compiler.meta_router_v2 import MetaRoutingHarness, MetaRoutingResult
from cognitive_compiler.research_harness_v1 import ResearchHarness
from cognitive_compiler.building_harness_v1 import BuildingHarness
from cognitive_compiler.meta_coordinator_v3_2 import MetaIntelligenceCoordinator, QueryType, IntelligenceLayer


class HarnessDispatcher:
    """
    v1.0 dispatcher with SCS-aware hybrid execution.
    """

    def __init__(self, coordinator: Optional[MetaIntelligenceCoordinator] = None):
        self.meta = MetaRoutingHarness()
        self.research = ResearchHarness()
        self.building = BuildingHarness()
        self.coordinator = coordinator or MetaIntelligenceCoordinator(worker_count=2)

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
            "elapsed_s": meta.elapsed_s,
        }

        if primary == "base_are":
            result["primary_output"] = self._base_are(query, context)
            scs.add_harness_output("base_are", result["primary_output"])
            return result

        if primary == "research":
            result["primary_output"] = self.research.execute(query)
        elif primary == "building":
            result["primary_output"] = self.building.execute(query, constraints=context.get("constraints", []))
        else:
            result["primary_output"] = self._base_are(query, context)
        scs.add_harness_output(primary, result["primary_output"])

        if secondary:
            handoff_prompt = (
                "You are continuing a hybrid reasoning session.\n" + scs.to_prompt_context() +
                "\nIntegrate the prior reasoning and complete the secondary protocol."
            )
            if secondary == "research":
                result["secondary_output"] = self.research.execute(query + "\n\nContext: " + scs.problem_statement)
            elif secondary == "building":
                result["secondary_output"] = self.building.execute(query, constraints=context.get("constraints", []))
            elif secondary == "complex_reasoning":
                result["secondary_output"] = self._base_are(handoff_prompt, context)
            else:
                result["secondary_output"] = self._base_are(handoff_prompt, context)
            scs.add_harness_output(secondary, result["secondary_output"])

        return result

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
                timeout=context.get("timeout", 10.0)
            )
            return res.to_dict()
        except Exception as e:
            return {"error": str(e), "query": query}

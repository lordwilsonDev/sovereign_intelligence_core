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
from cognitive_compiler.sovereign_finetune_harness_v1 import SovereignFineTuningHarness
from cognitive_compiler.sovereign_autonomy_core import (
    CognitiveMirageAuditor,
    EpistemicIndependenceGauge,
    PhysicalSovereigntyAssertion,
    QuarantineInversionAgent,
    ReasoningToNoiseMeter,
    SACEnvelope,
    SovereignAutonomyCore,
    SovereignAutonomyScore,
)


class HarnessDispatcher:
    """
    v1.0 dispatcher with SCS-aware hybrid execution.
    """

    def __init__(self, coordinator: Optional[MetaIntelligenceCoordinator] = None) -> None:
        self.meta = MetaRoutingHarness()
        self.research = ResearchHarness()
        self.building = BuildingHarness()
        self.finetune = SovereignFineTuningHarness(repo_path="", privacy_boundary="local-only")
        self.coordinator = coordinator or MetaIntelligenceCoordinator(worker_count=2)
        self.verifier = CognitiveCompilerVerifier()
        self._sac = SovereignAutonomyCore()

    def dispatch(self, query: str, context: Dict[str, Any] = None, scs: Optional[SharedCognitiveState] = None) -> Dict[str, Any]:
        context = context or {}
        meta = self._execute_meta_routing(query, context)
        scs = self._prepare_scs(query, context, meta, scs)
        sac_block = self._run_sac_gate(query, context, scs)
        if sac_block is not None:
            return sac_block
        policy_block = self._enforce_dispatch_policy(query, context, scs)
        if policy_block is not None:
            return policy_block
        result = self._build_base_result(query, context, meta, scs)
        if scs.routing_decision.get("primary") == "base_are":
            result["primary_output"] = self._base_are(query, context)
            scs.add_harness_output("base_are", result["primary_output"])
            return self._post_process_result(result, meta, query, context)
        primary_result = self._execute_primary(query, context, result, scs)
        result.update(primary_result)
        if self._verification_blocked(result, context):
            return self._post_process_result(result, meta, query, context)
        secondary_result = self._execute_secondary_if_needed(query, context, result, scs)
        if secondary_result is not None:
            result.update(secondary_result)
        return self._post_process_result(result, meta, query, context)

    def _execute_meta_routing(self, query: str, context: Dict[str, Any]) -> MetaRoutingResult:
        return self.meta.execute(query, context)

    def _prepare_scs(self, query: str, context: Dict[str, Any], meta: MetaRoutingResult, scs: Optional[SharedCognitiveState]) -> SharedCognitiveState:
        scs = scs or SharedCognitiveState(problem_statement=query)
        scs.routing_decision = {
            "primary": meta.decision.primary,
            "secondary": meta.decision.secondary,
            "order": meta.decision.order,
            "confidence": meta.decision.confidence,
            "justification": meta.decision.justification,
        }
        scs.context = context
        return scs

    def _run_sac_gate(self, query: str, context: Dict[str, Any], scs: SharedCognitiveState) -> Optional[Dict[str, Any]]:
        core = SovereignAutonomyCore()
        envelope = core.run_dispatch_gate(query=query, context=context, model_source="local")
        scs.sac = SovereignAutonomyCore.to_dict(envelope)
        return None

    def _enforce_dispatch_policy(self, query: str, context: Dict[str, Any], scs: SharedCognitiveState) -> Optional[Dict[str, Any]]:
        try:
            from msb_v2.v3.policy import CognitivePolicyError, enforce_dispatch_policy
            actor = context.get("actor") or context.get("sub") or "anonymous"
            primary = scs.routing_decision.get("primary")
            secondary = scs.routing_decision.get("secondary")
            order = scs.routing_decision.get("order")
            enforce_dispatch_policy(str(primary), {"actor": actor, **context})
            if secondary and order == "serial":
                enforce_dispatch_policy(str(secondary), {"actor": actor, **context})
        except CognitivePolicyError as exc:
            primary = scs.routing_decision.get("primary")
            secondary = scs.routing_decision.get("secondary")
            order = scs.routing_decision.get("order")
            meta_elapsed = getattr(self.meta.execute(query, context), "elapsed_s", 0.0)
            return {
                "routing": {
                    "primary": primary,
                    "secondary": secondary,
                    "order": order,
                    "confidence": 0.0,
                    "justification": str(exc),
                    "rerouted": False,
                },
                "primary_output": {"verification": "blocked", "reason": str(exc)},
                "secondary_output": None,
                "telemetry": {
                    "primary": {"execution_time_s": 0.0, "retries": 0, "fallback_reason": str(exc), "error_class": "policy", "tags": [primary]},
                    "secondary": {"execution_time_s": 0.0, "retries": 0, "fallback_reason": None, "error_class": None, "tags": [secondary]},
                    "routing_confidence": 0.0,
                    "elapsed_s": meta_elapsed,
                },
                "elapsed_s": meta_elapsed,
            }
        except Exception:
            pass
        return None

    def _build_base_result(self, query: str, context: Dict[str, Any], meta: MetaRoutingResult, scs: SharedCognitiveState) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "routing": {
                "primary": meta.decision.primary,
                "secondary": meta.decision.secondary,
                "order": meta.decision.order,
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
                "primary": {"execution_time_s": 0.0, "retries": 0, "fallback_reason": None, "error_class": None, "tags": [meta.decision.primary]},
                "secondary": {"execution_time_s": 0.0, "retries": 0, "fallback_reason": None, "error_class": None, "tags": [meta.decision.secondary]},
                "routing_confidence": meta.decision.confidence,
                "elapsed_s": meta.elapsed_s,
            },
            "elapsed_s": meta.elapsed_s,
        }
        return result

    def _execute_primary(self, query: str, context: Dict[str, Any], result: Dict[str, Any], scs: SharedCognitiveState) -> Dict[str, Any]:
        primary = scs.routing_decision.get("primary")
        start = time.time()
        primary_payload = self._run_primary(primary, query, context)
        elapsed = round(time.time() - start, 4)
        result["telemetry"]["primary"]["execution_time_s"] = elapsed
        result["telemetry"]["primary"]["tags"] = self._tags_for(primary)
        result["elapsed_s"] = elapsed + result.get("elapsed_s", 0.0) - scs.routing_decision.get("elapsed", elapsed)
        result["primary_output"] = primary_payload
        scs.add_harness_output(primary, primary_payload)
        if isinstance(primary_payload, dict) and primary in {"building", "agentic-dev"} and "artifact" in primary_payload:
            result.setdefault("artifact_summary", {
                "normalizer_backend": primary_payload.get("artifact", {}).get("metrics", {}).get("normalizer_backend"),
                "artifact_id": primary_payload.get("artifact", {}).get("artifact_id"),
                "kind": primary_payload.get("artifact", {}).get("kind"),
            })
        return result

    def _verification_blocked(self, result: Dict[str, Any], context: Dict[str, Any]) -> bool:
        verification = self.verifier.verify(result, context)
        if verification is not None and not verification.ok:
            result["primary_output"] = {"verification": "blocked", "issues": verification.issues, "risk": verification.risk}
            result.setdefault("telemetry", {})["primary"]["error_class"] = "verification"
            result.setdefault("telemetry", {})["primary"]["fallback_reason"] = f"axiom_risk={verification.risk:.2f}"
            return True
        return False

    def _execute_secondary_if_needed(self, query: str, context: Dict[str, Any], result: Dict[str, Any], scs: SharedCognitiveState) -> Optional[Dict[str, Any]]:
        primary = scs.routing_decision.get("primary")
        secondary = scs.routing_decision.get("secondary")
        order = scs.routing_decision.get("order")
        if secondary and order == "serial":
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
        return None

    def _post_process_result(self, result: Dict[str, Any], meta: MetaRoutingResult, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        core = getattr(self, "_sac", None) or SovereignAutonomyCore()
        result.setdefault("sac", {}).update(
            SovereignAutonomyCore.to_dict(
                self._run_post_sac(result, query=result.get("query", query), context=result.get("context", context), core=core)
            )
        )
        if "memory_bytes" not in result["telemetry"]["primary"]:
            try:
                import sys as _sys
                result["telemetry"]["primary"]["memory_bytes"] = _sys.getsizeof(result)
            except Exception:
                pass
        return result

    def _post_process(self, result: Dict[str, Any], meta: MetaRoutingResult) -> Dict[str, Any]:
        core = getattr(self, "_sac", None) or SovereignAutonomyCore()
        result.setdefault("sac", {}).update(
            SovereignAutonomyCore.to_dict(
                self._run_post_sac(result, query=result.get("query", ""), context=result.get("context", {}), core=core)
            )
        )
        if "memory_bytes" not in result["telemetry"]["primary"]:
            try:
                import sys as _sys
                result["telemetry"]["primary"]["memory_bytes"] = _sys.getsizeof(result)
            except Exception:
                pass
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
            "agentic-dev": ["agentic", "software development", "feature", "bug fix", "system design", "code review", "inversion", "MoIE", "developer"],
            "base_are": ["base-are", "reasoning"],
        }
        return mapping.get(harness, [harness])

    def _select_primary_handler(self, primary: str):
        if primary == "research":
            return lambda q, c: self.research.execute(q)
        if primary == "building":
            return lambda q, c: self.building.execute(q, constraints=c.get("constraints", []))
        if primary == "desktop":
            from cognitive_compiler.desktop_harness_v1 import DesktopHarness
            return lambda q, c: DesktopHarness().execute(q, timeout_s=float(c.get("timeout_s", 600.0)))
        if primary == "career":
            from cognitive_compiler.career_harness_v1 import CareerHarness
            return lambda q, c: CareerHarness(project_root=c.get("career_project_root")).execute(
                q,
                context={
                    "career_company": c.get("career_company", "Unknown"),
                    "career_role": c.get("career_role", "Unknown"),
                    "career_jd": c.get("career_jd", q),
                    "career_score": c.get("career_score"),
                    "confidence": c.get("confidence", 0.0),
                },
            ).payload
        if primary == "telegram":
            from cognitive_compiler.telegram_artifact_harness_v1 import TelegramArtifactHarness
            return lambda q, c: TelegramArtifactHarness().execute(q, context=c).payload
        if primary == "agentic-dev":
            from cognitive_compiler.agentic_software_development_harness_v1 import AgenticSoftwareDevelopmentHarness
            return lambda q, c: AgenticSoftwareDevelopmentHarness().execute(q, context=c).payload
        if primary == "empirical-grounding":
            from cognitive_compiler.empirical_grounding_harness_v1 import EmpiricalGroundingHarness
            return lambda q, c: EmpiricalGroundingHarness().execute(q, context=c).payload
        if primary == "sovereign-finetune":
            return lambda q, c: self._run_primary_finetune(q, c)
        return None

    def _run_primary_finetune(self, query: str, context: Dict[str, Any]) -> Any:
        action = context.get("finetune_action", "scan")
        repo = context.get("repo_path", "/tmp")
        handler = getattr(self, "finetune", None)
        if handler is None:
            raise RuntimeError("Sovereign fine-tune harness is not initialized on dispatcher")
        setattr(handler, "repo_path", repo)
        if action == "scan":
            return handler.scan_documents()
        if action == "distill":
            pairs = handler.synthesize_pairs(max_pairs=int(context.get("max_pairs", 64)))
            validation = handler.validate_pairs()
            return {"action": "distill", "pairs": len(pairs), "validation": validation, "privacy_boundary": handler.privacy_boundary}
        if action == "train":
            handler.repo_path = repo
            handler.scan_documents()
            handler.synthesize_pairs()
            job = handler.create_training_job(base_model=context.get("base_model", "local-base"))
            baseline = handler.validate_baseline_coherence()
            report = handler.run_post_training_validation(job_id=job.job_id)
            return {
                "action": "train",
                "job_id": job.job_id,
                "status": job.status,
                "dataset_size": job.dataset_size,
                "baseline_coherence": baseline,
                "integration_report": {
                    "model_name": report.model_name,
                    "validation_passed": report.validation_passed,
                    "coherence_score": report.coherence_score,
                    "confidence_score": report.confidence_score,
                    "recommendation": report.recommendation,
                    "falsification_condition": report.falsification_condition,
                },
            }
        return handler.scan_documents()

    def _run_primary(self, primary: Optional[str], query: str, context: Dict[str, Any]) -> Any:
        handler = self._select_primary_handler(primary)
        if handler is not None:
            return handler(query, context)
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
        if secondary == "agentic-dev":
            from cognitive_compiler.agentic_software_development_harness_v1 import AgenticSoftwareDevelopmentHarness
            return AgenticSoftwareDevelopmentHarness().execute(query, context=context).payload
        if secondary == "empirical-grounding":
            from cognitive_compiler.empirical_grounding_harness_v1 import EmpiricalGroundingHarness
            return EmpiricalGroundingHarness().execute(query, context=context).payload
        return self._base_are(handoff_prompt, context)

    def _run_post_sac(self, harness_output: Dict[str, Any], *, query: str, context: Dict[str, Any], core: Optional[SovereignAutonomyCore] = None) -> SACEnvelope:
        return (core or getattr(self, "_sac", SovereignAutonomyCore())).run_dispatch_gate(
            query=query,
            context=context,
            harness_output=harness_output,
            model_source="local",
            change_id=context.get("change_id"),
        )

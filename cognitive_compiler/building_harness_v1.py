#!/usr/bin/env python3
"""
BUILDING HARNESS v1.0 – Axiomatic Reasoning Engine (ARE)
Activates on building tasks: design/architect/plan/create.
Overlays onto ARE reasoning cycle with domain-specific steps.
"""

from __future__ import annotations

import math
import random
import time
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field

# Reuse ARE engines
from cognitive_compiler.cognitive_compiler_Aie import AxiomEvaluator
from cognitive_compiler.meta_coordinator_v3_2 import (
    AxiomInversionEngine,
    IntelligenceLayer,
    QueryType,
)
from cognitive_compiler.codebrain_artifact import ArtifactNormalizer, CodeBrainArtifact


# ===========================================================================
# DATA STRUCTURES
# ===========================================================================

@dataclass
class Requirement:
    id: str
    text: str
    explicit: bool
    category: str  # functional | non-functional | constraint | resource | timeline
    assumptions: List[str] = field(default_factory=list)
    assumption_confidence: List[float] = field(default_factory=list)

@dataclass
class DesignConcept:
    name: str
    description: str
    source: str  # standard | inverted | anomalous | hybrid
    feasibility: float  # 0..1
    upside: float  # 0..1
    assumptions_attacked: List[str] = field(default_factory=list)

@dataclass
class Architecture:
    components: List[str]
    flows: List[str]
    interfaces: List[str]
    traceability: Dict[str, List[str]]  # assumption -> component ids
    primitives: List[str] = field(default_factory=list)
    phase_transition_risk: str = ""

@dataclass
class PrototypePlan:
    name: str
    target_assumptions: List[str]
    build_description: str
    success_criteria: List[str]
    metrics: List[str]
    forecast_hold: str
    forecast_fail: str
    pivot_persevere_kill: str = "persevere"

@dataclass
class Risk:
    id: str
    category: str  # logical | scaling | coordination | cost | tech_obsolescence
    description: str
    mitigation: str
    severity: str  # LOW | MEDIUM | HIGH | CRITICAL

@dataclass
class BuildPlan:
    final_design: str
    assumptions_to_tests: Dict[str, List[str]]
    timeline_phases: List[str]
    decision_gates: List[str]
    resources: List[str]
    risks: List[Risk]
    falsification_conditions: List[str]
    overall_confidence: float
    top_assumptions: List[str]
    immediate_next_action: str


# ===========================================================================
# MOIE PANEL (Lightweight)
# ===========================================================================

class MoIEBuilderPanel:
    """Critic, Scout, Synthesizer for building tasks."""

    def __init__(self):
        self.critiques: List[str] = []
        self.scout_findings: List[str] = []
        self.synthesis: List[str] = []

    def critic(self, design: str, assumptions: List[str]) -> List[str]:
        critiques = []
        if not assumptions:
            critiques.append("Design has no explicit assumptions to attack.")
        if any(a.lower() in ["always", "must", "only one"] for a in assumptions):
            critiques.append("Absolute assumptions detected; prime inversion targets.")
        if "user" in design.lower() and "needs" in design.lower():
            critiques.append("User need statement present; consider anti-solution inversion.")
        self.critiques.extend(critiques)
        return critiques

    def scout(self, task_type: str) -> Dict[str, List[str]]:
        findings = {
            "standard": [],
            "anomalous": [],
            "failures": []
        }
        if "api" in task_type.lower() or "service" in task_type.lower():
            findings["standard"] = ["REST/HTTP", "gRPC", "event-driven", "GraphQL"]
            findings["anomalous"] = ["CRDT-based coordination", "Bittorrent-style swarms"]
            findings["failures"] = ["Chatty microservices in low-bandwidth environments"]
        elif "storage" in task_type.lower() or "state" in task_type.lower():
            findings["standard"] = ["Relational DB", "Document store", "KV cache"]
            findings["anomalous"] = ["Git-as-database", "BitTorrent DHT", "CRDT log"]
            findings["failures"] = ["Over-sharding without locality", "Schema drift"]
        else:
            findings["standard"] = ["Monolithic v1", "Microservice v2", "Serverless hybrid"]
            findings["anomalous"] = ["Erlang-style supervision trees", "Smalltalk image model"]
            findings["failures"] = ["Premature distribution", "Distributed monolith"]
        self.scout_findings.extend(findings["standard"] + findings["anomalous"] + findings["failures"])
        return findings

    def synthesizer(self, concepts: List[DesignConcept], constraints: List[str]) -> List[str]:
        synth = []
        if not concepts:
            synth.append("No concepts to synthesize.")
            return synth
        # Prefer hybrid combinations of standard + inverted
        standard = [c for c in concepts if c.source == "standard"]
        inverted = [c for c in concepts if c.source == "inverted"]
        if standard and inverted:
            synth.append(f"Fuse {standard[0].name} with inverted concept {inverted[0].name}.")
        if constraints:
            synth.append(f"Enforce constraints as first-class design boundaries: {', '.join(constraints[:3])}.")
        self.synthesis.extend(synth)
        return synth


# ===========================================================================
# BUILDING HARNESS
# ===========================================================================

class BuildingHarness:
    """
    v1.0 building protocol overlay.
    """

    def __init__(self, ail: Optional[AxiomInversionEngine] = None):
        self.ail = ail or AxiomInversionEngine()
        self.panel = MoIEBuilderPanel()
        self.aie = AxiomEvaluator()
        self.normalizer = ArtifactNormalizer()

    # ------------------------------------------------------------------
    # Step 1 – Requirement Extraction & Assumption Mapping
    # ------------------------------------------------------------------
    def requirement_extraction(self, goal: str, constraints: Optional[List[str]] = None) -> Tuple[List[Requirement], List[str]]:
        constraints = constraints if constraints is not None else []
        # Parse simple requirements from goal text. In production, use LLM.
        reqs: List[Requirement] = []
        sentences = [s.strip() for s in goal.replace(".", "\n").split("\n") if s.strip()]
        for idx, sentence in enumerate(sentences, 1):
            cat = "functional"
            if any(w in sentence.lower() for w in ["fast", "latency", "throughput", "scale", "perf"]):
                cat = "non-functional"
            if any(w in sentence.lower() for w in ["within", "by", "deadline", "<=>", "<=>"]):
                cat = "constraint" if "must" in sentence.lower() else "timeline"
            if any(w in sentence.lower() for w in ["budget", "team", "headcount", "resources"]):
                cat = "resource"
            assumptions = [
                f"Belief: '{sentence}' maps to real user need.",
                f"Belief: current tech can satisfy '{sentence}' within constraints.",
            ]
            confs = [0.7, 0.6]
            reqs.append(Requirement(
                id=f"REQ-{idx:03d}",
                text=sentence,
                explicit=True,
                category=cat,
                assumptions=assumptions,
                assumption_confidence=confs
            ))

        all_assumptions = [a for r in reqs for a in r.assumptions]
        return reqs, all_assumptions

    # ------------------------------------------------------------------
    # Step 2 – Design Space Exploration (Scout-led)
    # ------------------------------------------------------------------
    def design_space_exploration(self, task_type: str) -> Dict[str, List[str]]:
        return self.panel.scout(task_type)

    # ------------------------------------------------------------------
    # Step 3 – Axiom Inversion & Radical Alternatives (Critic-led)
    # ------------------------------------------------------------------
    def axiom_inversion(self, requirement_text: str, constraint_list: Optional[List[str]] = None) -> List[DesignConcept]:
        constraint_list = constraint_list if constraint_list is not None else []
        # Extract simple assumption stubs
        assumptions = []
        for sentence in requirement_text.split("."):
            s = sentence.strip()
            if not s:
                continue
            if "must" in s.lower() or "need" in s.lower() or "should" in s.lower():
                assumptions.append(s)

        concepts: List[DesignConcept] = []
        inverted_hypotheses = self.ail.invert(requirement_text, requirement_text)
        for hyp in inverted_hypotheses:
            concepts.append(DesignConcept(
                name=hyp["mechanism"],
                description=hyp["inverted_assumption"],
                source="inverted",
                feasibility=max(0.1, min(0.9, hyp["confidence"])),
                upside=0.3 + hyp["confidence"] * 0.5,
                assumptions_attacked=[hyp["original_assumption"]]
            ))

        # Always add one standard suggestion
        concepts.append(DesignConcept(
            name="Standard Approach",
            description="Proven pattern matching the explicit requirements with minimal deviation.",
            source="standard",
            feasibility=0.9,
            upside=0.4,
            assumptions_attacked=[]
        ))

        return concepts

    # ------------------------------------------------------------------
    # Step 4 – Architecture Synthesis (Synthesizer-led)
    # ------------------------------------------------------------------
    def architecture_synthesis(self, concepts: List[DesignConcept], requirements: List[Requirement], assumptions: List[str]) -> Architecture:
        components = ["Ingress", "Core", "State", "Egress"]
        flows = ["Request → Core → State → Response", "Event → Core → State"]
        interfaces = ["REST: /v1/*", "Event: topic.system.*"]
        trace = {}
        comp_ids = [f"C{i+1}" for i in range(len(components))]
        for idx, a in enumerate(assumptions[:len(comp_ids)]):
            trace[a] = [comp_ids[idx]]
        primitives = ["Actor per component", "CBF guard on State"]
        return Architecture(
            components=components,
            flows=flows,
            interfaces=interfaces,
            traceability=trace,
            primitives=primitives,
            phase_transition_risk="Shared State may serialize under >10k RPS; shard State before that threshold."
        )

    # ------------------------------------------------------------------
    # Step 5 – Prototyping & Test Strategy
    # ------------------------------------------------------------------
    def prototype_plan(self, requirements: List[Requirement], assumptions: List[str]) -> PrototypePlan:
        target = assumptions[:3] if len(assumptions) >= 3 else assumptions
        return PrototypePlan(
            name="Spike-v1",
            target_assumptions=target,
            build_description="Build one-path mock implementation against a fixed dataset.",
            success_criteria=["latency p99 < 200ms", "error rate < 0.1%"],
            metrics=["p50_latency_ms", "p99_latency_ms", "error_rate", "throughput_rps"],
            forecast_hold="Assumption holds: metrics improve monotonically with optimization.",
            forecast_fail="Assumption fails: latency variance spikes as data skew increases.",
            pivot_persevere_kill="persevere"
        )

    # ------------------------------------------------------------------
    # Step 6 – Logic Loop & Error Correction
    # ------------------------------------------------------------------
    def logic_loop(self, architecture: Architecture, requirements: List[Requirement]) -> Tuple[Architecture, List[Risk]]:
        risks = [
            Risk("R1", "logical", "Circular dependency between Core and State", "Introduce explicit command/query separation", "HIGH"),
            Risk("R2", "scaling", "Single State becomes bottleneck", "Partition State by key prefix when QPS > 10k", "MEDIUM"),
            Risk("R3", "coordination", "Actor failure cascade", "Add supervisor with restart/backoff policy", "HIGH"),
        ]
        # If the architecture is brittle, we return it unchanged for minor fixes,
        # but the caller may re-enter Step 3 if failures are severe.
        return architecture, risks

    # ------------------------------------------------------------------
    # Step 7 – Synthesis & Build Plan
    # ------------------------------------------------------------------
    def build_plan(self, final_design: str, architecture: Architecture, prototype: PrototypePlan, risks: List[Risk]) -> BuildPlan:
        return BuildPlan(
            final_design=final_design,
            assumptions_to_tests={a: [prototype.name] for a in prototype.target_assumptions},
            timeline_phases=["Spike", "Hardening", "Integration", "Observability"],
            decision_gates=["Gate 1: Spike metrics within SLA", "Gate 2: <5% error in load test", "Gate 3: On-call runbook"],
            resources=["1 backend engineer", "1 SRE for 2 weeks"],
            risks=risks,
            falsification_conditions=["p99 latency > 500ms under 2x expected load", "memory growth > 1GB/24h without leak"],
            overall_confidence=0.72,
            top_assumptions=prototype.target_assumptions[:3],
            immediate_next_action="Implement Spike-v1 against synthetic dataset and run the success criteria benchmark."
        )

    # ------------------------------------------------------------------
    # Main Execution
    # ------------------------------------------------------------------
    def execute(self, goal: str, constraints: List[str] = None) -> Dict[str, Any]:
        constraints = constraints or []
        start = time.time()

        # Step 1
        requirements, assumptions = self.requirement_extraction(goal, constraints)
        self.panel.critic(goal, assumptions)

        # Step 2
        task_type = goal
        scout_map = self.design_space_exploration(task_type)

        # Step 3
        concepts: List[DesignConcept] = []
        for req in requirements:
            concepts.extend(self.axiom_inversion(req.text, constraints))
        concepts = sorted(concepts, key=lambda c: (-c.feasibility, -c.upside))
        # Deduplicate names
        seen = set()
        unique_concepts = []
        for c in concepts:
            if c.name not in seen:
                seen.add(c.name)
                unique_concepts.append(c)
        concepts = unique_concepts[:10]

        # Step 4
        architecture = self.architecture_synthesis(concepts, requirements, assumptions)
        synth_output = self.panel.synthesizer(concepts, constraints)

        # Step 5
        prototype = self.prototype_plan(requirements, assumptions)

        # Step 6
        architecture, risks = self.logic_loop(architecture, requirements)

        # Step 7
        plan = self.build_plan(goal + " synthesized design.", architecture, prototype, risks)

        return {
            "goal": goal,
            "requirements": [{"id": r.id, "text": r.text, "category": r.category, "assumptions": r.assumptions} for r in requirements],
            "assumptions": assumptions,
            "scout_map": scout_map,
            "concepts": [{"name": c.name, "source": c.source, "feasibility": c.feasibility, "upside": c.upside} for c in concepts],
            "architecture": {
                "components": architecture.components,
                "flows": architecture.flows,
                "interfaces": architecture.interfaces,
                "traceability_count": len(architecture.traceability),
                "primitives": architecture.primitives,
                "phase_transition_risk": architecture.phase_transition_risk
            },
            "prototype": {
                "name": prototype.name,
                "targets": prototype.target_assumptions,
                "build": prototype.build_description,
                "success": prototype.success_criteria,
                "metrics": prototype.metrics
            },
            "risks": [{"id": r.id, "category": r.category, "severity": r.severity, "description": r.description, "mitigation": r.mitigation} for r in risks],
            "plan": {
                "confidence": plan.overall_confidence,
                "phases": plan.timeline_phases,
                "gates": plan.decision_gates,
                "resources": plan.resources,
                "falsifications": plan.falsification_conditions,
                "next_action": plan.immediate_next_action
            },
            "elapsed_s": round(time.time() - start, 4),
            "artifact": self.normalizer.normalize({"goal": goal, "requirements": requirements, "assumptions": assumptions}, kind="build").to_dict(),
        }

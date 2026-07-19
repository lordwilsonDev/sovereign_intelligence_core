from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from cognitive_compiler.harness_abc import BaseHarness, HarnessResult, HarnessTelemetry
from cognitive_compiler.codebrain_artifact import ArtifactNormalizer


@dataclass
class DevRequirement:
    id: str
    text: str
    category: str
    assumptions: List[str] = field(default_factory=list)
    assumption_confidence: List[float] = field(default_factory=list)


@dataclass
class DevDesignConcept:
    name: str
    description: str
    source: str
    feasibility: float
    upside: float
    assumptions_attacked: List[str] = field(default_factory=list)


@dataclass
class DevArchitecture:
    components: List[str]
    flows: List[str]
    interfaces: List[str]
    traceability_count: int
    primitives: List[str] = field(default_factory=list)
    phase_transition_risk: str = ""


@dataclass
class PrototypePlan:
    name: str
    targets: List[str]
    build_description: str
    success_criteria: List[str]
    metrics: List[str]


@dataclass
class BuildRisk:
    id: str
    category: str
    severity: str
    description: str
    mitigation: str


@dataclass
class BuildPlan:
    confidence: float
    phases: List[str]
    gates: List[str]
    resources: List[str]
    falsifications: List[str]
    next_action: str


class AgenticSoftwareDevelopmentHarness(BaseHarness):
    """
    Agentic Software Development Harness v1.0
    Overlays axiom inversion, MoIE dialectic, and recursive review onto building tasks.
    """

    def __init__(self, ail: Optional[Any] = None) -> None:
        self.ail = ail
        self.critiques: List[str] = []
        self.scout_findings: List[str] = []
        self.synthesis: List[str] = []

    def initialize(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"ok": True, "event": "initialized"}

    def evaluate(self, query: str, context: Dict[str, Any]) -> HarnessResult:
        start = time.time()
        goal = context.get("dev_goal") or query
        constraints = context.get("dev_constraints", [])
        requirements, assumptions = self._requirement_extraction(goal, constraints)
        self._critic(goal, assumptions)
        scout_map = self._design_space_exploration(goal)
        concepts = self._axiom_inversion(goal)
        concepts = self._dedup(concepts)[:10]
        architecture = self._architecture_synthesis(concepts, requirements, assumptions)
        self._synthesizer(concepts, constraints)
        prototype = self._prototype_plan(requirements, assumptions)
        architecture, risks = self._logic_loop(architecture, requirements)
        plan = self._build_plan(goal, architecture, prototype, risks)
        elapsed = round(time.time() - start, 4)
        payload = {
            "goal": goal,
            "requirements": [{"id": r.id, "text": r.text, "category": r.category, "assumptions": r.assumptions} for r in requirements],
            "assumptions": assumptions,
            "scout_map": scout_map,
            "concepts": [{"name": c.name, "source": c.source, "feasibility": c.feasibility, "upside": c.upside} for c in concepts],
            "architecture": {
                "components": architecture.components,
                "flows": architecture.flows,
                "interfaces": architecture.interfaces,
                "traceability_count": architecture.traceability_count,
                "primitives": architecture.primitives,
                "phase_transition_risk": architecture.phase_transition_risk,
            },
            "prototype": {
                "name": prototype.name,
                "targets": prototype.targets,
                "build": prototype.build_description,
                "success": prototype.success_criteria,
                "metrics": prototype.metrics,
            },
            "risks": [{"id": r.id, "category": r.category, "severity": r.severity, "description": r.description, "mitigation": r.mitigation} for r in risks],
            "plan": {
                "confidence": plan.confidence,
                "phases": plan.phases,
                "gates": plan.gates,
                "resources": plan.resources,
                "falsifications": plan.falsifications,
                "next_action": plan.next_action,
            },
            "elapsed_s": elapsed,
        }
        telemetry = HarnessTelemetry(routing_confidence=0.85, execution_time_s=elapsed, tags=["agentic", "building"])
        payload["artifact"] = ArtifactNormalizer().normalize({
            "goal": goal,
            "requirements": [r.text for r in requirements],
            "assumptions": assumptions,
        }, kind="agentic-dev").to_dict()
        return HarnessResult(ok=True, event="evaluated", payload=payload, telemetry=telemetry)

    def execute(self, query: str, *args: Any, context: Optional[Dict[str, Any]] = None, **kwargs: Any) -> HarnessResult:
        if context is None:
            context = {}
        return self.evaluate(query, context)

    def observe(self, result: HarnessResult) -> Dict[str, Any]:
        return {"event": result.event, "risks": len(result.payload.get("risks", []))}

    def repair(self, result: HarnessResult) -> Optional[HarnessResult]:
        if result.ok:
            return None
        return HarnessResult(ok=False, event="repair:manual", error="review required", telemetry=HarnessTelemetry(tags=["agentic", "repair"]))

    def shutdown(self) -> Dict[str, Any]:
        return {"ok": True, "event": "shutdown"}

    def _requirement_extraction(self, goal: str, constraints: List[str]) -> tuple[list[DevRequirement], list[str]]:
        reqs: list[DevRequirement] = []
        assumptions: list[str] = []
        sentences = [s.strip() for s in goal.replace(".", "\n").split("\n") if s.strip()]
        for idx, sentence in enumerate(sentences, 1):
            category = "functional"
            low = sentence.lower()
            if any(w in low for w in ["fast", "latency", "throughput", "scale", "perf"]):
                category = "non-functional"
            if any(w in low for w in ["within", "by", "deadline", "must"]) and category != "non-functional":
                category = "constraint" if "must" in low else "timeline"
            if any(w in low for w in ["budget", "team", "headcount", "resources"]):
                category = "resource"
            assumption_list = [
                f"Belief: '{sentence}' maps to real user need.",
                f"Belief: current tech can satisfy '{sentence}' within constraints.",
            ]
            confidence_list = [0.7, 0.6]
            reqs.append(DevRequirement(id=f"REQ-{idx:03d}", text=sentence, category=category, assumptions=assumption_list, assumption_confidence=confidence_list))
            assumptions.extend(assumption_list)
        return reqs, assumptions

    def _critic(self, goal: str, assumptions: List[str]) -> List[str]:
        critiques = []
        if not assumptions:
            critiques.append("No explicit assumptions to attack.")
        if any(a.lower() in ["always", "must", "only one"] for a in assumptions):
            critiques.append("Absolute assumptions detected; prime inversion targets.")
        if "user" in goal.lower() and "needs" in goal.lower():
            critiques.append("User need statement present; consider anti-solution inversion.")
        self.critiques.extend(critiques)
        return critiques

    def _design_space_exploration(self, task_type: str) -> Dict[str, List[str]]:
        low = task_type.lower()
        if "api" in low or "service" in low:
            return {
                "standard": ["REST/HTTP", "gRPC", "event-driven", "GraphQL"],
                "anomalous": ["CRDT-based coordination", "BitTorrent-style swarms"],
                "failures": ["Chatty microservices in low-bandwidth environments"],
            }
        if "storage" in low or "state" in low:
            return {
                "standard": ["Relational DB", "Document store", "KV cache"],
                "anomalous": ["Git-as-database", "BitTorrent DHT", "CRDT log"],
                "failures": ["Over-sharding without locality", "Schema drift"],
            }
        return {
            "standard": ["Monolithic v1", "Microservice v2", "Serverless hybrid"],
            "anomalous": ["Erlang-style supervision trees", "Smalltalk image model"],
            "failures": ["Premature distribution", "Distributed monolith"],
        }

    def _axiom_inversion(self, requirement_text: str) -> List[DevDesignConcept]:
        concepts: List[DevDesignConcept] = []
        if self.ail and hasattr(self.ail, "invert"):
            try:
                inverted_hypotheses = self.ail.invert(requirement_text, requirement_text)
                for hyp in inverted_hypotheses:
                    concepts.append(DevDesignConcept(
                        name=hyp.get("mechanism", "Inverted"),
                        description=hyp.get("inverted_assumption", ""),
                        source="inverted",
                        feasibility=max(0.1, min(0.9, float(hyp.get("confidence", 0.5)))),
                        upside=0.3 + float(hyp.get("confidence", 0.5)) * 0.5,
                        assumptions_attacked=[hyp.get("original_assumption", "")],
                    ))
            except Exception:
                pass
        concepts.append(DevDesignConcept(
            name="Standard Approach",
            description="Proven pattern matching explicit requirements with minimal deviation.",
            source="standard",
            feasibility=0.9,
            upside=0.4,
            assumptions_attacked=[],
        ))
        return concepts

    def _architecture_synthesis(self, concepts: List[DevDesignConcept], requirements: List[DevRequirement], assumptions: List[str]) -> DevArchitecture:
        components = ["Ingress", "Core", "State", "Egress"]
        flows = ["Request -> Core -> State -> Response", "Event -> Core -> State"]
        interfaces = ["REST: /v1/*", "Event: topic.system.*"]
        traceability_count = min(len(assumptions), len(components))
        primitives = ["Actor per component", "CBF guard on State"]
        phase_risk = "Shared State may serialize under >10k RPS; shard State before that threshold."
        return DevArchitecture(components=components, flows=flows, interfaces=interfaces, traceability_count=traceability_count, primitives=primitives, phase_transition_risk=phase_risk)

    def _prototype_plan(self, requirements: List[DevRequirement], assumptions: List[str]) -> PrototypePlan:
        targets = assumptions[:3] if len(assumptions) >= 3 else assumptions
        return PrototypePlan(
            name="Spike-v1",
            targets=targets,
            build_description="Build one-path mock implementation against a fixed dataset.",
            success_criteria=["latency p99 < 200ms", "error rate < 0.1%"],
            metrics=["p50_latency_ms", "p99_latency_ms", "error_rate", "throughput_rps"],
        )

    def _logic_loop(self, architecture: DevArchitecture, requirements: List[DevRequirement]) -> tuple[DevArchitecture, List[BuildRisk]]:
        risks = [
            BuildRisk("R1", "logical", "HIGH", "Circular dependency between Core and State", "Introduce explicit command/query separation"),
            BuildRisk("R2", "scaling", "MEDIUM", "Single State becomes bottleneck", "Partition State by key prefix when QPS > 10k"),
            BuildRisk("R3", "coordination", "HIGH", "Actor failure cascade", "Add supervisor with restart/backoff policy"),
        ]
        return architecture, risks

    def _build_plan(self, goal: str, architecture: DevArchitecture, prototype: PrototypePlan, risks: List[BuildRisk]) -> BuildPlan:
        assumptions_to_tests = {a: [prototype.name] for a in prototype.targets}
        return BuildPlan(
            confidence=0.72,
            phases=["Spike", "Hardening", "Integration", "Observability"],
            gates=["Gate 1: Spike metrics within SLA", "Gate 2: <5% error in load test", "Gate 3: On-call runbook"],
            resources=["1 backend engineer", "1 SRE for 2 weeks"],
            falsifications=["p99 latency > 500ms under 2x expected load", "memory growth > 1GB/24h without leak"],
            next_action="Implement Spike-v1 against synthetic dataset and run success-criteria benchmark.",
        )

    def _synthesizer(self, concepts: List[DevDesignConcept], constraints: List[str]) -> List[str]:
        synth = []
        if not concepts:
            synth.append("No concepts to synthesize.")
            return synth
        standard = [c for c in concepts if c.source == "standard"]
        inverted = [c for c in concepts if c.source == "inverted"]
        if standard and inverted:
            synth.append(f"Fuse {standard[0].name} with inverted concept {inverted[0].name}.")
        if constraints:
            synth.append(f"Enforce constraints as first-class design boundaries: {', '.join(constraints[:3])}.")
        self.synthesis.extend(synth)
        return synth

    @staticmethod
    def _dedup(concepts: List[DevDesignConcept]) -> List[DevDesignConcept]:
        seen = set()
        out = []
        for c in concepts:
            if c.name not in seen:
                seen.add(c.name)
                out.append(c)
        return out

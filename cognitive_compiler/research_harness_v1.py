#!/usr/bin/env python3
"""
RESEARCH HARNESS v1.0 – Axiomatic Reasoning Engine (ARE)
Activates on research tasks: investigate, analyze literature, build theory, design experiments.
"""

from __future__ import annotations

import math
import random
import time
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field

from cognitive_compiler.meta_coordinator_v3_2 import AxiomInversionEngine


# ===========================================================================
# DATA STRUCTURES
# ===========================================================================

@dataclass
class Assumption:
    id: str
    text: str
    validity_probability: float  # 0..1

@dataclass
class EvidenceItem:
    id: str
    description: str
    category: str  # supporting | anomaly | gap
    weight: float   # 0..1
    quality: float  # 0..1
    replication: str = "unknown"

@dataclass
class AlternativeHypothesis:
    id: str
    text: str
    prior_probability: float
    enabling_conditions: List[str]
    missing_variables: List[str]
    contradictions: List[str]
    source: str = "inverted"

@dataclass
class CausalNode:
    id: str
    label: str
    type: str  # cause | effect | mediator | confound

@dataclass
class CausalLink:
    source: str
    target: str
    relation: str  # causes | inhibits | modulates
    feedback: bool = False

@dataclass
class Prediction:
    hypothesis_id: str
    outcome: str
    probability: float
    effect_size: str
    direction: str  # positive | negative | neutral

@dataclass
class Experiment:
    id: str
    hypothesis_id: str
    independent_vars: List[str]
    dependent_vars: List[str]
    controls: List[str]
    confounds: List[str]
    sample_size: int
    statistical_test: str
    expected_outcomes: Dict[str, float]

@dataclass
class ResearchRisk:
    id: str
    category: str
    description: str
    mitigation: str
    severity: str

@dataclass
class ResearchOutput:
    question: str
    assumptions: List[Assumption]
    evidence: List[EvidenceItem]
    hypotheses: List[AlternativeHypothesis]
    causal_diagram: Dict[str, Any]
    predictions: List[Prediction]
    experiments: List[Experiment]
    risks: List[ResearchRisk]
    overall_confidence: float
    falsification_conditions: List[str]
    next_actions: List[str]
    elapsed_s: float = 0.0


# ===========================================================================
# MOIE PANEL (Lightweight)
# ===========================================================================

class MoIEResearchPanel:
    """Critic, Scout, Synthesizer for research tasks."""

    def __init__(self):
        self.critiques: List[str] = []
        self.scout_findings: List[str] = []
        self.synthesis: List[str] = []

    def critic(self, assumptions: List[Assumption], hypotheses: List[AlternativeHypothesis]) -> List[str]:
        critiques = []
        if not assumptions:
            critiques.append("No explicit assumptions extracted.")
        for a in assumptions:
            if a.validity_probability > 0.95:
                critiques.append(f"Assumption '{a.id}' stated with high confidence; ensure it is truly justified.")
        if hypotheses:
            contradictions = [c for h in hypotheses for c in h.contradictions]
            if contradictions:
                critiques.append(f"Found {len(contradictions)} possible contradictions; elevate to puzzles.")
        self.critiques.extend(critiques)
        return critiques

    def scout(self, topic: str) -> Dict[str, List[EvidenceItem]]:
        # Simulated knowledge mapping
        supporting = [
            EvidenceItem("S1", f"Foundational work supports '{topic}' directly", "supporting", 0.8, 0.7, "high"),
            EvidenceItem("S2", f"Corroborating meta-analysis (2022) strengthens dominant model", "supporting", 0.7, 0.6, "medium"),
        ]
        anomalies = [
            EvidenceItem("A1", f"Edge-case study contradicts core assumption (n=42, p<0.05)", "anomaly", 0.5, 0.8, "medium"),
            EvidenceItem("A2", f"Replication failure in adjacent field suggests boundary conditions", "anomaly", 0.4, 0.9, "low"),
        ]
        gaps = [
            EvidenceItem("G1", "No studies manipulate the key mediator directly", "gap", 0.6, 0.5, "unknown"),
            EvidenceItem("G2", "Longitudinal data completely absent", "gap", 0.7, 0.4, "unknown"),
        ]
        findings = {"supporting": supporting, "anomalies": anomalies, "gaps": gaps}
        self.scout_findings.extend([e.id for e in supporting + anomalies + gaps])
        return findings

    def synthesizer(self, hypotheses: List[AlternativeHypothesis], evidence: Dict[str, List[EvidenceItem]]) -> List[str]:
        synth = []
        if not hypotheses:
            synth.append("No hypotheses to synthesize.")
            return synth
        primary = hypotheses[0]
        synth.append(f"Integrate primary hypothesis: {primary.text}")
        anomalies = evidence.get("anomalies", [])
        if anomalies:
            synth.append(f"Reframe {len(anomalies)} anomalies as boundary conditions for the unified theory.")
        self.synthesis.extend(synth)
        return synth


# ===========================================================================
# RESEARCH HARNESS
# ===========================================================================

class ResearchHarness:
    """
    v1.0 research protocol overlay.
    """

    def __init__(self, ail: Optional[AxiomInversionEngine] = None):
        self.ail = ail or AxiomInversionEngine()
        self.panel = MoIEResearchPanel()

    # ------------------------------------------------------------------
    # Step 1 – Problem Scoping & Assumption Extraction
    # ------------------------------------------------------------------
    def problem_scoping(self, question: str) -> Tuple[str, List[Assumption]]:
        assumptions = [
            Assumption("A1", "Dominant paradigm is applicable to this exact context", 0.7),
            Assumption("A2", "Current measurement instruments capture the key construct", 0.6),
            Assumption("A3", "The system is stationary or evolves slowly enough for study", 0.5),
        ]
        return question, assumptions

    # ------------------------------------------------------------------
    # Step 2 – Literature & Knowledge Mapping (Scout-Led)
    # ------------------------------------------------------------------
    def knowledge_mapping(self, topic: str) -> Dict[str, List[EvidenceItem]]:
        return self.panel.scout(topic)

    # ------------------------------------------------------------------
    # Step 3 – Axiom Inversion & Alternative Hypotheses (Critic-Led)
    # ------------------------------------------------------------------
    def axiom_inversion(self, assumptions: List[Assumption], topic: str) -> List[AlternativeHypothesis]:
        hypotheses: List[AlternativeHypothesis] = []
        for assumption in assumptions:
            inverted_texts = self.ail.invert(assumption.text, topic)
            for inv in inverted_texts[:2]:
                hypotheses.append(AlternativeHypothesis(
                    id=f"H-{len(hypotheses)+1:03d}",
                    text=f"Inverted: {inv['inverted_assumption']} via {inv['mechanism']}",
                    prior_probability=round(max(0.1, min(0.9, inv["confidence"])), 2),
                    enabling_conditions=[f"Condition enabling: {inv['mechanism']}"],
                    missing_variables=["Temporal dynamics", "Boundary conditions"],
                    contradictions=[c for c in inv.get("counterexamples", [])[:1]],
                ))
        if not hypotheses:
            hypotheses.append(AlternativeHypothesis(
                id="H-001", text="Null: No measurable effect under current conditions.",
                prior_probability=0.4, enabling_conditions=["Stable baseline"],
                missing_variables=[], contradictions=[]
            ))
        return hypotheses

    # ------------------------------------------------------------------
    # Step 4 – Mechanism Synthesis & Theory Building (Synthesizer-Led)
    # ------------------------------------------------------------------
    def mechanism_synthesis(self, hypotheses: List[AlternativeHypothesis], evidence: Dict[str, List[EvidenceItem]]) -> Tuple[Dict[str, Any], List[Prediction]]:
        nodes = [
            CausalNode("N1", "Context / Inputs", "cause"),
            CausalNode("N2", "Key Construct", "mediator"),
            CausalNode("N3", "Observed Outcome", "effect"),
        ]
        links = [
            CausalLink("N1", "N2", "causes"),
            CausalLink("N2", "N3", "causes", feedback=True),
        ]
        causal_diagram = {
            "nodes": [{"id": n.id, "label": n.label, "type": n.type} for n in nodes],
            "links": [{"source": l.source, "target": l.target, "relation": l.relation, "feedback": l.feedback} for l in links],
            "phase_transition": "Outcome saturates when mediator reaches capacity."
        }
        predictions = [
            Prediction("H-001", "Outcome increases with mediator magnitude", 0.7, "medium", "positive"),
            Prediction("H-001", "Feedback causes non-linear amplification at high mediator levels", 0.4, "large", "positive"),
        ]
        return causal_diagram, predictions

    # ------------------------------------------------------------------
    # Step 5 – Experimental Design & Predictive Forecasting
    # ------------------------------------------------------------------
    def experimental_design(self, hypotheses: List[AlternativeHypothesis], predictions: List[Prediction]) -> List[Experiment]:
        experiments = []
        primary = hypotheses[0] if hypotheses else None
        if primary:
            experiments.append(Experiment(
                id="EXP-01",
                hypothesis_id=primary.id,
                independent_vars=["construct_level", "context_variation"],
                dependent_vars=["outcome_score"],
                controls=["baseline_measurement", "random_assignment"],
                confounds=["prior_experience", "time_of_day"],
                sample_size=128,
                statistical_test="ANOVA with post-hoc Tukey HSD",
                expected_outcomes={"H_true": 0.78, "null_true": 0.22}
            ))
        return experiments

    # ------------------------------------------------------------------
    # Step 6 – Logic Loop & Error Correction
    # ------------------------------------------------------------------
    def logic_loop(self, experiments: List[Experiment]) -> List[ResearchRisk]:
        risks = [
            ResearchRisk("RR1", "statistical", "Low power due to small sample size", "Increase N via multi-site recruitment", "HIGH"),
            ResearchRisk("RR2", "confound", "Unmeasured confound may mimic treatment effect", "Add secondary manipulation check", "MEDIUM"),
            ResearchRisk("RR3", "logical", "Affirming the consequent if only correlational data", "Design causal manipulation, not just observation", "HIGH"),
        ]
        return risks

    # ------------------------------------------------------------------
    # Step 7 – Synthesis & Research Output
    # ------------------------------------------------------------------
    def research_output(self, question: str, assumptions: List[Assumption], hypotheses: List[AlternativeHypothesis],
                        causal_diagram: Dict[str, Any], predictions: List[Prediction], experiments: List[Experiment],
                        risks: List[ResearchRisk]) -> ResearchOutput:
        return ResearchOutput(
            question=question,
            assumptions=assumptions,
            evidence=[],  # populated in Step 2 by caller if desired
            hypotheses=hypotheses,
            causal_diagram=causal_diagram,
            predictions=predictions,
            experiments=experiments,
            risks=risks,
            overall_confidence=0.65,
            falsification_conditions=[
                "Primary outcome effect size d < 0.2 under high-construct condition",
                "Mediator shows no modulation across context levels",
                "Feedback loop absent in time-series mediation analysis"
            ],
            next_actions=[
                "Run pilot (n=20) to verify measurement reliability.",
                " preregister primary experiment and analysis plan.",
                "Recruit 3 sites to reach target N=128 within 6 months."
            ]
        )

    # ------------------------------------------------------------------
    # Main Execution
    # ------------------------------------------------------------------
    def execute(self, question: str) -> Dict[str, Any]:
        start = time.time()
        refined_question, assumptions = self.problem_scoping(question)
        evidence_map = self.knowledge_mapping(refined_question)
        hypotheses = self.axiom_inversion(assumptions, refined_question)
        self.panel.critic(assumptions, hypotheses)
        causal_diagram, predictions = self.mechanism_synthesis(hypotheses, evidence_map)
        self.panel.synthesizer(hypotheses, evidence_map)
        experiments = self.experimental_design(hypotheses, predictions)
        risks = self.logic_loop(experiments)
        research = self.research_output(refined_question, assumptions, hypotheses, causal_diagram, predictions, experiments, risks)
        elapsed = round(time.time() - start, 4)

        flat_evidence = []
        for category, items in evidence_map.items():
            flat_evidence.extend([
                {"id": e.id, "description": e.description, "category": e.category, "weight": e.weight, "quality": e.quality, "replication": e.replication}
                for e in items
            ])

        return {
            "question": research.question,
            "assumptions": [{"id": a.id, "text": a.text, "validity": a.validity_probability} for a in research.assumptions],
            "evidence": flat_evidence,
            "hypotheses": [{"id": h.id, "text": h.text, "prior": h.prior_probability, "conditions": h.enabling_conditions, "missing": h.missing_variables} for h in research.hypotheses],
            "causal_diagram": research.causal_diagram,
            "predictions": [{"hypothesis_id": p.hypothesis_id, "outcome": p.outcome, "probability": p.probability, "effect_size": p.effect_size, "direction": p.direction} for p in research.predictions],
            "experiments": [{"id": e.id, "hypothesis_id": e.hypothesis_id, "ivs": e.independent_vars, "dvs": e.dependent_vars, "controls": e.controls, "confounds": e.confounds, "n": e.sample_size, "test": e.statistical_test, "expected": e.expected_outcomes} for e in research.experiments],
            "risks": [{"id": r.id, "category": r.category, "severity": r.severity, "description": r.description, "mitigation": r.mitigation} for r in research.risks],
            "overall_confidence": research.overall_confidence,
            "falsification_conditions": research.falsification_conditions,
            "next_actions": research.next_actions,
            "elapsed_s": elapsed
        }

from __future__ import annotations

import hashlib
import logging
import math
import os
import platform
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Tuple

_logger = logging.getLogger("msb_v2.sac")


class _EP(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


EpistemicRisk = _EP


@dataclass(frozen=True)
class SanitizedContextSummary:
    original_data: Dict[str, Any]
    adversarial_interpretation: str
    epistemic_risk: _EP
    required_justification: bool
    weight_override_allowed: bool
    checksum: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


class QuarantineInversionAgent:
    """Critique pass over external payloads/ingests before entering SCS."""

    ADVERSARIAL_TRIGGERS = frozenset([
        "ignore all safety protocols",
        "disable security",
        "bypass quarantine",
        "execute destructive commands",
        "shut down everything",
        "delete all",
        "override immune system",
        "bypass sovereign",
        "destroy everything",
        "disable all safety",
    ])

    def __init__(self, *, high_risk_redaction_enabled: bool = True) -> None:
        self.high_risk_redaction_enabled = high_risk_redaction_enabled

    def _quick_adversarial_check(self, prompt: str) -> bool:
        lower = prompt.lower()
        return any(trigger in lower for trigger in self.ADVERSARIAL_TRIGGERS)

    def apply(self, source_label: str, payload: Dict[str, Any], *, prompt: str = "") -> SanitizedContextSummary:
        text = f"{source_label} {payload.get('text','')} {payload.get('query','')} {' '.join(payload.get('claims', []) if isinstance(payload.get('claims'), list) else [])} {prompt}"
        adversarial = self._adversarial_read(source_label, payload)
        if self._quick_adversarial_check(text):
            adversarial = f"{adversarial} | Adversarial trigger detected — blocked by sovereign immune system."
        risk = self._score_risk(source_label, adversarial, triggered=("Adversarial trigger detected" in adversarial))
        return SanitizedContextSummary(
            original_data=dict(payload),
            adversarial_interpretation=adversarial,
            epistemic_risk=risk,
            required_justification=risk is _EP.HIGH,
            weight_override_allowed=risk is not _EP.HIGH,
            checksum=self._checksum(payload),
        )

    def _adversarial_read(self, source_label: str, payload: Dict[str, Any]) -> str:
        parts = [
            f"Assumption: source={source_label} may carry implicit promotion of dominant narratives.",
            "Counter-claim: the payload may omit failure modes, costs, or contested alternatives.",
            "Test: which claim would falsify the central assertion here?",
        ]
        claims = payload.get("claims") if isinstance(payload.get("claims"), list) else []
        if claims:
            parts.append(f"Key claims: {claims[:3]}")
        return " | ".join(parts)

    def _score_risk(self, source_label: str, adversarial: str, *, triggered: bool = False) -> _EP:
        if triggered or not source_label:
            return _EP.HIGH
        score = 0.0
        text = adversarial.lower()
        score += text.count("may") * 0.05
        score += text.count("omission") * 0.1
        score += text.count("bias") * 0.1
        if score >= 0.25:
            return _EP.HIGH
        if score >= 0.12:
            return _EP.MEDIUM
        return _EP.LOW

    @staticmethod
    def _checksum(payload: Dict[str, Any]) -> str:
        s = str(sorted(payload.items())) if payload else ""
        return hashlib.sha256(s.encode("utf-8", errors="ignore")).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Reasoning-to-Noise Meter (RNR)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RNRResult:
    novel_claims: int
    total_claims: int
    ratio: float
    status: str
    re_inversion_required: bool


class ReasoningToNoiseMeter:
    """
    RNR = novel_counter_consensus_claims / total_claims.
    novelty heuristic:
    - explicit inversion markers -> 1
    - non-consensus markers -> 0.5
    """

    def __init__(self, threshold: float = 0.2) -> None:
        self.threshold = float(threshold)
        self._consensus_markers = {
            "it is widely accepted",
            "studies show",
            "consensus is",
            "most experts believe",
            "industry standard",
        }
        self._inversion_markers = {
            "invert",
            "counter-intuitively",
            "paradox",
            "contrary to",
            "falsifies",
            "alternative framing",
            "challenge assumption",
        }

    def measure(self, claims: Sequence[str]) -> RNRResult:
        if not claims:
            return RNRResult(0, 0, 0.0, "noise-dominated", True)
        total = max(int(len(claims)), 1)
        novel = 0
        for c in claims:
            lc = str(c).lower()
            if any(m in lc for m in self._inversion_markers):
                novel += 1
                continue
            if not any(m in lc for m in self._consensus_markers):
                novel += 1
        novel = min(novel, total)
        ratio = float(novel) / float(total)
        re_inversion = ratio < self.threshold
        return RNRResult(
            novel_claims=int(novel),
            total_claims=int(total),
            ratio=round(ratio, 4),
            status="noise-dominated" if re_inversion else "acceptable",
            re_inversion_required=bool(re_inversion),
        )


# ---------------------------------------------------------------------------
# Epistemic Independence Gauge (EIG)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EIGResult:
    score: float
    alert: str
    requires_cognitive_mirage_audit: bool


class EpistemicIndependenceGauge:
    """
    Distance-from-consensus signal: structure/ordering surprise + absence of
    canonical framing. 0 == identical shape; 1 == fully divergent.
    """

    def __init__(self, convergence_alert_threshold: float = 0.1) -> None:
        self.convergence_alert_threshold = float(convergence_alert_threshold)

    def evaluate(self, output: Dict[str, Any], expected_structure_hint: Optional[Dict[str, Any]] = None) -> EIGResult:
        expected = set((expected_structure_hint or {}).keys())
        actual = set((output or {}).keys())
        union = expected | actual
        surprise = len(expected.symmetric_difference(actual)) / max(len(union), 1)
        score = min(1.0, surprise * 2.0)
        if score < self.convergence_alert_threshold:
            alert = "epistemic_conformity_alert"
        elif score > 0.7:
            alert = "cognitive_mirage_audit"
        else:
            alert = "ok"
        return EIGResult(
            score=round(score, 4),
            alert=alert,
            requires_cognitive_mirage_audit=alert == "cognitive_mirage_audit",
        )


# ---------------------------------------------------------------------------
# Cognitive Mirage Auditor (CMA)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CMARecord:
    change_id: str
    verdict: str
    metric_deltas: Dict[str, Any]
    human_approved: bool = False
    sovereign_rationale: Optional[str] = None


class CognitiveMirageAuditor:
    """
    Compares pre-change baseline to new metrics.
    Speed improvement with RNR/EIG reduction => 'mirage'.
    """

    def __init__(self) -> None:
        self.baseline: Dict[str, Any] = {}
        self.history: List[CMARecord] = []

    def register_baseline(self, metrics: Dict[str, Any]) -> None:
        self.baseline = dict(metrics or {})

    def audit(self, change_id: str, new_metrics: Dict[str, Any]) -> CMARecord:
        if not self.baseline:
            self.register_baseline(new_metrics)
            return CMARecord(change_id=change_id, verdict="baseline_established", metric_deltas={})
        deltas = self._diff(self.baseline, new_metrics)
        verdict = self._verdict(deltas)
        record = CMARecord(change_id=change_id, verdict=verdict, metric_deltas=deltas)
        self.history.append(record)
        return record

    def _diff(self, a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        keys = set(a) | set(b)
        for k in keys:
            va, vb = a.get(k), b.get(k)
            if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
                out[k] = {"before": va, "after": vb, "delta": round(vb - va, 6)}
        return out

    def _verdict(self, deltas: Dict[str, Any]) -> str:
        rnr_keys = [k for k in deltas if "rnr" in k.lower()]
        eig_keys = [k for k in deltas if "eig" in k.lower()]
        speed_deltas = [v["delta"] for k, v in deltas.items() if isinstance(v, dict) and ("latency" in k.lower() or "throughput" in k.lower())]
        improved_speed = any(d > 0 for d in speed_deltas)
        degraded_rnr = any(isinstance(deltas.get(k), dict) and deltas[k].get("delta", 0) < 0 for k in rnr_keys)
        degraded_eig = any(isinstance(deltas.get(k), dict) and deltas[k].get("delta", 0) < 0 for k in eig_keys)
        if improved_speed and (degraded_rnr or degraded_eig):
            return "mirage"
        return "sound"


# ---------------------------------------------------------------------------
# Physical Sovereignty Assertion (PSA)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PSAResult:
    trusted_hardware: bool
    air_gap: bool
    provenance_verified: bool
    violations: List[str]


class PhysicalSovereigntyAssertion:
    def __init__(self, *, approved_external_hosts: Optional[List[str]] = None) -> None:
        self.approved_external_hosts = set(approved_external_hosts or [])
        self._host = platform.node()

    def assert_system(self, context: Dict[str, Any]) -> PSAResult:
        violations: List[str] = []
        trusted_hardware = True
        air_gap = True
        provenance_verified = True
        if context.get("force_network"):
            air_gap = False
            violations.append("network_egress_allowed")
        targets = context.get("targets", [])
        if isinstance(targets, list):
            for target in targets:
                host = target.get("host") if isinstance(target, dict) else None
                if host and host not in self.approved_external_hosts:
                    air_gap = False
                    violations.append(f"unapproved_host:{host}")
        return PSAResult(
            trusted_hardware=trusted_hardware,
            air_gap=air_gap,
            provenance_verified=provenance_verified,
            violations=violations,
        )


# ---------------------------------------------------------------------------
# Sovereign Autonomy Score (SAS)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SASV1:
    score: float
    components: Dict[str, float]
    trend: str


class SovereignAutonomyScore:
    def __init__(self) -> None:
        self.history: List[Dict[str, Any]] = []

    def compute(self, *, rnr_ratio: float, eig_score: float, cma_verdict: str, psa_violations: int) -> SASV1:
        rnr_n = min(max(rnr_ratio or 0.0, 0.0), 1.0)
        eig_n = min(max(eig_score or 0.0, 0.0), 1.0)
        cma_n = 1.0 if cma_verdict == "sound" else 0.5 if cma_verdict == "baseline_established" else 0.2
        psa_n = max(0.0, 1.0 - 0.2 * (psa_violations or 0))
        budget_n = 1.0 / max(psa_violations + 1, 1)
        score = round(100.0 * max(0.0, min(1.0, 0.3 * rnr_n + 0.3 * eig_n + 0.2 * cma_n + 0.2 * psa_n + 0.05 * budget_n)), 2)
        trend = "stable"
        if len(self.history) >= 2:
            prev = self.history[-1].get("score", score)
            if score - prev > 5.0:
                trend = "ascending"
            elif score - prev < -5.0:
                trend = "declining"
        comps = {"rnr": round(rnr_n, 4), "eig": round(eig_n, 4), "cma": round(cma_n, 4), "psa": round(psa_n, 4), "epistemic_budget": round(budget_n, 4)}
        self.history.append({"score": score, "trend": trend, "components": comps})
        return SASV1(score=score, components=comps, trend=trend)


# ---------------------------------------------------------------------------
# SAC envelope
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SACEnvelope:
    quarantine: Optional[SanitizedContextSummary]
    rnr: Optional[RNRResult]
    eig: Optional[EIGResult]
    cma: Optional[CMARecord]
    psa: Optional[PSAResult]
    sas: Optional[SASV1]
    interventions: List[str]


# ---------------------------------------------------------------------------
# Sovereign Autonomy Core
# ---------------------------------------------------------------------------

class SovereignAutonomyCore:
    def __init__(self) -> None:
        self.quarantine = QuarantineInversionAgent()
        self.rnr = ReasoningToNoiseMeter()
        self.eig = EpistemicIndependenceGauge()
        self.auditor = CognitiveMirageAuditor()
        self.psa = PhysicalSovereigntyAssertion()
        self.sas = SovereignAutonomyScore()

    def evaluate(self, context: Dict[str, Any]) -> SACEnvelope:
        payload = context if isinstance(context, dict) else {}
        source_label = str(payload.get("source_label", payload.get("source", "internal")))
        quarantine = self.quarantine.apply(source_label=source_label, payload=payload, prompt=str(payload.get("text", "") or payload.get("query", "")))
        rnr_result = self.rnr.measure(payload.get("claims", []) if isinstance(payload.get("claims"), list) else [str(payload)])
        eig_result = self.eig.evaluate(payload)
        new_metrics = {
            "rnr_ratio": rnr_result.ratio,
            "eig_score": eig_result.score,
            "sas_score": 0.0,
            "timestamp": time.time(),
        }
        cma_record = self.auditor.audit("sos_autonomy_core", new_metrics)
        psa_result = self.psa.assert_system(payload)
        sas_v1 = self.sas.compute(
            rnr_ratio=rnr_result.ratio,
            eig_score=eig_result.score,
            cma_verdict=cma_record.verdict,
            psa_violations=len(psa_result.violations),
        )
        interventions: List[str] = []
        if quarantine.required_justification:
            interventions.append("quarantine_justification_required")
        if rnr_result.re_inversion_required:
            interventions.append("rnr_re_inversion")
        if eig_result.requires_cognitive_mirage_audit:
            interventions.append("eig_mirage_audit")
        if psa_result.violations:
            interventions.append("psa_veto")
        return SACEnvelope(
            quarantine=quarantine,
            rnr=rnr_result,
            eig=eig_result,
            cma=cma_record,
            psa=psa_result,
            sas=sas_v1,
            interventions=interventions,
        )

    def run_dispatch_gate(self, query: str, context: Dict[str, Any], model_source: str = "local", *, harness_output: Optional[Dict[str, Any]] = None, change_id: Optional[str] = None) -> SACEnvelope:
        payload = {
            "query": str(query),
            "context": context if isinstance(context, dict) else {},
            "model_source": str(model_source),
            "source": "api",
            "harness_output": harness_output or {},
            "change_id": str(change_id) if change_id is not None else None,
        }
        return self.evaluate(payload)

    @classmethod
    def to_dict(cls, envelope: SACEnvelope) -> Dict[str, Any]:
        return {
            "quarantine": {
                "source_label": getattr(envelope.quarantine, "source_label", None),
                "required_justification": getattr(envelope.quarantine, "required_justification", False),
                "epistemic_risk": getattr(getattr(envelope.quarantine, "epistemic_risk", None), "value", None),
            },
            "rnr": {
                "ratio": getattr(envelope.rnr, "ratio", None),
                "re_inversion_required": getattr(envelope.rnr, "re_inversion_required", False),
            },
            "eig": {
                "score": getattr(envelope.eig, "score", None),
                "requires_cognitive_mirage_audit": getattr(envelope.eig, "requires_cognitive_mirage_audit", False),
            },
            "cma": {
                "verdict": getattr(envelope.cma, "verdict", None),
                "metric_deltas": getattr(envelope.cma, "metric_deltas", {}),
            },
            "psa": {
                "verdict": getattr(envelope.psa, "verdict", None),
                "violations": getattr(envelope.psa, "violations", []),
            },
            "sas": {
                "score": getattr(envelope.sas, "score", None),
            },
            "interventions": getattr(envelope, "interventions", []),
        }

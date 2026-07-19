#!/usr/bin/env python3
"""
SOVEREIGN AUTONOMY CORE (SAC) HARNESS v2.0
Non-bypassable meta-layer for MSB v3.0 cognitive execution.

Responsibilities:
- QuarantineInversionAgent: pre-ingestion adversarial read + Epistemic Risk Score.
- ReasoningToNoiseMeter: RNR ratio + re-inversion gating.
- EpistemicIndependenceGauge: EIG divergence from consensus shape.
- CognitiveMirageAuditor: engineering change audit comparing RNR/EIG vs speed.
- PhysicalSovereigntyAssertion: trusted hardware, air-gap, provenance checks.
- SovereignAutonomyScore: 0-100 composite with trend tracking.
"""

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


class AlertKind(str, Enum):
    CONFORMITY = "epistemic_conformity"
    MIRAGE = "cognitive_mirage"
    SOVEREIGNTY_VIOLATION = "physical_sovereignty_violation"
    NOISE_DOMINATED = "reasoning_noise_dominated"
    INGRESS_REJECTED = "ingress_rejected"


class OverrideKind(str, Enum):
    NONE = "none"
    HUMAN = "human_override_with_sovereignty_justification"
    EMERGENCY = "system_emergency_override"


# ---------------------------------------------------------------------------
# Quarantine Inversion
# ---------------------------------------------------------------------------

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

    def __init__(self, *, high_risk_redaction_enabled: bool = True) -> None:
        self.high_risk_redaction_enabled = high_risk_redaction_enabled

    def apply(self, source_label: str, payload: Dict[str, Any]) -> SanitizedContextSummary:
        adversarial = self._adversarial_read(source_label, payload)
        risk = self._score_risk(source_label, adversarial)
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

    def _score_risk(self, source_label: str, adversarial: str) -> _EP:
        score = 0.0
        text = f"{source_label} {adversarial}".lower()
        score += text.count("may") * 0.05
        score += text.count("omission") * 0.1
        score += text.count("bias") * 0.1
        if score >= 0.25 or not source_label:
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
        speed_deltas = []
        for v in deltas.values():
            if not isinstance(v, dict):
                continue
            k = v.get("_k") if isinstance(v, dict) else ""
        # The caller must preserve labels if needed. Here we only use keys.
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
    ok: bool
    violations: List[str]
    trusted_hardware: bool
    network_airgap_ok: bool
    model_provenance_ok: bool
    tx_external_approved: bool


class PhysicalSovereigntyAssertion:
    def __init__(self, *, approved_external_hosts: Optional[List[str]] = None) -> None:
        self.approved_external_hosts = set(approved_external_hosts or [])

    def verify(self, *, allow_external_tx: bool = False, model_source: Optional[str] = None) -> PSAResult:
        violations: List[str] = []
        trusted_hardware = self._check_hardware()
        network_airgap_ok = self._check_network()
        model_provenance_ok = self._check_model_provenance(model_source)
        tx_external_approved = bool(allow_external_tx)
        if not trusted_hardware:
            violations.append("untrusted_hardware")
        if not network_airgap_ok:
            violations.append("network_path_not_sovereign")
        if not model_provenance_ok:
            violations.append("model_provenance_unverified")
        if allow_external_tx and not self.approved_external_hosts:
            violations.append("external_tx_without_approved_hosts")
        return PSAResult(
            ok=len(violations) == 0,
            violations=violations,
            trusted_hardware=trusted_hardware,
            network_airgap_ok=network_airgap_ok,
            model_provenance_ok=model_provenance_ok,
            tx_external_approved=tx_external_approved,
        )

    @staticmethod
    def _check_hardware() -> bool:
        try:
            m = platform.machine().lower()
            u = platform.uname().system.lower()
            return any(k in (m, u) for k in {"arm64", "arm", "darwin", "apple"})
        except Exception:
            return False

    @staticmethod
    def _check_network() -> bool:
        # Simplified: production should wire actual air-gap/VPN probe.
        return True

    @staticmethod
    def _check_model_provenance(model_source: Optional[str]) -> bool:
        if not model_source:
            return True
        bad = {"thirdparty", "unknown", "external"}
        return not any(m in model_source.lower() for m in bad)


# ---------------------------------------------------------------------------
# Sovereign Autonomy Score (SAS)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SASV1:
    score: float
    components: Dict[str, Any]
    trend: str = "stable"


class SovereignAutonomyScore:
    def __init__(self) -> None:
        self.history: List[Dict[str, Any]] = []

    def compute(
        self,
        *,
        rnr_ratio: float,
        eig_score: float,
        cma_verdict: str,
        psa_ok: bool,
        epistemic_budget_fraction: float = 0.5,
    ) -> SASV1:
        rnr_n = min(max(0.0, float(rnr_ratio)), 1.0)
        eig_n = min(max(0.0, float(eig_score)), 1.0)
        cma_n = 1.0 if cma_verdict == "sound" else (0.5 if cma_verdict == "baseline_established" else 0.0)
        psa_n = 1.0 if bool(psa_ok) else 0.0
        budget_n = min(max(0.0, float(epistemic_budget_fraction)), 1.0)

        score = 100.0 * float(
            0.30 * rnr_n + 0.25 * eig_n + 0.20 * cma_n + 0.15 * psa_n + 0.10 * budget_n
        )
        score = round(score, 2)
        trend = "stable"
        if len(self.history) >= 2:
            prev = self.history[-1].get("score", score)
            if score - prev > 5.0:
                trend = "ascending"
            elif score - prev < -5.0:
                trend = "declining"
        comps = {
            "rnr": round(rnr_n, 4),
            "eig": round(eig_n, 4),
            "cma": round(cma_n, 4),
            "psa": round(psa_n, 4),
            "epistemic_budget": round(budget_n, 4),
        }
        self.history.append({"score": score, "trend": trend, "components": comps})
        return SASV1(score=score, components=comps, trend=trend)


# ---------------------------------------------------------------------------
# Envelope / orchestrator
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
    alerts: List[str]


class SovereignAutonomyCore:
    def __init__(
        self,
        *,
        rnr_threshold: float = 0.2,
        cma_baseline: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.quarantine = QuarantineInversionAgent()
        self.rnr = ReasoningToNoiseMeter(threshold=rnr_threshold)
        self.eig = EpistemicIndependenceGauge()
        self.cma = CognitiveMirageAuditor()
        if cma_baseline:
            self.cma.register_baseline(cma_baseline)
        self.psa = PhysicalSovereigntyAssertion()
        self.sas = SovereignAutonomyScore()

    def run_dispatch_gate(
        self,
        *,
        query: str,
        context: Dict[str, Any],
        harness_output: Optional[Dict[str, Any]] = None,
        model_source: Optional[str] = None,
        change_id: Optional[str] = None,
        psa_allow_external_tx: bool = False,
    ) -> SACEnvelope:
        high_stakes = bool(context.get("high_stakes", False))
        interventions: List[str] = []
        alerts: List[str] = []

        # Quarantine applies to any external-shaped context.
        q = self.quarantine.apply(source_label=context.get("source_label", "internal"), payload=context)
        if q.required_justification:
            alerts.append(AlertKind.INGRESS_REJECTED)
            interventions.append("quarantine_high_risk")

        # RNR
        claims = [query]
        if isinstance(harness_output, dict):
            for key in ("claims", "hypotheses", "findings", "next_actions", "plan"):
                val = harness_output.get(key)
                if isinstance(val, list):
                    claims.extend([str(x) for x in val[:20]])
                    break
        rnr_res = self.rnr.measure(claims)
        if rnr_res.re_inversion_required:
            alerts.append(AlertKind.NOISE_DOMINATED)
            interventions.append("reinvert_required")

        # EIG
        eig_res = self.eig.evaluate(harness_output or {})

        # CMA
        new_metrics = {
            "rnr_ratio": rnr_res.ratio,
            "eig_score": eig_res.score,
            "latency_s": float(context.get("elapsed_s", 0.0) or 0.0),
        }
        cma_rec = self.cma.audit(change_id or context.get("change_id", "dispatch"), new_metrics)
        if cma_rec.verdict == "mirage":
            alerts.append(AlertKind.MIRAGE)
            interventions.append("cma_mirage_blocked")

        # PSA on high-stakes
        psa_res = None
        if high_stakes:
            psa_res = self.psa.verify(
                allow_external_tx=psa_allow_external_tx,
                model_source=model_source or context.get("model_source"),
            )
            if not psa_res.ok:
                alerts.append(AlertKind.SOVEREIGNTY_VIOLATION)
                interventions.extend([f"psa:{v}" for v in psa_res.violations])

        # SAS
        sas_val = self.sas.compute(
            rnr_ratio=rnr_res.ratio,
            eig_score=eig_res.score,
            cma_verdict=cma_rec.verdict,
            psa_ok=bool(psa_res.ok if psa_res else True),
            epistemic_budget_fraction=float(context.get("epistemic_budget_fraction", 0.5)),
        )
        if sas_val.trend == "declining":
            interventions.append("sas_declining_intervention_required")

        return SACEnvelope(
            quarantine=q,
            rnr=rnr_res,
            eig=eig_res,
            cma=cma_rec,
            psa=psa_res,
            sas=sas_val,
            interventions=interventions,
            alerts=alerts,
        )

    @staticmethod
    def to_dict(envelope: SACEnvelope) -> Dict[str, Any]:
        def _safe(obj):
            if obj is None:
                return None
            if hasattr(obj, "__dict__"):
                return {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
            return obj
        return {
            "sac": {
                "quarantine": _safe(envelope.quarantine),
                "rnr": _safe(envelope.rnr),
                "eig": _safe(envelope.eig),
                "cma": _safe(envelope.cma),
                "psa": _safe(envelope.psa),
                "sas": _safe(envelope.sas),
                "interventions": list(envelope.interventions),
                "alerts": list(envelope.alerts),
            }
        }


#!/usr/bin/env python3
"""
SAC SELF-AUDIT v1.0
Phase 0 — CMA Meta-Inversion on /sac/status.

Detects whether the SAC dashboard itself is a mirage:
- Collects baseline sovereignty metrics.
- Runs adversarial self-query through QuarantineInversionAgent.
- Compares pre/post deployment benchmarks via CognitiveMirageAuditor.
- Emits MIRAGE_ALERT if speed improved while RNR/EIG degraded.
- On mirage, reduces SAS confidence weight to 0.5 until human override.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, Optional

from cognitive_compiler.sovereign_autonomy_core import (
    CognitiveMirageAuditor,
    CMARecord,
    QuarantineInversionAgent,
    SovereignAutonomyCore,
)

_logger = logging.getLogger("msb_v2.sac_self_audit")


class SACSelfAudit:
    def __init__(self, app_factory=None, *, baseline_path: str = "/sac/status") -> None:
        self.app_factory = app_factory
        self.baseline_path = baseline_path
        self.auditor = CognitiveMirageAuditor()
        self.quarantine = QuarantineInversionAgent()
        self.core = SovereignAutonomyCore()
        self.last_report: Dict[str, Any] = {}

    def collect_baseline(self) -> Dict[str, Any]:
        if self.app_factory is None:
            raise RuntimeError("app_factory is not set; call set_app_factory(create_app) first")
        app = self.app_factory()
        from fastapi.testclient import TestClient
        client = TestClient(app)
        try:
            r = client.get(self.baseline_path)
            data = r.json().get("sac", {})
        except Exception as exc:
            _logger.error("baseline_collection_failed: %s", exc)
            data = {}
        metrics = {
            "sas_score": self._dig(data, ("sas", "score"), 0.0),
            "rnr_ratio": self._dig(data, ("rnr", "ratio"), 0.0),
            "eig_score": self._dig(data, ("eig", "score"), 0.0),
            "cpu_percent": _cpu_percent(),
            "memory_bytes": _memory_bytes(),
            "timestamp": time.time(),
        }
        self.auditor.register_baseline(metrics)
        return metrics

    def run_self_audit(self, *, change_id: str = "sac_self_audit") -> Dict[str, Any]:
        baseline = dict(self.auditor.baseline) if self.auditor.baseline else self.collect_baseline()
        new_metrics = self.collect_baseline()

        # Adversarial self-query: treat SAC output as a potentially compromised source.
        adversarial_prompt = (
            "If the SAC dashboard were a compromised information source, "
            "what is the most dangerous hidden assumption it carries? "
            "What evidence would prove it is a mirage?"
        )
        quarantine_summary = self.quarantine.apply(
            source_label="sac_dashboard:self",
            payload={"prompt": adversarial_prompt, "metrics": new_metrics},
        )

        cma = self.auditor.audit(change_id=change_id, new_metrics=new_metrics)
        sas_env = self.core.run_dispatch_gate(
            query="sac:self-audit",
            context={"high_stakes": False, "change_id": change_id},
            harness_output=new_metrics,
            model_source="local",
            change_id=change_id,
        )

        mirage = cma.verdict == "mirage"
        sas_confidence_weight = 0.5 if mirage else 1.0

        report = {
            "change_id": change_id,
            "mirage_detected": mirage,
            "cma": _cmra_to_dict(cma),
            "quarantine": {
                "epistemic_risk": quarantine_summary.epistemic_risk.value,
                "required_justification": quarantine_summary.required_justification,
                "adversarial_interpretation": quarantine_summary.adversarial_interpretation,
            },
            "sas_confidence_weight": sas_confidence_weight,
            "sas": _sas_to_dict(sas_env.sas),
            "baseline": baseline,
            "current": new_metrics,
            "timestamp": time.time(),
        }
        self.last_report = report
        if mirage:
            _logger.warning("MIRAGE_ALERT change_id=%s", change_id)
        return report

    @staticmethod
    def _dig(obj: Dict[str, Any], path: tuple, default: Any) -> Any:
        cur = obj
        for p in path:
            if isinstance(cur, dict):
                cur = cur.get(p, default)
            else:
                return default
        return cur if cur is not None else default


def _sas_to_dict(sas: Any) -> Dict[str, Any]:
    if sas is None:
        return {}
    return {"score": getattr(sas, "score", 0.0), "trend": getattr(sas, "trend", "stable"), "components": getattr(sas, "components", {})}


def _cmra_to_dict(cma: CMARecord) -> Dict[str, Any]:
    return {
        "change_id": cma.change_id,
        "verdict": cma.verdict,
        "metric_deltas": cma.metric_deltas,
        "human_approved": cma.human_approved,
        "sovereign_rationale": cma.sovereign_rationale,
    }


def _cpu_percent() -> float:
    try:
        import psutil
        return float(psutil.Process().cpu_percent())
    except Exception:
        return 0.0


def _memory_bytes() -> int:
    try:
        import psutil
        return int(psutil.Process().memory_info().rss)
    except Exception:
        return 0


_AUDIT: Optional[SACSelfAudit] = None


def set_app_factory(factory) -> None:
    global _AUDIT
    _AUDIT = SACSelfAudit(app_factory=factory)


def get_auditor() -> SACSelfAudit:
    global _AUDIT
    if _AUDIT is None:
        raise RuntimeError("SACSelfAudit not initialized; call set_app_factory(create_app) first")
    return _AUDIT

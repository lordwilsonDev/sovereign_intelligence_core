"""Sovereign Artifact Quarantine Gate service."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from msb_v2.audit.sovereign.merkle import AuditMerkleChain
from msb_v2.pipeline.metrics import PIPELINE_DECISIONS_TOTAL, PIPELINE_FTS_AVERAGE, PIPELINE_SAS_AVERAGE
from msb_v2.pipeline.sovereign_artifact_quarantine import SovereignArtifactQuarantine

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GateDecision:
    artifact_id: str
    verdict: str
    sas_a: float
    sas: float
    rnr: float
    fts: float
    reason: Optional[str] = None
    audit_receipt: Optional[str] = None


class SovereignGate:
    def __init__(self, root: Optional[str] = None, threshold: float = 80.0) -> None:
        self.root = Path(root) if root else Path.cwd()
        self.threshold = float(threshold)
        audit_path = self.root / ".pipeline" / "sovereign_gate.jsonl"
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        self.audit_chain = AuditMerkleChain(audit_path)
        self.quarantine = SovereignArtifactQuarantine(root=str(self.root))

    def evaluate(self, metrics: Dict[str, Any]) -> GateDecision:
        sas = float(metrics.get("sas", 0.0))
        fts = float(metrics.get("fts", 0.0))
        rnr = float(metrics.get("rnr", 0.0))
        sas_a = float(metrics.get("sas_a", 0.0))
        artifact_id = str(metrics.get("artifact_id") or metrics.get("id") or "unknown")
        reason = None
        if sas_a < self.threshold:
            reason = f"SAS-A {sas_a:.2f} below threshold {self.threshold:.2f}"
        elif fts > 0.5:
            reason = f"FTS {fts:.2f} exceeds limit 0.50"
        elif sas_a < 100.0 and fts > 0.3:
            reason = f"combined sovereignty degradation: SAS-A {sas_a:.2f}, FTS {fts:.2f}"
        verdict = "REJECT" if reason else "PASS"
        event = {
            "type": "SOVEREIGN_GATE_DECISION",
            "artifact_id": artifact_id,
            "verdict": verdict,
            "sas_a": sas_a,
            "sas": sas,
            "rnr": rnr,
            "fts": fts,
            "reason": reason,
        }
        try:
            PIPELINE_SAS_AVERAGE.labels(stage="gate").set(sas_a)
            PIPELINE_FTS_AVERAGE.labels(stage="gate").set(fts)
            PIPELINE_DECISIONS_TOTAL.labels(verdict=verdict).inc()
        except Exception:
            pass
        try:
            receipt = self.audit_chain.append(event)
        except Exception:
            receipt = None
        return GateDecision(
            artifact_id=artifact_id,
            verdict=verdict,
            sas_a=sas_a,
            sas=sas,
            rnr=rnr,
            fts=fts,
            reason=reason,
            audit_receipt=receipt,
        )

    def assess(self, image_name: str) -> Dict[str, Any]:
        artifact = {"id": image_name, "kind": "image", "name": image_name}
        result = self.quarantine.run_quarantine(artifact)
        metrics = {
            "artifact_id": result.get("artifact_id", image_name),
            "sas": float(result.get("sas", 0.0)),
            "rnr": float(result.get("rnr", 0.0)),
            "fts": float(result.get("fts", 0.0)),
            "sas_a": float(result.get("sas_a", 0.0)),
        }
        decision = self.evaluate(metrics)
        payload = dict(metrics)
        payload["verdict"] = decision.verdict
        payload["reason"] = decision.reason
        payload["audit_receipt"] = decision.audit_receipt
        return payload

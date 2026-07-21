"""Pipeline sovereignty API router."""

from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends

from msb_v2.api.middleware import require_bearer_token
from msb_v2.pipeline.sovereign_gate import SovereignGate

pipeline_router = APIRouter()


@pipeline_router.post("/assess")
def assess_pipeline_artifact(
    payload: Dict[str, Any],
    _auth: str = Depends(require_bearer_token),
) -> Dict[str, Any]:
    gate = SovereignGate()
    metrics = {
        "artifact_id": str(payload.get("artifact_id") or payload.get("id") or payload.get("image") or "unknown"),
        "sas": float(payload.get("sas", 0.0)),
        "rnr": float(payload.get("rnr", 0.0)),
        "fts": float(payload.get("fts", 0.0)),
        "sas_a": float(payload.get("sas_a", 0.0)),
    }
    decision = gate.evaluate(metrics)
    return {
        "verdict": decision.verdict,
        "artifact_id": decision.artifact_id,
        "sas_a": decision.sas_a,
        "sas": decision.sas,
        "rnr": decision.rnr,
        "fts": decision.fts,
        "reason": decision.reason,
        "audit_receipt": decision.audit_receipt,
    }


router = pipeline_router

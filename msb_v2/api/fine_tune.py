from __future__ import annotations

import os
import sys
from dataclasses import asdict
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from msb_v2.api.middleware import require_bearer_token

from cognitive_compiler.sovereign_finetune_harness_v1 import SovereignFineTuningHarness

router = APIRouter(tags=["fine-tuning"])

_UNSLOTH_REPO_PATH = "/Users/lordwilson/unsloth"


class ScanRequest(BaseModel):
    repo_path: str
    privacy_boundary: str = "local-only"


class DistillRequest(BaseModel):
    repo_path: str
    max_pairs: int = 64
    chunk_words: int = 512
    overlap: int = 64


class TrainRequest(BaseModel):
    repo_path: str
    base_model: str


def _ensure_unsloth_available() -> Dict[str, Any]:
    sys.path.insert(0, _UNSLOTH_REPO_PATH)
    try:
        import unsloth  # noqa: F401
        return {"unsloth_available": True, "repo": _UNSLOTH_REPO_PATH}
    except Exception as exc:
        return {"unsloth_available": False, "error": str(exc), "repo": _UNSLOTH_REPO_PATH}


@router.post("/fine-tune/scan")
def fine_tune_scan(body: ScanRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    if not os.path.isdir(body.repo_path):
        raise HTTPException(status_code=400, detail="repo_path must be a directory")
    harness = SovereignFineTuningHarness(repo_path=body.repo_path, privacy_boundary=body.privacy_boundary)
    report = harness.scan_documents()
    availability = _ensure_unsloth_available()
    return {
        "source_hash": report.source_hash,
        "document_count": len(report.documents),
        "total_tokens": report.total_tokens,
        "recommendation": report.recommendation,
        "assumption_risks": [asdict(r) for r in report.assumption_risks],
        "failure_patterns": report.failure_patterns,
        "unsloth": availability,
    }


@router.post("/fine-tune/distill")
def fine_tune_distill(body: DistillRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    if not os.path.isdir(body.repo_path):
        raise HTTPException(status_code=400, detail="repo_path must be a directory")
    harness = SovereignFineTuningHarness(repo_path=body.repo_path)
    pairs = harness.synthesize_pairs(max_pairs=body.max_pairs, chunk_words=body.chunk_words, overlap=body.overlap)
    validation = harness.validate_pairs()
    return {
        "pairs_generated": len(pairs),
        "validation": validation,
        "privacy_boundary": harness.privacy_boundary,
    }


@router.post("/fine-tune/train")
def fine_tune_train(body: TrainRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    if not os.path.isdir(body.repo_path):
        raise HTTPException(status_code=400, detail="repo_path must be a directory")
    harness = SovereignFineTuningHarness(repo_path=body.repo_path)
    harness.scan_documents()
    harness.synthesize_pairs()
    job = harness.create_training_job(base_model=body.base_model)
    baseline = harness.validate_baseline_coherence()
    report = harness.run_post_training_validation(job_id=job.job_id)
    unsloth = _ensure_unsloth_available()
    return {
        "job_id": job.job_id,
        "status": job.status,
        "dataset_size": job.dataset_size,
        "baseline_coherence": baseline,
        "unsloth": unsloth,
        "integration_report": {
            "model_name": report.model_name,
            "validation_passed": report.validation_passed,
            "coherence_score": report.coherence_score,
            "confidence_score": report.confidence_score,
            "recommendation": report.recommendation,
            "falsification_condition": report.falsification_condition,
        },
    }

from __future__ import annotations

import hashlib
from typing import Any, Dict

from fastapi import APIRouter
from pydantic import BaseModel

from msb_v2.engine.merkle_reasoning import MerkleReasoningChain

router = APIRouter()


class MerkleVerifyRequest(BaseModel):
    root: str
    step_id: str
    step_type: str
    payload: Dict[str, Any]
    prev_hash: str
    step_hash: str


class SemanticDriftRequest(BaseModel):
    expected: str
    actual: str


def _verify_step(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


@router.post("/verification/merkle")
def verify_merkle(payload: MerkleVerifyRequest) -> Dict[str, Any]:
    result = _verify_step(payload.root, payload.step_id, payload.step_type, payload.payload, payload.prev_hash, payload.step_hash)
    return {"status": "ok", "result": result}


@router.post("/semantic/drift")
def semantic_drift(payload: SemanticDriftRequest) -> Dict[str, Any]:
    expected_tokens = payload.expected.split()
    actual_tokens = payload.actual.split()
    expected_set = set(expected_tokens)
    actual_set = set(actual_tokens)
    jaccard = len(expected_set & actual_set) / max(1, len(expected_set | actual_set))
    drift_score = 1.0 - jaccard
    status = "ok"
    detail = "within tolerance"
    if drift_score > 0.5:
        status = "drift"
        detail = "semantic boundary exceeded"
    elif drift_score > 0.2:
        status = "watch"
        detail = "minor drift detected"
    chain = MerkleReasoningChain()
    chain.append("semantic-drift", {"drift_score": drift_score, "status": status})
    return {
        "status": status,
        "drift_score": drift_score,
        "detail": detail,
        "root": chain.root_hash(),
        "expected_tokens": len(expected_tokens),
        "actual_tokens": len(actual_tokens),
    }

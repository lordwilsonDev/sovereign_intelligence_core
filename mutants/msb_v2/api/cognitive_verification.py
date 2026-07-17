from __future__ import annotations

import hashlib
from typing import Any, Dict

from fastapi import APIRouter
from pydantic import BaseModel

from msb_v2.engine.merkle_reasoning import MerkleReasoningChain

router = APIRouter()


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


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
mutants_x__verify_step__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__verify_step__mutmut)
def _verify_step(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_orig(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_1(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = None
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_2(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"XXstep_idXX": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_3(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"STEP_ID": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_4(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "XXstep_typeXX": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_5(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "STEP_TYPE": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_6(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "XXpayloadXX": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_7(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "PAYLOAD": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_8(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "XXprevXX": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_9(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "PREV": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_10(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = None
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_11(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(None).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_12(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode(None)).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_13(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(None).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_14(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("XXutf-8XX")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_15(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("UTF-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_16(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = None
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_17(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed != step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_18(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = None
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_19(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root != step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_20(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else True
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_21(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"XXvalidXX": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_22(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"VALID": valid, "chain_valid": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_23(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "XXchain_validXX": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_24(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "CHAIN_VALID": chain_valid, "computed": computed, "provided": step_hash}


def x__verify_step__mutmut_25(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "XXcomputedXX": computed, "provided": step_hash}


def x__verify_step__mutmut_26(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "COMPUTED": computed, "provided": step_hash}


def x__verify_step__mutmut_27(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "XXprovidedXX": step_hash}


def x__verify_step__mutmut_28(root: str, step_id: str, step_type: str, payload: Dict[str, Any], prev_hash: str, step_hash: str) -> Dict[str, Any]:
    raw = {"step_id": step_id, "step_type": step_type, "payload": payload, "prev": prev_hash}
    computed = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()
    valid = computed == step_hash
    chain_valid = root == step_hash if valid else False
    return {"valid": valid, "chain_valid": chain_valid, "computed": computed, "PROVIDED": step_hash}

mutants_x__verify_step__mutmut['_mutmut_orig'] = x__verify_step__mutmut_orig # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_1'] = x__verify_step__mutmut_1 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_2'] = x__verify_step__mutmut_2 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_3'] = x__verify_step__mutmut_3 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_4'] = x__verify_step__mutmut_4 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_5'] = x__verify_step__mutmut_5 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_6'] = x__verify_step__mutmut_6 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_7'] = x__verify_step__mutmut_7 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_8'] = x__verify_step__mutmut_8 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_9'] = x__verify_step__mutmut_9 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_10'] = x__verify_step__mutmut_10 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_11'] = x__verify_step__mutmut_11 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_12'] = x__verify_step__mutmut_12 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_13'] = x__verify_step__mutmut_13 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_14'] = x__verify_step__mutmut_14 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_15'] = x__verify_step__mutmut_15 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_16'] = x__verify_step__mutmut_16 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_17'] = x__verify_step__mutmut_17 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_18'] = x__verify_step__mutmut_18 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_19'] = x__verify_step__mutmut_19 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_20'] = x__verify_step__mutmut_20 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_21'] = x__verify_step__mutmut_21 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_22'] = x__verify_step__mutmut_22 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_23'] = x__verify_step__mutmut_23 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_24'] = x__verify_step__mutmut_24 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_25'] = x__verify_step__mutmut_25 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_26'] = x__verify_step__mutmut_26 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_27'] = x__verify_step__mutmut_27 # type: ignore # mutmut generated
mutants_x__verify_step__mutmut['x__verify_step__mutmut_28'] = x__verify_step__mutmut_28 # type: ignore # mutmut generated


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

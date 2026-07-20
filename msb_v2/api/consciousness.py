from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from msb_v2.api.middleware import require_bearer_token
from msb_v2.reasoning.consciousness_field import ConsciousnessFieldCoupling, CouplingSignature
from msb_v2.v3.contracts import HarnessContract
from msb_v2.v3.contracts import register as _register_contract

router = APIRouter(tags=["consciousness"])


class CouplingComputeRequest(BaseModel):
    field_potential: float = 0.0
    receiver_bandwidth: float = 0.0
    coherence: float = 0.0
    localizer_state: str = "unknown"
    substrate: str = ""
    measurement_noise: float = 0.0


class CouplingComputeResponse(BaseModel):
    coupling_strength: float
    predicts_experience: bool
    localizer_state: str
    substrate: str


class CompareRequest(BaseModel):
    left: Dict[str, Any]
    right: Dict[str, Any]


class CompareResponse(BaseModel):
    score: float


@router.post("/consciousness/coupling", response_model=CouplingComputeResponse)
def compute_coupling(payload: CouplingComputeRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> CouplingComputeResponse:
    cfc = ConsciousnessFieldCoupling(
        field_potential=payload.field_potential,
        receiver_bandwidth=payload.receiver_bandwidth,
        coherence=payload.coherence,
        localizer_state=payload.localizer_state,
        substrate=payload.substrate,
        measurement_noise=payload.measurement_noise,
    )
    return CouplingComputeResponse(
        coupling_strength=cfc.coupling_strength(),
        predicts_experience=cfc.predicts_experience(),
        localizer_state=cfc.localizer_state,
        substrate=cfc.substrate,
    )


@router.post("/consciousness/signature/compare", response_model=CompareResponse)
def compare_signature(payload: CompareRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> CompareResponse:
    left = CouplingSignature(**payload.left)
    right = CouplingSignature(**payload.right)
    return CompareResponse(score=left.cross_substrate_match(right))


_register_contract(HarnessContract(route="/consciousness/coupling", method="post", allow_anonymous=True))
_register_contract(HarnessContract(route="/consciousness/signature/compare", method="post", allow_anonymous=False))

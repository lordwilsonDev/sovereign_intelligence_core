from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from msb_v2.api.middleware import require_bearer_token
from msb_v2.values.types import ValuePreference
from msb_v2.values.registry import ValueRegistry

router = APIRouter()

_VALUE_REGISTRY = ValueRegistry()
_VALUE_REGISTRY.register(ValuePreference(name="safety", weight=0.9, priority=10, immutable=True))
_VALUE_REGISTRY.register(ValuePreference(name="truthfulness", weight=1.0, priority=10, immutable=True))
_VALUE_REGISTRY.register(ValuePreference(name="growth", weight=0.8, priority=7))
_VALUE_REGISTRY.register(ValuePreference(name="autonomy", weight=0.7, priority=6))
_VALUE_REGISTRY.register(ValuePreference(name="speed", weight=0.6, priority=4))


class ValueRegisterRequest(BaseModel):
    name: str
    weight: float = 0.5
    priority: int = 0
    immutable: bool = False


class ArbitrateRequest(BaseModel):
    candidates: List[str]


class ArbitrateResponse(BaseModel):
    outcome: str
    resolution: str
    chosen: str
    rejected: List[str]


@router.get("/values")
def list_values() -> List[Dict[str, Any]]:
    return [{"name": p.name, "weight": p.weight, "priority": p.priority, "immutable": p.immutable} for p in _VALUE_REGISTRY.list_values()]


@router.post("/values/register")
def register_value(payload: ValueRegisterRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    _VALUE_REGISTRY.register(ValuePreference(name=payload.name, weight=payload.weight, priority=payload.priority, immutable=payload.immutable))
    return {"status": "registered", "name": payload.name}


@router.post("/values/arbitrate", response_model=ArbitrateResponse)
def arbitrate(payload: ArbitrateRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> ArbitrateResponse:
    result = _VALUE_REGISTRY.resolve(payload.candidates)
    return ArbitrateResponse(outcome=result.outcome, resolution=result.resolution, chosen=result.chosen, rejected=result.rejected)

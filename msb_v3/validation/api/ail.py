from __future__ import annotations

import logging
from typing import Any, Dict, List

from fastapi import APIRouter
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class AssumptionMineRequest(BaseModel):
    text: str


class AssumptionResponse(BaseModel):
    statement: str
    confidence: str
    evidence: List[str]


class InversionRequest(BaseModel):
    assumption: str


router = APIRouter()


@router.post("/validation/ail/mine")
def mine_assumptions(payload: AssumptionMineRequest) -> Dict[str, Any]:
    from msb_v3.validation.ail.assumption_miner import miner as _miner
    assumptions = _miner().mine(payload.text)
    return {"count": len(assumptions), "assumptions": [AssumptionResponse(statement=a.statement, confidence=a.confidence, evidence=a.evidence).model_dump() for a in assumptions]}


@router.post("/validation/ail/invert")
def invert_assumption(payload: InversionRequest) -> Dict[str, Any]:
    assumption = str(payload.assumption).strip()
    inversions = [assumption.replace("is", "is not"), f"What prevents {assumption}"]
    return {"assumption": assumption, "inversions": inversions}

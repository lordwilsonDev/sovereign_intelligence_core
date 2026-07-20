from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from msb_v2.api.middleware import require_bearer_token
from msb_v2.v3.contracts import HarnessContract, register as _register_contract
from msb_v2.audit.sac_audit import get_audit_log

router = APIRouter(tags=["audit"])


class SacRecentResponse(BaseModel):
    events: List[Dict[str, Any]]


@router.get("/recent", dependencies=[Depends(require_bearer_token)])
def sac_recent(limit: int = 100) -> SacRecentResponse:
    return SacRecentResponse(events=get_audit_log().recent(limit=limit))


_register_contract(HarnessContract(route="/audit/sac/recent", method="get", allow_anonymous=False))

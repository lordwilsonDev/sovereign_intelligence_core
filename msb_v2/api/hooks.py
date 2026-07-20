from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from msb_v2.api.middleware import require_bearer_token
from msb_v2.v3.contracts import HarnessContract, register as _register_contract

router = APIRouter(tags=["hooks"])


class SquadHookEvent(BaseModel):
    kind: str
    subject: str
    payload: Dict[str, Any] | None = None
    trace_id: str | None = None


@router.post("/event", dependencies=[Depends(require_bearer_token)])
def squad_hook_event(event: SquadHookEvent) -> Dict[str, Any]:
    print("HOOK HIT", event.kind)
    return {"status": "queued", "kind": event.kind, "subject": event.subject}


_register_contract(HarnessContract(route="/hooks/event", method="post", allow_anonymous=False))

from __future__ import annotations

import logging
import threading
import time
from collections import deque
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from msb_v2.api.middleware import require_bearer_token
from msb_v2.v3.contracts import HarnessContract, register as _register_contract

router = APIRouter(tags=["observability"])
_lock = threading.Lock()
_events: deque[Dict[str, Any]] = deque(maxlen=2000)
_started = datetime.now(timezone.utc)


@router.get("/observability/health")
def observability_health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "uptime_seconds": int((datetime.now(timezone.utc) - _started).total_seconds()),
        "event_log_length": len(_events),
    }


@router.get("/observability/squads")
def observability_squads() -> Dict[str, Any]:
    return {
        "squads": [
            {
                "id": "squad-chief",
                "role": "orchestrator",
                "children": ["squad-designer", "squad-engineer", "squad-verifier"],
            }
        ],
        "hooks": {
            "post_task": "log_to_observability",
            "post_memory": "update_honcho_router",
        },
    }


@router.post("/observability/hooks/event")
def observability_hook_event(payload: Dict[str, Any], auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    event = {
        "received_at": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }
    with _lock:
        _events.append(event)
    return {"accepted": True, "event_count": len(_events)}


@router.get("/observability/hooks/events")
def observability_hook_events(limit: int = 50) -> Dict[str, Any]:
    with _lock:
        items = list(_events)[-max(1, limit) :]
    return {"count": len(items), "events": items}


# HCL contracts
_register_contract(HarnessContract(route="/observability/health", method="get", allow_anonymous=True))
_register_contract(HarnessContract(route="/observability/squads", method="get", allow_anonymous=True))
_register_contract(HarnessContract(route="/observability/hooks/event", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/observability/hooks/events", method="get", allow_anonymous=False))

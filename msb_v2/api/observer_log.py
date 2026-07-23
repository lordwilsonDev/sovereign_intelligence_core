"""Observer's Log API — read the organism's narrative stream."""
from fastapi import APIRouter

from msb_v2.observer_log.engine import ObserverLog

router = APIRouter(tags=["observer-log"])
_log = ObserverLog()


@router.get("/recent")
def recent_thoughts(limit: int = 20):
    return {"thoughts": _log.recent(limit)}


@router.post("/emit")
def emit_thought(payload: dict):
    source = str(payload.get("source", ""))
    message = str(payload.get("message", ""))
    priority = str(payload.get("priority", "info"))
    if not source or not message:
        return {"detail": "source and message are required"}
    _log.emit(source=source, message=message, priority=priority)
    return {"status": "emitted"}


@router.post("/clear")
def clear_thoughts():
    _log.log_path.write_text("")
    return {"status": "cleared"}

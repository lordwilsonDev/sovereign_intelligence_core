from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from msb_v2.reasoning.integrity import EventKind, EventStreamStore, ExecutionEvent

router = APIRouter(tags=["reasoning"])
_stream = EventStreamStore()


class EventIn(BaseModel):
    event_id: str
    kind: EventKind
    source: str
    payload: dict = Field(default_factory=dict)
    trace_id: str | None = None
    decision_id: str | None = None


@router.post("/events")
def append_event(body: EventIn) -> dict:
    event = ExecutionEvent(
        event_id=body.event_id,
        sequence=0,
        kind=body.kind,
        source=body.source,
        payload=body.payload,
        trace_id=body.trace_id,
        decision_id=body.decision_id,
    )
    stored = _stream.append(event)
    return {
        "event_id": stored.event_id,
        "sequence": stored.sequence,
        "kind": stored.kind.value,
        "ts": stored.ts,
    }


@router.get("/events")
def list_events(limit: int = 100) -> list[dict]:
    events = _stream.global_stream(limit=min(max(limit, 1), 500))
    return [
        {
            "event_id": e.event_id,
            "sequence": e.sequence,
            "kind": e.kind.value,
            "source": e.source,
            "payload": e.payload,
            "trace_id": e.trace_id,
            "decision_id": e.decision_id,
            "ts": e.ts,
        }
        for e in events
    ]


@router.get("/events/trace/{trace_id}")
def events_for_trace(trace_id: str) -> dict:
    events = _stream.events_for_trace(trace_id)
    if not events:
        raise HTTPException(status_code=404, detail="trace not found")
    return {
        "trace_id": trace_id,
        "events": [
            {
                "event_id": e.event_id,
                "sequence": e.sequence,
                "kind": e.kind.value,
                "source": e.source,
                "payload": e.payload,
                "ts": e.ts,
            }
            for e in events
        ],
    }


@router.get("/trace/{trace_id}")
def materialize_trace(trace_id: str) -> dict:
    events = _stream.events_for_trace(trace_id)
    if not events:
        raise HTTPException(status_code=404, detail="trace not found")
    return {
        "trace_id": trace_id,
        "trace": _stream.materialize_trace(trace_id),
        "verify": _stream.verify_continuity(trace_id),
    }


@router.get("/trace/verify/{decision_id}")
def verify_trace(decision_id: str) -> dict:
    return _stream.verify_integrity(decision_id)

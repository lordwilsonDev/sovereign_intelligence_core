from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel

from msb_v2.api.middleware import require_bearer_token
from msb_v2.reasoning.integrity import EventKind, ExecutionEvent
from msb_v2.api.reasoning_integrity import _stream

from msb_v2.v3.contracts import HarnessContract
from msb_v2.v3.contracts import register as _register_contract
router = APIRouter()


class AdkQueryRequest(BaseModel):
  query: str
  trace_id: Optional[str] = None
  simulate: bool = True
  answer: Optional[str] = None

_ADK_AVAILABLE = False
try:
  from google.adk.events.event import Event  # noqa
  _ADK_AVAILABLE = True
except Exception:
  _ADK_AVAILABLE = False


def _simulate_events(trace_id: str, query: str, answer: str) -> list[dict[str, Any]]:
  return [
    {
      "kind": EventKind.TOOL.value,
      "event_id": f"{trace_id}-t1",
      "sequence": 1,
      "source": "adk.tool.retriever",
      "payload": {"step": 1, "query": query, "returned_ids": ["mem-local-1"], "result_disposition": "used", "verdict": "accepted"},
      "trace_id": trace_id,
    },
    {
      "kind": EventKind.MEMORY_READ.value,
      "event_id": f"{trace_id}-t2",
      "sequence": 2,
      "source": "adk.memory.search",
      "payload": {"step": 2, "query": query, "returned_ids": ["mem-local-2"], "result_disposition": "used", "verdict": "accepted"},
      "trace_id": trace_id,
    },
    {
      "kind": EventKind.EXECUTION.value,
      "event_id": f"{trace_id}-exec",
      "sequence": 3,
      "source": "adk.llm.runner",
      "payload": {"query": query, "answer": answer},
      "trace_id": trace_id,
    },
    {
      "kind": EventKind.CONFIDENCE_ASSESSMENT.value,
      "event_id": f"{trace_id}-score",
      "sequence": 4,
      "source": "msb.scorer",
      "payload": {"score": 0.95, "confidence": 0.90, "entropy": 0.2, "concurrence": 2.0, "dissent": 0.0},
      "trace_id": trace_id,
    },
  ]


@router.post("/query-adk", dependencies=[Depends(require_bearer_token)])
def demo_query_adk(payload: AdkQueryRequest) -> Dict[str, Any]:
  trace_id = payload.trace_id or f"adk-{hash(payload.query) % 100000}"
  answer = payload.answer or "adk simulated response"

  adk_events = _simulate_events(trace_id, payload.query, answer)
  for event in adk_events:
    _stream.append(
      ExecutionEvent(
        event_id=event.get("event_id", ""),
        sequence=int(event.get("sequence", 0)),
        kind=EventKind(event.get("kind", "execution")),
        source=event.get("source", ""),
        payload=event.get("payload") or {},
        trace_id=event.get("trace_id"),
      )
    )

  return {
    "query": payload.query,
    "answer": answer,
    "trace_id": trace_id,
    "adk_available": _ADK_AVAILABLE,
    "adk_events": [
      {
        "kind": e.get("kind"),
        "source": e.get("source"),
        "event_id": e.get("event_id"),
        "payload": e.get("payload"),
      }
      for e in adk_events
    ],
    "adk_session_id": None,
    "adk_run_id": None,
    "adk_error": None,
  }
# HCL contract registration
_register_contract(HarnessContract(route="/adk/query-adk", method="post", allow_anonymous=False))

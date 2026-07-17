from __future__ import annotations

import os
from typing import Any, Dict

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from msb_v2.reasoning.integrity import EventKind, ExecutionEvent
from msb_v2.reasoning.scorer import ConfidenceAssessment, score_from_events
from msb_v2.api.reasoning_integrity import _stream
from msb_v2.core.budget_manager import CognitiveBudgetManager
from msb_v2.memory.types import MemoryConfidence, MemoryRecord

router = APIRouter()


def _scorer_enabled() -> bool:
    val = os.getenv("MSB_REASONING_SCORER", "")
    return val == "1" or val.lower() in ("true", "yes")


budget_mgr = CognitiveBudgetManager()


class DemoQueryRequest(BaseModel):
    query: str
    trace_id: str
    accepted: bool = False


def _default_events(trace_id: str, query: str, accepted: bool) -> list[dict]:
    tool_events = [
        {
            "kind": EventKind.TOOL.value if i % 2 == 1 else EventKind.MEMORY_READ.value,
            "event_id": f"{trace_id}-t{i}",
            "sequence": i,
            "source": "demo.retriever" if i % 2 == 1 else "memory.search",
            "payload": {
                "step": i,
                "query": query,
                "returned_ids": [f"mem-local-{i}"],
                "result_disposition": "used",
                "verdict": "accepted" if accepted else "rejected",
            },
            "trace_id": trace_id,
        }
        for i in range(1, 5)
    ]
    human_event = {
        "kind": EventKind.HUMAN.value,
        "event_id": f"{trace_id}-h",
        "sequence": 5,
        "source": "user.feedback",
        "payload": {"verdict": "accepted" if accepted else "rejected"},
        "trace_id": trace_id,
    }
    return [*tool_events, human_event]


def _build_events(trace_id: str, query: str, accepted: bool, answer: str) -> list[dict]:
    events = _default_events(trace_id, query, accepted)
    events.append(
        {
            "kind": "execution",
            "event_id": f"{trace_id}-exec",
            "sequence": 6,
            "source": "msb.executor",
            "payload": {"query": query, "answer": answer},
            "trace_id": trace_id,
        }
    )
    return events


def _append_events(events: list[dict]) -> None:
    for event in events:
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


def _assess(events: list[dict], accepted: bool) -> Dict[str, Any]:
    assessment = score_from_events(events)
    payload = ConfidenceAssessment(
        trace_id=events[-1].get("trace_id", ""),
        statement_id=f"{events[-1].get('trace_id', '')}-final",
        score=assessment.score,
        confidence=assessment.confidence,
        concurrence=assessment.concurrence,
        dissent=assessment.dissent,
        entropy=assessment.entropy,
        ground_truth_accepted=accepted,
        notes="compared against user acceptance",
    ).payload()
    _stream.append(
        ExecutionEvent(
            event_id=f"{events[-1].get('trace_id', '')}-final",
            sequence=len(events) + 1,
            kind=EventKind.CONFIDENCE_ASSESSMENT,
            source="scorer",
            payload=payload,
            trace_id=events[-1].get("trace_id"),
        )
    )
    return payload


def _run_adk_query(trace_id: str, query: str) -> str:
    try:
        from google.adk import Agent
        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService
        from google.genai import types

        root_agent = Agent(
            name="msb_demo_agent",
            model="gemini-2.0-flash-exp",
            instruction="You are MSB demo agent.",
        )
        session_service = InMemorySessionService()
        runner = Runner(agent=root_agent, session_service=session_service)
        session = session_service.create_session(
            app_name="msb_demo",
            user_id="local",
            session_id=trace_id,
        )
        events = list(
            runner.run(
                user_id="local",
                session_id=session.id,
                new_message=types.Content(parts=[types.Part(text=query)]),
            )
        )
        text_parts = [
            part.text for event in events for part in (event.content.parts or []) if hasattr(part, "text") and part.text
        ]
        answer = "".join(text_parts).strip() or "[ADK empty response]"
        exec_event = ExecutionEvent(
            event_id=f"{trace_id}-adk-exec",
            sequence=4,
            kind=EventKind.EXECUTION,
            source="adk.runner",
            payload={"query": query, "answer": answer, "events": len(events)},
            trace_id=trace_id,
        )
        _stream.append(exec_event)
        return answer
    except Exception as exc:
        fallback = f"[ADK unavailable: {exc.__class__.__name__}]"
        exec_event = ExecutionEvent(
            event_id=f"{trace_id}-adk-fallback",
            sequence=4,
            kind=EventKind.EXECUTION,
            source="msb.fallback",
            payload={"query": query, "answer": fallback, "error": str(exc)},
            trace_id=trace_id,
        )
        _stream.append(exec_event)
        return fallback


@router.post("/query")
def demo_query(payload: DemoQueryRequest) -> Dict[str, Any]:
    if not _scorer_enabled():
        return {"query": payload.query, "answer": "local demo answer", "confidence_assessment": None}

    trace_id = payload.trace_id
    if budget_mgr._circuit.open:
        return JSONResponse(
            status_code=503,
            content={
                "detail": "Service unavailable - cognitive circuit breaker open",
                "trace_id": trace_id,
                "reason": "metabolic_collapse_veto",
            },
        )
    if not budget_mgr.can_execute(trace_id):
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Budget exceeded - request rejected",
                "trace_id": trace_id,
                "reason": "budget_exhausted",
            },
        )
    with budget_mgr.track(trace_id) as ctx:
        events = _build_events(trace_id, payload.query, payload.accepted, "local demo answer")
        _append_events(events)
        budget_mgr.increment_tool_calls(trace_id)
        budget_mgr.increment_depth(trace_id)

        full_events = [
            {
                "kind": e.kind.value,
                "event_id": e.event_id,
                "trace_id": e.trace_id,
                "payload": e.payload or {},
            }
            for e in _stream.events_for_trace(trace_id)
        ]
        assessment_payload = _assess(full_events, payload.accepted)

        try:
            store = _get_store()
            store.add(
                MemoryRecord(
                    id=f"demo-{trace_id}",
                    kind="experience",
                    content=payload.query,
                    confidence=MemoryConfidence(
                        source_reliability=0.9 if payload.accepted else 0.4,
                        verification_interval_days=1,
                    ),
                    tags=["demo", "query"],
                    outcome="success" if payload.accepted else "failure",
                    provenance={
                        "trace_id": trace_id,
                        "accepted": payload.accepted,
                        "confidence": assessment_payload.get("confidence"),
                    },
                )
            )
            _stream.append(
                ExecutionEvent(
                    event_id=f"{trace_id}-mem",
                    sequence=len(events) + 2,
                    kind=EventKind.MEMORY_WRITE,
                    source="demo.query",
                    payload={
                        "memory_id": f"demo-{trace_id}",
                        "content": payload.query,
                        "source_reliability": 0.9 if payload.accepted else 0.4,
                    },
                    trace_id=trace_id,
                )
            )
            try:
                store.verify(f"demo-{trace_id}")
            except Exception:
                pass
        except Exception:
            pass

        return {
            "query": payload.query,
            "answer": events[-1]["payload"].get("answer", "local demo answer") if events else "local demo answer",
            "trace_id": trace_id,
            "confidence_assessment": assessment_payload,
            "budget": {
                "breached": ctx.breached,
                "breach_reason": ctx.breach_reason,
                "depth": ctx.depth,
                "tool_calls": ctx.tool_calls,
            },
        }


@router.post("/query-adk")
def demo_query_adk(payload: DemoQueryRequest) -> Dict[str, Any]:
    if not _scorer_enabled():
        return {
            "query": payload.query,
            "answer": "local demo answer",
            "confidence_assessment": None,
            "adk_events": [],
            "adk_session_id": None,
            "adk_run_id": None,
            "adk_error": None,
        }
    answer = _run_adk_query(payload.trace_id, payload.query)
    events = _build_events(payload.trace_id, payload.query, payload.accepted, answer)
    _append_events(events)
    full_events = [
        {
            "kind": e.kind.value,
            "event_id": e.event_id,
            "trace_id": e.trace_id,
            "payload": e.payload or {},
        }
        for e in _stream.events_for_trace(payload.trace_id)
    ]
    assessment_payload = _assess(full_events, payload.accepted)
    return {
        "query": payload.query,
        "answer": answer,
        "trace_id": payload.trace_id,
        "confidence_assessment": assessment_payload,
    }

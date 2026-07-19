from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from msb_v2.api.middleware import require_bearer_token
from msb_v2.provider import DeepSeekProvider
from msb_v2.reasoning.integrity import EventKind, ExecutionEvent
from msb_v2.reasoning.scorer import score_from_events
from msb_v2.api.reasoning_integrity import _stream

router = APIRouter()
_provider = DeepSeekProvider()
SCORER_ENABLED = os.getenv("MSB_REASONING_SCORER", "0").lower() in ("1", "true", "yes")


class DeepSeekChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    max_tokens: int = 256
    goal: Optional[str] = None


@router.post("/chat")
def deepseek_chat(payload: DeepSeekChatRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    response: Dict[str, Any] = {}

    if SCORER_ENABLED:
        trace_id = f"chat-{abs(hash((payload.goal or '') + str(payload.messages))) % 1000000007}"
        response["trace_id"] = trace_id
        _stream.append(ExecutionEvent(
            event_id=f"{trace_id}-1",
            sequence=0,
            kind=EventKind.EXECUTION,
            source="deepseek.chat",
            payload={"goal": payload.goal, "message_count": len(payload.messages or [])},
            trace_id=trace_id,
        ))
    else:
        trace_id = None

    if payload.goal:
        result = _provider.plan(payload.goal, context=None)
        if SCORER_ENABLED:
            _stream.append(ExecutionEvent(
                event_id=f"{trace_id}-2",
                sequence=0,
                kind=EventKind.EXECUTION,
                source="deepseek.plan",
                payload={"status": result.get("status", "unknown")},
                trace_id=trace_id,
            ))
        if SCORER_ENABLED:
            assessment = score_from_events([e.payload for e in _stream.events_for_trace(trace_id)])
            assessment_payload = assessment.payload()
            assessment_payload["ground_truth_accepted"] = None
            _stream.append(ExecutionEvent(
                event_id=f"{trace_id}-a",
                sequence=0,
                kind=EventKind.CONFIDENCE_ASSESSMENT,
                source="scorer",
                payload=assessment_payload,
                trace_id=trace_id,
            ))
            response["confidence_assessment"] = assessment_payload
        return {**response, **result}

    if not payload.messages:
        return {"status": "error", "message": "missing messages", "confidence": 0.0}

    result = _provider.chat(payload.messages, max_tokens=payload.max_tokens)
    if result is None:
        return {"status": "error", "message": "missing DEEPSEEK_API_KEY", "confidence": 0.0}

    if SCORER_ENABLED:
        _stream.append(ExecutionEvent(
            event_id=f"{trace_id}-3",
            sequence=0,
            kind=EventKind.EXECUTION,
            source="deepseek.chat",
            payload={"status": "ok", "result_snippet": str(result)[:120]},
            trace_id=trace_id,
        ))
        assessment = score_from_events([e.payload for e in _stream.events_for_trace(trace_id)])
        assessment_payload = assessment.payload()
        assessment_payload["ground_truth_accepted"] = None
        _stream.append(ExecutionEvent(
            event_id=f"{trace_id}-a",
            sequence=0,
            kind=EventKind.CONFIDENCE_ASSESSMENT,
            source="scorer",
            payload=assessment_payload,
            trace_id=trace_id,
        ))
        response["confidence_assessment"] = assessment_payload

    return {**response, "result": result}
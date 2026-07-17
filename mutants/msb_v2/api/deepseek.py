from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from msb_v2.provider import DeepSeekProvider

router = APIRouter()
_provider = DeepSeekProvider()


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class DeepSeekChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    max_tokens: int = 256
    goal: Optional[str] = None


@router.post("/chat")
def deepseek_chat(payload: DeepSeekChatRequest) -> Dict[str, Any]:
    if payload.goal:
        return _provider.plan(payload.goal, context=None)
    if not payload.messages:
        return {"status": "error", "message": "missing messages", "confidence": 0.0}
    result = _provider.chat(payload.messages, max_tokens=payload.max_tokens)
    if result is None:
        return {"status": "error", "message": "missing DEEPSEEK_API_KEY", "confidence": 0.0}
    return {"status": "ok", "result": result}

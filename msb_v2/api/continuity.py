from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, Query

from msb_v2.continuity.resume_compiler import ResumePromptCompiler
from msb_v2.api.middleware import require_bearer_token

router = APIRouter()
_compiler = ResumePromptCompiler(
    project="MSB v2",
    version="v2",
)


@router.get("/resume-prompt")
def resume_prompt(
    format: Optional[str] = Query("compact", pattern="^(compact|json)$"),
    active_task: Optional[str] = Query(None),
    topic: Optional[str] = Query(None),
    last_turn_summary: Optional[str] = Query(None),
    simple_assumption_score: Optional[float] = Query(None),
    auth: dict[str, Any] = Depends(require_bearer_token),
) -> dict[str, Any]:
    if active_task is not None:
        _compiler.active_task = active_task
    if topic is not None:
        _compiler.topic = topic
    if last_turn_summary is not None:
        _compiler.last_turn_summary = last_turn_summary
    if simple_assumption_score is not None:
        _compiler.simple_assumption_score = float(simple_assumption_score)
    prompt = _compiler.compile()
    if format == "json":
        return {"prompt": prompt, "compact": _compiler.compact_text()}
    return {"prompt": prompt}

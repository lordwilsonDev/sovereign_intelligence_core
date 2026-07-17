from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter
from pydantic import BaseModel

from msb_v2.api.cognitive import _engine as cognitive_engine
from msb_v2.engine.moie_orchestrator import MoIEOrchestrator
from msb_v2.engine.rcoh import RCOH, RCOHState, Phase

router = APIRouter(tags=["brain"])


class ManifestRequest(BaseModel):
    query: str
    intent: str = "default"
    trace_id: str | None = None


def _ok(kind: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"status": "ok", "kind": kind, "payload": payload}


@router.post("/run")
def brain_run(req: ManifestRequest) -> Dict[str, Any]:
    kind = req.intent.lower()

    if kind == "debate":
        result = MoIEOrchestrator().run(req.query)
        return _ok("moie", result)

    if kind == "plan":
        state = RCOHState(
            cycle_id=f"rcoh-brain-{req.query[:20].replace(' ', '_')}",
            current_phase=Phase.OBSERVE,
            context_summary=req.query,
            goals=[req.query],
            max_iterations=3,
        )
        final = RCOH(state=state).run(max_iterations=3)
        return _ok("rcoh", {
            "cycle_id": final.cycle_id,
            "phase": final.current_phase.value,
            "confidence": final.confidence,
            "goals": final.goals,
            "alternatives_count": len(final.alternatives),
        })

    if kind == "assess":
        trace_id = req.trace_id or ""
        result = cognitive_engine.assess(trace_id)
        return _ok("cognitive", {"trace_id": trace_id, "assessment": result})

    return _ok("fallback", {"resolved": "noop", "query": req.query})

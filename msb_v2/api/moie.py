from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from msb_v2.engine.causal_memory import CausalMemory
from msb_v2.engine.crystallizer import Crystallizer
from msb_v2.engine.hive_nodes import default_nodes
from msb_v2.engine.moie_judge import Judge
from msb_v2.engine.moie_orchestrator import MoIEOrchestrator
from msb_v2.engine.rcoh_persistence import RCOHPersistence

router = APIRouter()

_moie: MoIEOrchestrator | None = None


def _get_moie() -> MoIEOrchestrator:
    global _moie
    if _moie is None:
        persistence = RCOHPersistence()
        causal_memory = CausalMemory()
        judge = Judge(persistence=persistence)
        crystallizer = Crystallizer(persistence=persistence)
        _moie = MoIEOrchestrator(judge=judge, crystallizer=crystallizer, persistence=persistence, causal_memory=causal_memory, nodes=default_nodes())
    return _moie


class QueryRequest(BaseModel):
    query: str


@router.post("/run")
def moie_run(payload: QueryRequest) -> dict[str, Any]:
    moie = _get_moie()
    result = moie.run(payload.query)
    result["status"] = "ok" if result.get("status") != "failed" else "failed"
    return result

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from msb_v2.v3.constraints import ConstraintEngine
from msb_v2.v3.inversion_registry import get_registry as _get_inversion_registry
from msb_v2.v3.memory_router import MemoryRouter
from msb_v2.v3.registry import get_registry as _get_capability_registry

router = APIRouter(tags=["v3-deliberation"])


def _mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


@router.post("/v3/deliberate")
def deliberate(payload: dict) -> JSONResponse:
    query = payload.get("query", "")
    max_rounds = int(payload.get("max_rounds", 2))
    if max_rounds < 1:
        max_rounds = 1
    if max_rounds > 3:
        max_rounds = 3
    inversion = _get_inversion_registry()
    hypotheses = inversion.list_hypotheses()[:max_rounds]
    rounds = []
    for hypothesis in hypotheses:
        experiments = inversion.experiments_for(hypothesis.hypothesis_id)
        evidence_scores = [float(e.get("evidence_score", 0.0) or 0.0) for e in experiments]
        base = _mean(evidence_scores) if evidence_scores else 0.5
        rounds.append({
            "hypothesis_id": hypothesis.hypothesis_id,
            "title": hypothesis.assumption,
            "score": round(min(1.0, max(0.0, base)), 2),
        })
    return JSONResponse({
        "query": query,
        "rounds": rounds,
        "recommended": rounds[0]["hypothesis_id"] if rounds else None,
    })

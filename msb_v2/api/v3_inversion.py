from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from msb_v2.v3.inversion_registry import get_registry as _get_inversion_registry

router = APIRouter(tags=["v3-inversion"])


@router.get("/v3/inversion/hypotheses")
def list_hypotheses() -> JSONResponse:
    registry = _get_inversion_registry()
    items = registry.list_hypotheses()
    return JSONResponse({
        "count": len(items),
        "items": [h.__dict__ for h in items],
    })


@router.get("/v3/inversion/experiments")
def list_experiments() -> JSONResponse:
    registry = _get_inversion_registry()
    items = registry.list_experiments()
    return JSONResponse({
        "count": len(items),
        "items": [e.__dict__ for e in items],
    })


@router.post("/v3/inversion/hypotheses")
def add_hypothesis(payload: dict) -> JSONResponse:
    registry = _get_inversion_registry()
    hypothesis = registry.register_hypothesis(
        title=payload.get("title", ""),
        description=payload.get("description", ""),
        assumptions=payload.get("assumptions", []),
    )
    return JSONResponse({"hypothesis_id": hypothesis.hypothesis_id})


@router.post("/v3/inversion/experiments")
def add_experiment(payload: dict) -> JSONResponse:
    registry = _get_inversion_registry()
    experiment = registry.register_experiment(
        hypothesis_id=payload.get("hypothesis_id", ""),
        description=payload.get("description", ""),
    )
    return JSONResponse({"experiment_id": experiment.experiment_id})


@router.post("/v3/inversion/experiments/{experiment_id}/evidence")
def add_evidence(experiment_id: str, payload: dict) -> JSONResponse:
    registry = _get_inversion_registry()
    evidence = registry.add_evidence(
        experiment_id=experiment_id,
        supports=bool(payload.get("supports", True)),
        score=float(payload.get("score", 0.5)),
        note=payload.get("note", ""),
    )
    return JSONResponse({"evidence_id": evidence.evidence_id})

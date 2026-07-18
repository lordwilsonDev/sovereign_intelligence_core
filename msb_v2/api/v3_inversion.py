from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from msb_v2.v3.inversion_registry import (
    Experiment,
    Hypothesis,
    get_registry,
)

router = APIRouter(tags=["v3"])


@router.post("/v3/inversion/hypotheses")
def create_hypothesis(hypothesis: Hypothesis) -> JSONResponse:
    registry = get_registry()
    registry.add_hypothesis(hypothesis)
    return JSONResponse({"added": True, "hypothesis_id": hypothesis.hypothesis_id})


@router.get("/v3/inversion/hypotheses/{hypothesis_id}")
def get_hypothesis(hypothesis_id: str) -> JSONResponse:
    registry = get_registry()
    record = registry.get_hypothesis(hypothesis_id)
    if record is None:
        return JSONResponse({"error": "not_found", "hypothesis_id": hypothesis_id}, status_code=404)
    return JSONResponse(record)


@router.post("/v3/inversion/experiments")
def create_experiment(experiment: Experiment) -> JSONResponse:
    registry = get_registry()
    registry.add_experiment(experiment)
    return JSONResponse({"added": True, "experiment_id": experiment.experiment_id})


@router.get("/v3/inversion/experiments/hypothesis/{hypothesis_id}")
def experiments_for_hypothesis(hypothesis_id: str) -> JSONResponse:
    registry = get_registry()
    return JSONResponse({"experiments": registry.experiments_for(hypothesis_id)})


@router.get("/v3/inversion/summary")
def inversion_summary() -> JSONResponse:
    return JSONResponse(get_registry().summary())

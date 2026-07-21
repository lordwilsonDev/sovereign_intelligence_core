from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Request
from pydantic import BaseModel

from msb_v2.star.engine import StarEngine

router = APIRouter()

_engine = StarEngine()


class JobCreateRequest(BaseModel):
    name: str
    cron: str = "*/15 * * * *"
    harness_action: Dict[str, Any]
    description: str = ""
    retry_policy: Dict[str, Any] | None = None
    failure_policy: str = "alert"
    active: bool = True


class JobUpdateRequest(BaseModel):
    active: bool | None = None
    cron: str | None = None
    harness_action: Dict[str, Any] | None = None


@router.get("/star/jobs")
def list_star_jobs() -> Dict[str, Any]:
    return _engine.list_jobs()


@router.post("/star/jobs")
def create_star_job(payload: JobCreateRequest) -> Dict[str, Any]:
    return _engine.create_job(payload.model_dump())


@router.get("/star/jobs/{job_id}")
def get_star_job(job_id: str) -> Dict[str, Any]:
    job = _engine.get_job(job_id)
    if job is None:
        return {"status": "not_found", "job_id": job_id}
    return job


@router.put("/star/jobs/{job_id}")
def update_star_job(job_id: str, payload: JobUpdateRequest) -> Dict[str, Any]:
    job = _engine.get_job(job_id)
    if job is None:
        return {"status": "not_found", "job_id": job_id}
    return _engine.update_job(job_id, payload.model_dump(exclude_none=True))


@router.delete("/star/jobs/{job_id}")
def delete_star_job(job_id: str) -> Dict[str, Any]:
    try:
        return _engine.delete_job(job_id)
    except KeyError:
        return {"status": "not_found", "job_id": job_id}


@router.post("/star/jobs/{job_id}/enable")
def enable_star_job(job_id: str) -> Dict[str, Any]:
    return _engine.enable_job(job_id)


@router.post("/star/jobs/{job_id}/run")
def run_star_job(job_id: str) -> Dict[str, Any]:
    return _engine.trigger(job_id)


@router.get("/star/history")
def star_history(job_id: str | None = None, limit: int = 50) -> Dict[str, Any]:
    return _engine.history(job_id=job_id, limit=limit)


@router.get("/star/status")
def star_status() -> Dict[str, Any]:
    return _engine.status()

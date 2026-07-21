from __future__ import annotations

from typing import Any, Dict

from msb_v2.star.manager import StarManager
from msb_v2.star.runner import JobRunner
from msb_v2.star.scheduler import JobDefinition, JobStore, Tracker
from msb_v2.star.manager import StarManager

class StarEngine:
    def __init__(self) -> None:
        self._job_store = JobStore()
        self._tracker = Tracker()
        self._runner = JobRunner(self._job_store, self._tracker)
        self._manager = StarManager(self._job_store, self._tracker, self._runner)

    def list_jobs(self) -> Dict[str, Any]:
        return self._manager.list_jobs()

    def create_job(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._manager.create_job(data)

    def get_job(self, job_id: str) -> Dict[str, Any]:
        job = self._manager.get_job(job_id)
        return job or {"status": "not_found", "job_id": job_id}

    def update_job(self, job_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        job = self._manager.get_job(job_id)
        if job is None:
            return {"status": "not_found", "job_id": job_id}
        return self._job_store.update_job(job_id, data)

    def delete_job(self, job_id: str) -> Dict[str, Any]:
        try:
            return self._manager.delete_job(job_id)
        except KeyError:
            return {"status": "not_found", "job_id": job_id}

    def enable_job(self, job_id: str) -> Dict[str, Any]:
        return self._manager.enable_job(job_id)

    def trigger(self, job_id: str) -> Dict[str, Any]:
        return self._manager.run_job(job_id)

    def history(self, job_id: str | None = None, limit: int = 50) -> Dict[str, Any]:
        return {"history": self._tracker.history(job_id=job_id, limit=limit)}

    def status(self) -> Dict[str, Any]:
        return {"status": "ok", "jobs": len(self._job_store.list_jobs())}

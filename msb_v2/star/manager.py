from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from msb_v2.star.scheduler import JobDefinition, JobStore, Tracker
from msb_v2.star.runner import JobRunner


class StarManager:
    def __init__(self, job_store: JobStore, tracker: Tracker, runner: JobRunner) -> None:
        self._job_store = job_store
        self._tracker = tracker
        self._runner = runner

    def create_job(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._job_store.create_job(data)

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        return self._job_store.get_job(job_id)

    def list_jobs(self) -> Dict[str, Any]:
        return {"jobs": self._job_store.list_jobs()}

    def delete_job(self, job_id: str) -> Dict[str, Any]:
        return self._job_store.delete_job(job_id)

    def run_job(self, job_id: str) -> Dict[str, Any]:
        job = self._job_store.get_job(job_id)
        if not job:
            return {"status": "not_found", "job_id": job_id}
        if not job.get("active", False):
            return {"status": "inactive", "job_id": job_id}
        run = self._runner.run(JobDefinition(**{k: v for k, v in job.items() if k in JobDefinition.__dataclass_fields__}))
        if run.status == "FAILED" and self._tracker.detect_failure_cluster(job_id):
            self._job_store.update_job(job_id, {"active": False})
            try:
                requests.post(
                    "http://127.0.0.1:8767/sn/notify",
                    json={
                        "source": "star",
                        "priority": "critical",
                        "template": "job_failed",
                        "template_data": {
                            "job_name": job.get("name") or job_id,
                            "error": "failure cluster detected; job disabled",
                            "run_id": run.run_id,
                            "timestamp": run.finished_at,
                        },
                        "channels": ["console"],
                        "require_ack": False,
                        "expires_in_seconds": 3600,
                    },
                    timeout=3,
                )
            except Exception:
                pass
        return {"status": "dispatched", "run_id": run.run_id, "job_id": job_id}

    def enable_job(self, job_id: str) -> Dict[str, Any]:
        job = self._job_store.get_job(job_id)
        if not job:
            return {"status": "not_found", "job_id": job_id}
        self._job_store.update_job(job_id, {"active": True})
        return {"status": "enabled", "job_id": job_id}

from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JOBS_PATH = ROOT / "star" / "jobs.json"
DEFAULT_HISTORY_PATH = ROOT / "star" / "job_history.jsonl"


@dataclass
class JobDefinition:
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    name: str = ""
    description: str = ""
    cron: str = "*/15 * * * *"
    harness_action: Dict[str, Any] = field(default_factory=dict)
    retry_policy: Dict[str, Any] = field(default_factory=lambda: {"max_retries": 2, "backoff_factor": 2.0})
    failure_policy: str = "alert"
    active: bool = True
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class JobRun:
    job_id: str
    run_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    status: str = "RUNNING"
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    finished_at: str = ""
    duration_ms: int = 0
    output_summary: str = ""
    audit_hash: str = ""
    attempt: int = 1


class JobStore:
    def __init__(self, jobs_path: Path = DEFAULT_JOBS_PATH) -> None:
        self._jobs_path = jobs_path
        self._jobs: Dict[str, JobDefinition] = {}
        self._load()

    def _load(self) -> None:
        if not self._jobs_path.exists():
            return
        payload = json.loads(self._jobs_path.read_text())
        for item in payload.get("jobs", []):
            job = JobDefinition(**{k: v for k, v in item.items() if k in JobDefinition.__dataclass_fields__})
            self._jobs[job.id] = job

    def _persist(self) -> None:
        self._jobs_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"jobs": [_job_to_dict(job) for job in self._jobs.values()]}
        self._jobs_path.write_text(json.dumps(payload, indent=2))

    def list_jobs(self) -> List[Dict[str, Any]]:
        return [_job_to_dict(job) for job in self._jobs.values()]

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        job = self._jobs.get(job_id)
        return _job_to_dict(job) if job else None

    def create_job(self, data: Dict[str, Any]) -> Dict[str, Any]:
        existing = next((job for job in self._jobs.values() if job.name == data.get("name")), None)
        if existing:
            raise ValueError(f"job name already exists: {data['name']}")
        job = JobDefinition(**{k: v for k, v in data.items() if k in JobDefinition.__dataclass_fields__})
        self._jobs[job.id] = job
        self._persist()
        return _job_to_dict(job)

    def update_job(self, job_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        job = self._jobs.get(job_id)
        if not job:
            raise KeyError(f"unknown job id: {job_id}")
        for key, value in data.items():
            if key in JobDefinition.__dataclass_fields__:
                setattr(job, key, value)
        self._persist()
        return _job_to_dict(job)

    def delete_job(self, job_id: str) -> Dict[str, Any]:
        job = self._jobs.pop(job_id, None)
        if not job:
            raise KeyError(f"unknown job id: {job_id}")
        self._persist()
        return _job_to_dict(job)


class Tracker:
    def __init__(self, history_path: Path = DEFAULT_HISTORY_PATH) -> None:
        self._history_path = history_path
        self._history_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_header()

    def _ensure_header(self) -> None:
        if not self._history_path.exists() or self._history_path.stat().st_size == 0:
            self._history_path.write_text("run_id,job_id,status,started_at,finished_at,duration_ms,attempt,output_summary\n")

    def record(self, run: JobRun) -> None:
        finished_at = run.finished_at or datetime.now(timezone.utc).isoformat()
        duration_ms = run.duration_ms
        if run.started_at and not run.finished_at:
            try:
                started = datetime.fromisoformat(run.started_at.replace("Z", "+00:00"))
                finished = datetime.fromisoformat(finished_at.replace("Z", "+00:00"))
                duration_ms = int((finished - started).total_seconds() * 1000)
            except Exception:
                pass
        line = f"{run.run_id},{run.job_id},{run.status},{run.started_at},{finished_at},{duration_ms},{run.attempt},{run.output_summary}\n"
        with self._history_path.open("a") as handle:
            handle.write(line)

    def history(self, job_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []
        if not self._history_path.exists():
            return items
        with self._history_path.open() as handle:
            for line in handle.readlines()[1:]:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",", 7)
                if len(parts) < 8:
                    continue
                run_id, item_job_id, status, started_at, finished_at, duration_ms, attempt, output_summary = parts
                if job_id and item_job_id != job_id:
                    continue
                try:
                    duration_ms = int(duration_ms)
                except ValueError:
                    duration_ms = 0
                items.append({
                    "run_id": run_id,
                    "job_id": item_job_id,
                    "status": status,
                    "started_at": started_at,
                    "finished_at": finished_at,
                    "duration_ms": duration_ms,
                    "output_summary": output_summary,
                })
                if len(items) >= limit:
                    break
        return items

    def detect_failure_cluster(self, job_id: str, window: int = 10, threshold: float = 0.7) -> bool:
        recent = [item for item in self.history(limit=window) if item["job_id"] == job_id]
        if not recent:
            return False
        failures = sum(1 for item in recent if item["status"] != "SUCCESS")
        return failures / len(recent) >= threshold


def _job_to_dict(job: JobDefinition) -> Dict[str, Any]:
    return {
        "id": job.id,
        "name": job.name,
        "description": job.description,
        "cron": job.cron,
        "harness_action": job.harness_action,
        "retry_policy": job.retry_policy,
        "failure_policy": job.failure_policy,
        "active": job.active,
        "created_at": job.created_at,
    }

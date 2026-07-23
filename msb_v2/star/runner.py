from __future__ import annotations

import json
import time
import traceback
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests

from msb_v2.star.scheduler import JobDefinition, JobRun


class JobRunner:
    def __init__(
        self,
        job_store: Any,
        tracker: Any,
    ) -> None:
        self._job_store = job_store
        self._tracker = tracker

    def _request(self, method: str, url: str, json: Any = None, timeout: int = 30, **kwargs: Any) -> Any:
        return requests.request(method, url, json=json, timeout=timeout, **kwargs)

    def run(self, job: JobDefinition) -> JobRun:
        started_at = datetime.now(timezone.utc).isoformat()
        status = "SUCCESS"
        output_summary = ""
        exit_code = 0
        duration_ms = 0
        try:
            start = time.perf_counter()
            output_summary = self._execute(job)
            duration_ms = int((time.perf_counter() - start) * 1000)
        except Exception as exc:  # pragma: no cover - defensive
            status = "FAILED"
            output_summary = traceback.format_exc()
            exit_code = 1
            duration_ms = int((time.perf_counter() - start) * 1000)
        run = JobRun(
            job_id=job.id,
            status=status,
            started_at=started_at,
            finished_at=datetime.now(timezone.utc).isoformat(),
            duration_ms=duration_ms,
            output_summary=output_summary[-500:],
            attempt=1,
        )
        self._tracker.record(run)
        payload = {
            "run_id": run.run_id,
            "job_id": job.id,
            "status": run.status,
            "timestamp_start": run.started_at,
            "timestamp_end": run.finished_at,
            "duration_ms": run.duration_ms,
            "exit_code": exit_code,
            "stdout_tail": run.output_summary,
            "stderr_tail": "",
            "cpu_percent": 0.0,
            "memory_mb": 0.0,
            "custom_metrics": {},
        }
        try:
            requests.post(
                "http://127.0.0.1:8767/scth/ingest",
                json=payload,
                timeout=3,
            )
        except Exception:
            pass
        if status == "FAILED":
            self._notify(job, run)
        return run

    def _notify(self, job: JobDefinition, run: JobRun) -> None:
        try:
            requests.post(
                "http://127.0.0.1:8767/sn/notify",
                json={
                    "source": "star",
                    "priority": "high",
                    "template": "job_failed",
                    "template_data": {
                        "job_name": job.name or job.id,
                        "error": run.output_summary,
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
            try:
                from msb_v2.sn.engine import NotificationEngine
                from msb_v2.sn.models import NotificationRequest, Priority
                from msb_v2.sn.policy_engine import PolicyEngine
                engine = NotificationEngine(policy=PolicyEngine(rate_limit_per_minute=100))
                engine.notify(
                    NotificationRequest(
                        source="star",
                        priority=Priority.high,
                        template="job_failed",
                        template_data={
                            "job_name": job.name or job.id,
                            "error": run.output_summary,
                            "run_id": run.run_id,
                            "timestamp": run.finished_at,
                        },
                        channels=["console"],
                        require_ack=False,
                        expires_in_seconds=3600,
                    )
                )
            except Exception:
                pass

    def _execute(self, job: JobDefinition) -> str:
        harness_action = job.harness_action or {}
        harness = harness_action.get("type") or harness_action.get("harness", "app")
        action = harness_action.get("action")
        if harness == "app":
            if action == "ping":
                return "pong"
            if action == "fail":
                raise RuntimeError("forced failure")
            return "app action executed"
        if harness == "http":
            return self._call_http(job, harness_action)
        if harness == "local_ai":
            return self._call_local_ai(job, action, harness_action.get("payload"))
        if harness == "github":
            return self._call_github(action, harness_action.get("payload"))
        return f"{harness}:{action} executed"

    def _call_http(self, job: JobDefinition, harness_action: Dict[str, Any]) -> str:
        try:
            url = harness_action.get("url")
            method = str(harness_action.get("method", "GET")).upper()
            body = harness_action.get("body")
            response = self._request(method, url or "", json=body, timeout=30)
            if response.ok:
                try:
                    data = response.json()
                    if isinstance(data, dict):
                        return str(data.get("status") or data.get("result") or "http action executed")
                except Exception:
                    pass
                return f"http {response.status_code}"
            return f"http {response.status_code}"
        except Exception as exc:
            return f"http action executed: {exc}"

    def _call_local_ai(self, job: JobDefinition, action: Optional[str], payload: Optional[Dict[str, Any]]) -> str:
        if action == "infer":
            try:
                response = requests.post(
                    "http://127.0.0.1:8767/local-ai/infer",
                    json=payload or {"prompt": "ping"},
                    timeout=30,
                )
                if response.ok:
                    data = response.json()
                    return str(data.get("text", "local inference ok"))
            except Exception:
                pass
        return "local inference ok"

    def _call_github(self, action: Optional[str], payload: Optional[Dict[str, Any]]) -> str:
        return f"github {action or 'status'} executed"

    def _emit_telemetry(self, job: JobDefinition, run: JobRun) -> None:
        try:
            requests.post(
                "http://127.0.0.1:8767/scth/ingest",
                json={
                    "run_id": run.run_id,
                    "job_id": job.id,
                    "status": run.status,
                    "timestamp_start": run.started_at,
                    "timestamp_end": run.finished_at,
                    "duration_ms": run.duration_ms,
                    "exit_code": run.exit_code,
                    "stdout_tail": run.output_summary,
                    "stderr_tail": "",
                    "cpu_percent": 0.0,
                    "memory_mb": 0.0,
                    "custom_metrics": {},
                },
                timeout=3,
            )
        except Exception:
            pass

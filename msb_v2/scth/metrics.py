from __future__ import annotations

from typing import Any, Dict

from prometheus_client import Counter, Gauge, Histogram

JOB_RUNS_TOTAL = Counter(
    "msb_cron_jobs_total",
    "Count of job runs by outcome.",
    ["job_id", "status"],
)
JOB_DURATION_SECONDS = Histogram(
    "msb_cron_job_duration_seconds",
    "Histogram of job duration in seconds.",
    ["job_id"],
)
JOB_LAST_SUCCESS_TIMESTAMP = Gauge(
    "msb_cron_job_last_success_timestamp",
    "Unix timestamp of last successful run per job.",
    ["job_id"],
)
JOB_CONSECUTIVE_FAILURES = Gauge(
    "msb_cron_job_consecutive_failures",
    "Consecutive failure count per job.",
    ["job_id"],
)
INGESTION_ERRORS_TOTAL = Counter(
    "msb_cron_telemetry_ingestion_errors_total",
    "Total telemetry ingestion errors.",
)


def record_run(event: Dict[str, Any]) -> None:
    job_id = str(event.get("job_id", ""))
    status = str(event.get("status", ""))
    duration_ms = event.get("duration_ms") or 0
    JOB_RUNS_TOTAL.labels(job_id=job_id, status=status).inc()
    if duration_ms:
        JOB_DURATION_SECONDS.labels(job_id=job_id).observe(duration_ms / 1000.0)
    if status == "SUCCESS":
        JOB_LAST_SUCCESS_TIMESTAMP.labels(job_id=job_id).set_to_current_time()
    if status == "FAILED":
        current = JOB_CONSECUTIVE_FAILURES.labels(job_id=job_id)
        current.inc()
    else:
        JOB_CONSECUTIVE_FAILURES.labels(job_id=job_id).set(0)


def bump_ingestion_error() -> None:
    INGESTION_ERRORS_TOTAL.inc()

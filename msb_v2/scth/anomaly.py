from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class Anomaly:
    anomaly_id: str
    job_id: str
    detected_at: str
    kind: str
    detail: str
    run_id: Optional[str] = None


class AnomalyDetector:
    def __init__(self, z_score_window: int = 20, z_score_threshold: float = 2.0) -> None:
        self._z_score_window = z_score_window
        self._z_score_threshold = z_score_threshold

    def detect(self, runs: List[Dict[str, Any]]) -> List[Anomaly]:
        anomalies: List[Anomaly] = []
        by_job: Dict[str, List[Dict[str, Any]]] = {}
        for run in runs:
            by_job.setdefault(str(run.get("job_id", "")), []).append(run)
        for job_id, job_runs in by_job.items():
            self._check_duration_spikes(anomalies, job_id, job_runs)
            self._check_failure_clusters(anomalies, job_id, job_runs)
            self._check_resource_creep(anomalies, job_id, job_runs)
        return anomalies

    def _check_duration_spikes(self, anomalies: List[Anomaly], job_id: str, runs: List[Dict[str, Any]]) -> None:
        recent = sorted(runs, key=lambda item: item.get("ingestion_ts", ""))[-self._z_score_window :]
        if not recent:
            return
        durations = [float(run.get("duration_ms") or 0) / 1000.0 for run in recent]
        mean = sum(durations) / len(durations)
        variance = sum((x - mean) ** 2 for x in durations) / len(durations)
        std = math.sqrt(variance) if variance else 0.0
        latest = durations[-1]
        run = recent[-1]
        if std and (latest - mean) / std > self._z_score_threshold:
            anomalies.append(
                Anomaly(
                    anomaly_id=f"duration-{job_id}-{run.get('run_id')}-{int(datetime.now(timezone.utc).timestamp())}",
                    job_id=job_id,
                    detected_at=datetime.now(timezone.utc).isoformat(),
                    kind="duration_spike",
                    detail=f"duration {latest:.2f}s outside {self._z_score_threshold} std dev from mean {mean:.2f}s",
                    run_id=run.get("run_id"),
                )
            )

    def _check_failure_clusters(self, anomalies: List[Anomaly], job_id: str, runs: List[Dict[str, Any]]) -> None:
        recent = sorted(runs, key=lambda item: item.get("ingestion_ts", ""))[-self._z_score_window :]
        if not recent:
            return
        failures = sum(1 for run in recent if str(run.get("status")) == "FAILED")
        ratio = failures / len(recent)
        if ratio >= 0.5:
            latest = recent[-1]
            anomalies.append(
                Anomaly(
                    anomaly_id=f"failures-{job_id}-{latest.get('run_id')}-{int(datetime.now(timezone.utc).timestamp())}",
                    job_id=job_id,
                    detected_at=datetime.now(timezone.utc).isoformat(),
                    kind="failure_cluster",
                    detail=f"{failures}/{len(recent)} recent runs failed (ratio {ratio:.2f})",
                    run_id=latest.get("run_id"),
                )
            )

    def _check_resource_creep(self, anomalies: List[Anomaly], job_id: str, runs: List[Dict[str, Any]]) -> None:
        recent = [run for run in runs if run.get("memory_mb") is not None]
        if len(recent) < 5:
            return
        mems = [float(run.get("memory_mb") or 0.0) for run in recent]
        first = sum(mems[:3]) / 3
        last = sum(mems[-3:]) / 3
        if first and last / first > 3:
            latest = recent[-1]
            anomalies.append(
                Anomaly(
                    anomaly_id=f"memory-creep-{job_id}-{latest.get('run_id')}-{int(datetime.now(timezone.utc).timestamp())}",
                    job_id=job_id,
                    detected_at=datetime.now(timezone.utc).isoformat(),
                    kind="memory_creep",
                    detail=f"memory increased from {first:.1f} MB to {last:.1f} MB",
                    run_id=latest.get("run_id"),
                )
            )

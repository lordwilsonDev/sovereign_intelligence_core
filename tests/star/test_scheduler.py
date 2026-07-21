from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pytest

from msb_v2.star.scheduler import JobDefinition, JobStore, Tracker
from msb_v2.star.runner import JobRunner
from msb_v2.star.manager import StarManager


@pytest.fixture()
def tmp_jobs_path(tmp_path: Path) -> Path:
    return tmp_path / "jobs.json"


@pytest.fixture()
def job_store(tmp_jobs_path: Path) -> JobStore:
    return JobStore(jobs_path=tmp_jobs_path)


@pytest.fixture()
def manager(job_store: JobStore) -> StarManager:
    tracker = Tracker(history_path=job_store._jobs_path.parent / "job_history.jsonl")
    runner = JobRunner(job_store, tracker)
    return StarManager(job_store, tracker, runner)


def test_create_and_list_jobs(manager: StarManager) -> None:
    manager.create_job({"name": "sqa", "cron": "*/15 * * * *", "harness_action": {"harness": "sqa", "action": "run_all"}})
    jobs = manager.list_jobs()
    assert [job["name"] for job in jobs["jobs"]] == ["sqa"]


def test_delete_job(manager: StarManager) -> None:
    created = manager.create_job({"name": "build", "cron": "0 * * * *", "harness_action": {"harness": "github", "action": "status"}})
    job_id = created["id"]
    response = manager.delete_job(job_id)
    assert response["id"] == job_id


def test_runner_records_history(job_store: JobStore, tmp_path: Path) -> None:
    tracker = Tracker(history_path=tmp_path / "history.jsonl")
    runner = JobRunner(job_store, tracker)
    job = JobDefinition(name="heartbeat", cron="* * * * *", harness_action={"harness": "app", "action": "ping"})
    run = runner.run(job)
    assert run.status == "SUCCESS"
    assert len(tracker.history(limit=10)) == 1


def test_failure_cluster_detection(tmp_path: Path) -> None:
    tracker = Tracker(history_path=tmp_path / "history.jsonl")
    tracker.history = lambda limit=50: [  # type: ignore[method-assign]
        {"job_id": "j1", "status": "FAILED"},
        {"job_id": "j1", "status": "FAILED"},
        {"job_id": "j1", "status": "SUCCESS"},
    ]
    assert tracker.detect_failure_cluster("j1", window=3, threshold=0.5) is True
    assert tracker.detect_failure_cluster("j1", window=3, threshold=0.9) is False


def test_failure_cluster_disables_job(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    store = JobStore(jobs_path=tmp_path / "jobs.json")
    tracker = Tracker(history_path=tmp_path / "history.jsonl")
    captured: Dict[str, Any] = {}

    def fake_post(url: str, json: Dict[str, Any], timeout: int) -> None:
        captured["url"] = url
        captured["json"] = json

    monkeypatch.setattr("requests.post", fake_post)
    runner = JobRunner(store, tracker)
    manager = StarManager(store, tracker, runner)
    created = manager.create_job({
        "name": "flaky",
        "cron": "*/15 * * * *",
        "harness_action": {"harness": "app", "action": "fail"},
        "retry_policy": {"max_retries": 0, "backoff_factor": 1.0},
        "failure_policy": "alert",
        "active": True,
    })
    for _ in range(3):
        manager.run_job(created["id"])
    assert store.get_job(created["id"])["active"] is False
    assert captured["url"].endswith("/sn/notify")
    assert captured["json"]["priority"] == "critical"

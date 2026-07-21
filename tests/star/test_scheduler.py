from __future__ import annotations

import tempfile
import pathlib
from typing import Any, Dict

import pytest

from msb_v2.star.scheduler import JobStore, Tracker
from msb_v2.star.runner import JobRunner
from msb_v2.star.manager import StarManager


def test_failure_cluster_disables_job(monkeypatch: pytest.MonkeyPatch) -> None:
    tmp = pathlib.Path(tempfile.mkdtemp())
    store = JobStore(jobs_path=tmp / "jobs.json")
    tracker = Tracker(history_path=tmp / "history.jsonl")
    captured: Dict[str, Any] = {}

    def fake_post(url: str, json: Dict[str, Any], timeout: int) -> None:
        captured["url"] = url
        captured["json"] = json

    monkeypatch.setattr("requests.post", fake_post)
    runner = JobRunner(store, tracker)
    manager = StarManager(store, tracker, runner)
    created = manager.create_job({
        "name": "flaky",
        "cron": "0/15 * * * *",
        "harness_action": {"harness": "app", "action": "fail"},
        "retry_policy": {"max_retries": 0, "backoff_factor": 1.0},
        "failure_policy": "alert",
        "active": True,
    })
    job_id = created["id"]
    for _ in range(3):
        manager.run_job(job_id)
    assert store.get_job(job_id)["active"] is False
    assert captured["url"].endswith("/sn/notify")
    assert captured["json"]["priority"] == "critical"

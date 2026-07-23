"""Tests for the sovereign research assistant STAR DAG structure and loadability."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pytest

from msb_v2.star.runner import JobRunner
from msb_v2.star.scheduler import JobDefinition, JobStore, Tracker


_WORKFLOW_ROOT = Path("msb_v2/star/workflows")
_DAILY = _WORKFLOW_ROOT / "sovereign_research_daily.json"
_WEEKLY = _WORKFLOW_ROOT / "sovereign_research_weekly.json"
_MONTHLY = _WORKFLOW_ROOT / "sovereign_research_monthly.json"

_REQUIRED_FILES = (_DAILY, _WEEKLY, _MONTHLY)
_REQUIRED_KEYS = ("id", "name", "cron", "harness_action", "retry_policy", "failure_policy", "active")


def _load_workflow(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_research_workflow_files_exist() -> None:
    for path in _REQUIRED_FILES:
        assert path.exists(), f"missing workflow file: {path}"


def test_research_workflow_schema() -> None:
    for path in _REQUIRED_FILES:
        data = _load_workflow(path)
        for key in _REQUIRED_KEYS:
            assert key in data, f"{path.name}: missing key: {key}"
        assert data["failure_policy"]["alert_template"] == "research_assistant_failure"


def test_research_dag_dependency_topology() -> None:
    daily = _load_workflow(_DAILY)
    weekly = _load_workflow(_WEEKLY)
    monthly = _load_workflow(_MONTHLY)
    assert daily["id"] == "sovereign-research-daily"
    assert weekly["id"] == "sovereign-research-weekly"
    assert monthly["id"] == "sovereign-research-monthly"
    assert daily["harness_action"]["body"]["phase"] == "literature_scan"
    assert weekly["harness_action"]["body"]["phase"] == "hypothesis_generation"
    assert monthly["harness_action"]["body"]["phase"] == "report_synthesis"


def test_research_dag_loadable_as_job_definitions() -> None:
    jobs = [JobDefinition(**_load_workflow(path)) for path in _REQUIRED_FILES]
    ids = [job.id for job in jobs]
    assert ids == ["sovereign-research-daily", "sovereign-research-weekly", "sovereign-research-monthly"]
    for job in jobs:
        assert job.active is True
        assert job.cron in {"0 8 * * *", "0 9 * * 1", "0 10 1 * *"}


def test_research_job_store_persists_and_lists(tmp_path: Path) -> None:
    jobs_path = tmp_path / "jobs.json"
    store = JobStore(jobs_path=jobs_path, workflows_path=tmp_path)
    jobs = [JobDefinition(**_load_workflow(path)) for path in _REQUIRED_FILES]
    for job in jobs:
        existing = next((item for item in store.list_jobs() if item.get("name") == job.name), None)
        if not existing:
            store.create_job({
                "id": job.id,
                "name": job.name,
                "cron": job.cron,
                "harness_action": job.harness_action,
                "retry_policy": job.retry_policy,
                "failure_policy": job.failure_policy,
                "active": job.active,
                "depends_on": job.depends_on,
            })
    listed = {item["id"]: item for item in store.list_jobs()}
    for job in jobs:
        assert job.id in listed
        assert listed[job.id]["cron"] == job.cron


def test_research_runner_http_execution_with_mocked_request(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeResponse:
        status_code = 200
        ok = True

        def json(self) -> Dict[str, Any]:
            return {"status": "ok"}

    captured: Dict[str, Any] = {}

    def fake_request(method: str, url: str, json: Any = None, timeout: int = 30, **kwargs: Any) -> FakeResponse:
        captured["method"] = method
        captured["url"] = url
        captured["json"] = json
        return FakeResponse()

    monkeypatch.setattr("msb_v2.star.runner.requests.request", fake_request, raising=False)
    runner = JobRunner(JobStore(), Tracker())
    job = JobDefinition(**_load_workflow(_DAILY))
    output = runner._execute(job)
    assert captured["method"] == "POST"
    assert captured["url"] == "http://127.0.0.1:8766/research/assistant/run"
    assert captured["json"] == {"phase": "literature_scan"}
    assert output == "ok"

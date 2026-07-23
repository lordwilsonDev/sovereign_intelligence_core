"""Verify the research assistant STAR job DAG."""
from __future__ import annotations

import json
from pathlib import Path

import pytest


_JOBS = [
    "msb_v2/star/workflows/sovereign_research_daily.json",
    "msb_v2/star/workflows/sovereign_research_weekly.json",
    "msb_v2/star/workflows/sovereign_research_monthly.json",
]


def _load(job_file: str) -> dict:
    return json.loads(Path(job_file).read_text(encoding="utf-8"))


def test_daily_job_exists() -> None:
    path = Path(_JOBS[0])
    assert path.exists()
    job = _load(_JOBS[0])
    assert job["id"] == "sovereign-research-daily"
    assert job["active"] is True
    assert job["depends_on"] == []


def test_weekly_job_depends_on_daily() -> None:
    job = _load(_JOBS[1])
    assert "sovereign-research-daily" in job["depends_on"]


def test_monthly_job_depends_on_weekly() -> None:
    job = _load(_JOBS[2])
    assert "sovereign-research-weekly" in job["depends_on"]


def test_all_phases_covered() -> None:
    phases = set()
    for job_file in _JOBS:
        job = _load(job_file)
        phases.add(job["harness_action"]["body"]["phase"])
    assert "literature_scan" in phases
    assert "hypothesis_generation" in phases
    assert "report_synthesis" in phases

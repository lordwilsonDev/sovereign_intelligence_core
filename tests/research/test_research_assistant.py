from __future__ import annotations

import json
from pathlib import Path

import pytest


def test_research_workflow_files_exist(tmp_path: Path) -> None:
    workflow_root = Path("msb_v2/star/workflows")
    assert (workflow_root / "sovereign_research_daily.json").exists()
    assert (workflow_root / "sovereign_research_weekly.json").exists()
    assert (workflow_root / "sovereign_research_monthly.json").exists()
    for name in ["sovereign_research_daily.json", "sovereign_research_weekly.json", "sovereign_research_monthly.json"]:
        data = json.loads((workflow_root / name).read_text(encoding="utf-8"))
        assert "id" in data
        assert "cron" in data
        assert "harness_action" in data
        assert data["failure_policy"]["alert_template"] == "research_assistant_failure"


def test_research_dag_pipeline_phases() -> None:
    phases = [
        ("sovereign-research-daily", "literature_scan", "0 8 * * *"),
        ("sovereign-research-weekly", "hypothesis_generation", "0 9 * * 1"),
        ("sovereign-research-monthly", "report_synthesis", "0 10 1 * *"),
    ]
    summary = {
        "ids": [item[0] for item in phases],
        "phases": [item[1] for item in phases],
    }
    assert summary["ids"] == ["sovereign-research-daily", "sovereign-research-weekly", "sovereign-research-monthly"]
    assert summary["phases"] == ["literature_scan", "hypothesis_generation", "report_synthesis"]

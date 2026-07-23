from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pytest

from msb_v2.research.assistant import SovereignResearchAssistant


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


def test_full_pipeline_with_sac_block(monkeypatch: pytest.MonkeyPatch) -> None:
    assistant = SovereignResearchAssistant("immune test")

    def mock_sac_low(*_args: Any, **_kwargs: Any) -> bool:
        return False
    monkeypatch.setattr(assistant, "_sac_gate", mock_sac_low)

    result = assistant.run_full_pipeline()
    assert result["status"] == "blocked_by_sac"


def test_full_pipeline_with_echo_block(monkeypatch: pytest.MonkeyPatch) -> None:
    assistant = SovereignResearchAssistant("immune test")

    monkeypatch.setattr(assistant, "_sac_gate", lambda *_: True)
    monkeypatch.setattr(assistant, "_echo_gate", lambda *_args, **_kwargs: False)

    result = assistant.run_full_pipeline()
    assert result["status"] == "awaiting_confirmation"


def test_health_check_included_in_result(monkeypatch: pytest.MonkeyPatch) -> None:
    assistant = SovereignResearchAssistant("immune test")

    monkeypatch.setattr(assistant, "_sac_gate", lambda *_: True)
    monkeypatch.setattr(assistant, "_echo_gate", lambda *_args, **_kwargs: True)
    monkeypatch.setattr(assistant, "_health_check", lambda: {"schh": "GREEN", "sshh": "healthy"})

    result = assistant.run_full_pipeline()
    assert result["status"] == "completed"
    assert result["health"]["schh"] == "GREEN"
    assert result["health"]["sshh"] == "healthy"

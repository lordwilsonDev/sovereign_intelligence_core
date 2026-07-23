"""Tests for the sovereign research assistant MVP."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from msb_v2.research.assistant import SovereignResearchAssistant


def _assistant(tmp_root: Path, topic: str = "sovereign-local-llm-economics") -> SovereignResearchAssistant:
    return SovereignResearchAssistant(topic=topic, root=tmp_root / "workspace")


def test_run_inversion_returns_uim_and_state(tmp_path: Path) -> None:
    assistant = _assistant(tmp_path)
    uim = assistant.run_inversion()
    assert uim["topic"] == "sovereign-local-llm-economics"
    assert assistant.state["phase"] == "inverted"
    assert "hypotheses" in assistant.state
    assert len(assistant.state["hypotheses"]) >= 1
    assert (assistant.root / f"{assistant.slug}_UIM.json").exists()


def test_ground_evidence_populates_ledger(tmp_path: Path) -> None:
    assistant = _assistant(tmp_path)
    assistant.run_inversion()
    ledger = assistant.ground_evidence()
    assert ledger["local_source_count"] >= 1
    assert "evidence" in ledger
    assert "claims" in ledger
    assert assistant.state["phase"] == "evidence_grounded"
    assert (assistant.root / f"{assistant.slug}_evidence_ledger.json").exists()


def test_draft_report_creates_markdown(tmp_path: Path) -> None:
    assistant = _assistant(tmp_path)
    assistant.run_inversion()
    assistant.ground_evidence()
    path = assistant.draft_report()
    assert path.suffix == ".md"
    assert path.exists()
    assert "Sovereign Research Report" in path.read_text(encoding="utf-8")


def test_record_completion_persists_summary(tmp_path: Path) -> None:
    assistant = _assistant(tmp_path)
    assistant.run_inversion()
    assistant.ground_evidence()
    assistant.draft_report()
    completion = assistant.record_completion()
    assert completion["slug"] == assistant.slug
    assert completion["claims_total"] == len(assistant.state["claims"])
    assert (assistant.root / f"{assistant.slug}_completion.json").exists()


def test_guard_event_created_and_saved(tmp_path: Path) -> None:
    assistant = _assistant(tmp_path)
    assistant.run_inversion()
    assert len(assistant.guard_events) == 1
    assert assistant.guard_events[0]["phase"] == "inversion"


def test_run_full_pipeline_completes_locally(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import sys
    import types

    class _Resp:
        status_code = 200
        def json(self) -> Any:
            return {"available": True, "peers": [], "submitted_tasks": []}

    fake = types.ModuleType("requests")
    fake.post = lambda *args, **kwargs: _Resp()  # type: ignore[misc]
    fake.get = lambda *args, **kwargs: _Resp()  # type: ignore[misc]
    monkeypatch.setitem(sys.modules, "requests", fake)

    assistant = _assistant(tmp_path)
    summary = assistant.run_full_pipeline()
    assert summary["topic"] == "sovereign-local-llm-economics"
    assert len(summary["phases"]) == 3
    assert "evolution" in summary
    assert "mesh" in summary
    assert "continuity" in summary
    assert "memory" in summary

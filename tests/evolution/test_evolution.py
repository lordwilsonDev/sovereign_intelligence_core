"""Autonomous Evolution tests."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from msb_v2.evolution.proposal_engine import ProposalEngine
from msb_v2.evolution.shadow_buffer import ShadowBuffer
from msb_v2.evolution.autonomous_evolution import AutonomousEvolution


@pytest.fixture()
def proposal_engine(tmp_path: Path):
    repo_file = tmp_path / "hot.py"
    repo_file.write_text(
        "def long():\n"
        "    a = 1\n"
        "    b = 2\n"
        "    c = 3\n"
        "    d = 4\n"
        "    e = 5\n"
        "    f = 6\n"
        "    g = 7\n"
        "    h = 8\n"
        "    i = 9\n"
        "    pass\n"
    )
    return ProposalEngine(repo_path=tmp_path)


def test_generate_proposal_returns_structured_document(proposal_engine: ProposalEngine) -> None:
    hotspot = {"file": "hot.py", "function": "long", "complexity": 20}
    proposal = proposal_engine.generate(hotspot)
    assert proposal is not None
    assert proposal["file"] == "hot.py"
    assert proposal["function"] == "long"
    assert proposal["risk"] == "MEDIUM"
    assert proposal["id"]
    assert "changes" in proposal


def test_summarize_proposal(proposal_engine: ProposalEngine) -> None:
    proposal = {"id": "x", "file": "a", "function": "b", "complexity_before": 20, "technique": "extract_helper", "risk": "LOW", "changes": [{}]}
    summary = proposal_engine.summarize(proposal)
    assert summary["risk"] == "LOW"
    assert summary["file"] == "a"
    assert summary["changes"] == 1


def test_shadow_buffer_runs_tests(tmp_path: Path) -> None:
    shadow = ShadowBuffer(repo_path=tmp_path)
    proposal = {"id": "x", "changes": []}
    result = shadow.test_proposal(proposal)
    assert "passed" in result
    assert "proposal_id" in result


def test_generate_returns_none_for_low_complexity(proposal_engine: ProposalEngine) -> None:
    hotspot = {"file": "hot.py", "function": "short", "complexity": 3}
    proposal = proposal_engine.generate(hotspot)
    assert proposal is None


def test_autonomous_evolution_run_cycle_handles_scan_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    engine = AutonomousEvolution()
    import msb_v2.evolution.autonomous_evolution as ae
    monkeypatch.setattr(ae, "requests", type("R", (), {"post": lambda *a, **k: (_ for _ in ()).throw(Exception("down"))})())
    with patch("msb_v2.evolution.autonomous_evolution.emit_thought"):
        result = engine.run_cycle()
    assert result["status"] == "scan_failed"

"""Dream Mode tests."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from msb_v2.dream_mode.engine import DreamMode


@pytest.fixture()
def dream_engine(tmp_path: Path):
    dreams_path = tmp_path / "dreams.jsonl"
    with patch("msb_v2.dream_mode.engine.DreamMode._store"):
        engine = DreamMode(dreams_path=dreams_path)
    return engine


def test_run_dream_cycle_returns_outcome(dream_engine: DreamMode) -> None:
    result = dream_engine.run_dream_cycle()
    assert result["scenario_id"]
    assert result["outcome"]["survival_score"] >= 70
    assert result["outcome"]["recommended_action"] in ("maintain", "monitor", "adapt", "quarantine")


def test_recent_dreams_empty_when_no_history(dream_engine: DreamMode, tmp_path: Path) -> None:
    recent = dream_engine.recent()
    assert recent == []

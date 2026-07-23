"""Encrypted local snapshot backup tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from msb_v2.snapshot.engine import SnapshotEngine


def test_list_snapshots_empty_when_no_backups(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    empty = tmp_path / "empty"
    empty.mkdir(parents=True, exist_ok=True)
    engine = SnapshotEngine(repo_path=tmp_path)
    monkeypatch.setattr(engine, "backup_dir", empty)
    assert engine.list_snapshots() == []


def test_capture_returns_envelope(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    engine = SnapshotEngine(repo_path=tmp_path)
    monkeypatch.setattr(engine, "backup_dir", tmp_path / "backups")
    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data" / "evolution_memory.jsonl").write_text("{}", encoding="utf-8")
    result = engine.capture()
    assert result["status"] == "captured"
    assert result["snapshot_id"]
    assert result["path"].endswith(".zip")
    assert Path(result["path"]).exists()

"""Encrypted local snapshot backup engine."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import pyzipper

from msb_v2.snapshot.engine import SnapshotEngine


def test_snapshot_engine_list_empty_when_no_backups(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    engine = SnapshotEngine(repo_path=tmp_path)
    monkeypatch.setattr(engine, "backup_dir", tmp_path / "empty")
    assert engine.list_snapshots() == []


def test_snapshot_capture_returns_envelope(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    engine = SnapshotEngine(repo_path=tmp_path)
    monkeypatch.setattr(engine, "backup_dir", tmp_path / "backups")
    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data" / "evolution_memory.jsonl").write_text("{}", encoding="utf-8")
    result = engine.capture()
    assert result["status"] == "captured"
    assert result["snapshot_id"]
    assert result["path"].endswith(".zip")

from __future__ import annotations

import os

import pytest

from msb_v2.core.snapshots import SnapshotManager


def test_snapshot_rollback_preserves_and_replaces(tmp_path: str) -> None:
    root = tmp_path
    src = os.path.join(root, "src")
    os.makedirs(src, exist_ok=True)
    with open(os.path.join(src, "file.txt"), "w", encoding="utf-8") as f:
        f.write("hello")

    dest = os.path.join(root, "dest")
    os.makedirs(dest, exist_ok=True)
    with open(os.path.join(dest, "other.txt"), "w", encoding="utf-8") as f:
        f.write("old")

    mgr = SnapshotManager(os.path.join(root, "snapshots"))
    mgr.snapshot("v1", src)
    mgr.rollback("v1", dest)

    assert os.path.exists(os.path.join(dest, "file.txt"))
    assert open(os.path.join(dest, "file.txt"), encoding="utf-8").read() == "hello"
    assert not os.path.exists(os.path.join(dest, "other.txt"))


def test_snapshot_rollback_missing_tag_raises(tmp_path: str) -> None:
    mgr = SnapshotManager(os.path.join(tmp_path, "snapshots"))
    with pytest.raises(FileNotFoundError):
        mgr.rollback("missing", os.path.join(tmp_path, "out"))


def test_snapshot_source_equals_root_raises(tmp_path: str) -> None:
    root = os.path.join(tmp_path, "snapshots")
    os.makedirs(root, exist_ok=True)
    mgr = SnapshotManager(root)
    with pytest.raises(ValueError):
        mgr.snapshot("v1", root)


def test_snapshot_missing_source_raises(tmp_path: str) -> None:
    mgr = SnapshotManager(os.path.join(tmp_path, "snapshots"))
    with pytest.raises(FileNotFoundError):
        mgr.snapshot("v1", os.path.join(tmp_path, "nope"))


def test_snapshot_list_empty(tmp_path: str) -> None:
    mgr = SnapshotManager(os.path.join(tmp_path, "snapshots"))
    assert mgr.list_snapshots("v1") == []

from __future__ import annotations

import os

import pytest

from msb_v2.core.snapshots import SnapshotManager


def test_snapshot_byte_for_byte_rollback_after_break(tmp_path: str) -> None:
    root = tmp_path
    src = os.path.join(root, "src")
    os.makedirs(src, exist_ok=True)
    original = "alpha\nbeta\n"
    with open(os.path.join(src, "data.txt"), "w", encoding="utf-8") as f:
        f.write(original)

    mgr = SnapshotManager(os.path.join(root, "snapshots"))
    mgr.snapshot("v1", src)

    with open(os.path.join(src, "data.txt"), "w", encoding="utf-8") as f:
        f.write("CORRUPTED")

    dest = os.path.join(root, "restored")
    mgr.rollback("v1", dest)

    restored_path = os.path.join(dest, "data.txt")
    assert os.path.exists(restored_path)
    with open(restored_path, "rb") as f:
        assert f.read() == original.encode("utf-8")


def test_snapshot_file_mode_preserved(tmp_path: str) -> None:
    root = tmp_path
    src = os.path.join(root, "src")
    os.makedirs(src, exist_ok=True)
    target = os.path.join(src, "mode.txt")
    with open(target, "w", encoding="utf-8") as f:
        f.write("x")
    os.chmod(target, 0o600)

    mgr = SnapshotManager(os.path.join(root, "snapshots"))
    mgr.snapshot("v1", src)

    dest = os.path.join(root, "dest")
    os.makedirs(dest, exist_ok=True)
    mgr.rollback("v1", dest)
    assert oct(os.stat(os.path.join(dest, "mode.txt")).st_mode & 0o777) == "0o600"

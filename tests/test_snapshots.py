from __future__ import annotations

import os

from msb_v2.core.snapshots import SnapshotManager


def test_snapshot_and_rollback(tmp_path: str) -> None:
    root = tmp_path
    src = os.path.join(root, "src")
    os.makedirs(src, exist_ok=True)
    with open(os.path.join(src, "file.txt"), "w", encoding="utf-8") as f:
        f.write("hello")
    dest = os.path.join(root, "dest")
    mgr = SnapshotManager(os.path.join(root, "snapshots"))
    mgr.snapshot("v1", src)
    listings = mgr.list_snapshots("v1")
    assert len(listings) == 1
    mgr.rollback("v1", dest)
    assert os.path.exists(os.path.join(dest, "file.txt"))
    assert open(os.path.join(dest, "file.txt"), encoding="utf-8").read() == "hello"

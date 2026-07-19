from __future__ import annotations

import contextlib
import os

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.api.middleware import set_local_bypass as _set_local_bypass

client = TestClient(create_app())


def _make_temp_dir(tmpdir: str) -> str:
    d = os.path.join(tmpdir, "snap_src")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "seed.txt"), "w", encoding="utf-8") as f:
        f.write("seed")
    return d


@contextlib.contextmanager
def _bypass():
    _set_local_bypass(True)
    try:
        yield
    finally:
        _set_local_bypass(None)


def test_runtime_snapshot_create_and_list(tmp_path: str) -> None:
    src = _make_temp_dir(tmp_path)
    with _bypass():
        r = client.post("/runtime/snapshots", json={"tag": "v1", "source": src})
    assert r.status_code == 200
    r = client.get("/runtime/snapshots?tag=v1")
    assert r.status_code == 200
    body = r.json()
    assert body["tag"] == "v1"
    assert len(body["snapshots"]) >= 1


def test_runtime_snapshot_rollback(tmp_path: str) -> None:
    src = _make_temp_dir(tmp_path)
    with _bypass():
        client.post("/runtime/snapshots", json={"tag": "v2", "source": src})
        dest = os.path.join(tmp_path, "snap_dest_v2")
        r = client.post("/runtime/snapshots/rollback", json={"tag": "v2", "dest": dest})
    assert r.status_code == 200
    assert os.path.exists(dest)
    assert os.path.exists(os.path.join(dest, "seed.txt"))

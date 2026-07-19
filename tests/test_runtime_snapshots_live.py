from __future__ import annotations

import contextlib
import os

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.api.middleware import set_local_bypass as _set_local_bypass

client = TestClient(create_app())


@contextlib.contextmanager
def _bypass():
    _set_local_bypass(True)
    try:
        yield
    finally:
        _set_local_bypass(None)


def test_runtime_snapshots_live_flow(tmp_path: str) -> None:
    src = os.path.join(os.path.dirname(__file__), "..", "docs")
    src = os.path.abspath(src)

    with _bypass():
        r = client.post("/runtime/snapshots", json={"tag": "live-v1", "source": src})
    assert r.status_code == 200, r.text
    assert r.json()["tag"] == "live-v1"

    r = client.get("/runtime/snapshots?tag=live-v1")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["tag"] == "live-v1"
    assert len(body["snapshots"]) >= 1

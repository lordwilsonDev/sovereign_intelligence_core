from __future__ import annotations

from msb_v2.api.web import create_app
from starlette.testclient import TestClient


def test_governor_status_lists_registered_harnesses() -> None:
    client = TestClient(create_app())
    r = client.get("/governor/governor/status")
    assert r.status_code == 200
    data = r.json()
    assert "harness_count" in data
    assert "harnesses" in data

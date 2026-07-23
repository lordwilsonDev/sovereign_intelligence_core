"""Snapshot API smoke tests."""
from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


def test_snapshot_routes_mount_under_snapshot() -> None:
    client = TestClient(create_app())
    assert client.post("/snapshot/capture").status_code != 404
    assert client.get("/snapshot/list").status_code != 404


def test_truth_beat_routes_mount_under_truth_beat() -> None:
    client = TestClient(create_app())
    assert client.get("/truth-beat/pulse").status_code == 200
    assert client.post("/truth-beat/strip", json={"claim": "x"}).status_code == 200

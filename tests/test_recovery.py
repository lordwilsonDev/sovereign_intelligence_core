from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_recovery_snapshot_and_rollback() -> None:
    client = TestClient(create_app())
    r = client.post("/recovery/snapshot", json={"key": "r1", "snapshot": {"state": "ok"}})
    assert r.status_code == 200
    assert r.json()["ok"] is True

    r2 = client.get("/recovery/rollback/r1")
    assert r2.status_code == 200
    body = r2.json()
    assert body["ok"] is True
    assert body["snapshot"]["state"] == "ok"

    r3 = client.get("/recovery/rollback/does-not-exist")
    assert r3.status_code == 200
    assert r3.json()["ok"] is False
    assert r3.json()["reason"] == "not_found"

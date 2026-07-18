from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app

client = TestClient(create_app())


def test_live_smoke_v3_twin_full_flow():
    r = client.post("/v3/twin", json={"name": "smoke-twin", "state": {"count": 1}})
    assert r.status_code == 200
    twin_id = r.json()["twin_id"]

    r = client.post(f"/v3/twin/{twin_id}/snapshot")
    assert r.status_code == 200
    snap_id = r.json()["snapshot_id"]

    r = client.post(f"/v3/twin/{twin_id}/evolve", json={"delta": {"count": 2}})
    assert r.status_code == 200

    r = client.get(f"/v3/twin/{snap_id}")
    assert r.status_code == 200
    assert r.json()["state"]["count"] == 1

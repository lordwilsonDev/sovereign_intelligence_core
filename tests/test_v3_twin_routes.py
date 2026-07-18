from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


@pytest.fixture()
def client():
    return TestClient(create_app())


def test_digital_twin_create_snapshot_evolve(client):
    r = client.post("/v3/twin", json={"name": "alpha", "state": {"temperature": 1.0}})
    assert r.status_code == 200
    twin_id = r.json()["twin_id"]

    r = client.post(f"/v3/twin/{twin_id}/snapshot")
    assert r.status_code == 200
    assert "snapshot_id" in r.json()

    r = client.post(f"/v3/twin/{twin_id}/evolve", json={"delta": {"temperature": 0.8}})
    assert r.status_code == 200
    evolved_id = r.json()["twin_id"]

    r = client.get(f"/v3/twin/{evolved_id}")
    assert r.status_code == 200
    assert r.json()["state"]["temperature"] == 0.8


def test_digital_twin_not_found_404(client):
    r = client.get("/v3/twin/does-not-exist")
    assert r.status_code == 404

from __future__ import annotations


from fastapi.testclient import TestClient

from msb_v2.api.main import app

client = TestClient(app)


def test_moie_run_endpoint_returns_contract():
    payload = {"query": "local data custody beats cloud DBs"}
    resp = client.post("/moie/run", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    for key in ["query", "claims_total", "validated", "rejected", "inconclusive", "anomaly_score", "breakthrough_potential", "transcript_hash", "status", "message"]:
        assert key in data


def test_moie_run_transcript_hash_is_deterministic():
    payload = {"query": "deterministic micro-inspections"}
    first = client.post("/moie/run", json=payload).json()["transcript_hash"]
    second = client.post("/moie/run", json=payload).json()["transcript_hash"]
    assert first == second
    assert first.startswith("sha256:")


def test_health_and_subsystems():
    assert client.get("/health").status_code == 200
    assert client.get("/cognitive/ping").status_code == 200
    assert client.get("/runtime/ping").status_code == 200
    assert client.get("/imagination/ping").status_code == 200

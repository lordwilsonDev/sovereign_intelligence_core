from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app

client = TestClient(create_app())


def test_inversion_routes_expose_hypotheses_and_experiments():
    r = client.get("/v3/inversion/hypotheses")
    assert r.status_code == 200
    body = r.json()
    assert "count" in body
    assert "items" in body

    r = client.get("/v3/inversion/experiments")
    assert r.status_code == 200
    body = r.json()
    assert "count" in body
    assert "items" in body


def test_inversion_create_hypothesis_then_experiment():
    r = client.post("/v3/inversion/hypotheses", json={
        "title": "cache warmup reduces latency",
        "description": "Latency drops after cache warmup",
        "assumptions": ["cache is cold", "queries repeat"],
    })
    assert r.status_code == 200
    hypothesis_id = r.json()["hypothesis_id"]
    assert hypothesis_id

    r = client.post("/v3/inversion/experiments", json={
        "hypothesis_id": hypothesis_id,
        "description": "measure P95 before/after warmup",
    })
    assert r.status_code == 200
    experiment_id = r.json()["experiment_id"]
    assert experiment_id


def test_inversion_evidence_round_trip():
    r = client.post("/v3/inversion/hypotheses", json={
        "title": "shorter requests fail less",
        "description": "Brief prompts timeout less often",
        "assumptions": ["timeout scales with length"],
    })
    hypothesis_id = r.json()["hypothesis_id"]

    r = client.post("/v3/inversion/experiments", json={
        "hypothesis_id": hypothesis_id,
        "description": "compare 100 vs 1000 char requests",
    })
    experiment_id = r.json()["experiment_id"]

    r = client.post(f"/v3/inversion/experiments/{experiment_id}/evidence", json={
        "supports": True,
        "score": 0.75,
        "note": "100 char requests had 0% timeout rate",
    })
    assert r.status_code == 200
    assert "evidence_id" in r.json()

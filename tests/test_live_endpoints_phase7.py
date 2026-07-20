from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_live_endpoints_phase7_roundup() -> None:
    client = TestClient(create_app())
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    root = client.get("/")
    assert root.status_code == 200
    assert "msb-studio" in root.text
    html = client.get("/ui/")
    assert html.status_code == 200
    assert "<!DOCTYPE html>" in html.text
    studio = client.get("/studio/status")
    assert studio.status_code == 200
    body = studio.json()
    assert body["runtime"]["ok"] is True
    assert body["memory"]["ok"] is True
    assert body["verification"]["ok"] is True
    assert body["evolution"]["ok"] is True
    assert "agent" in body
    assert "run_endpoint" in body["agent"]

    sovereign = client.get("/sovereign/status")
    assert sovereign.status_code == 200
    assert sovereign.json()["phase"] == "Phase 7"

    environment = client.get("/environment/status")
    assert environment.status_code == 200
    assert environment.json() == sovereign.json()

    demo = client.post("/demo/query", json={"query": "live", "trace_id": "rt-1", "accepted": True})
    assert demo.status_code == 200
    demo_body = demo.json()
    assert demo_body["query"] == "live"
    # local fallback path now includes confidence_assessment
    assert "answer" in demo_body
    assert demo_body.get("confidence_assessment") is not None

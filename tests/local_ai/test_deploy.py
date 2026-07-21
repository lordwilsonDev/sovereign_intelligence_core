from __future__ import annotations

from msb_v2.api.middleware import set_local_bypass
from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


client = TestClient(create_app())


def test_deploy_then_stop_then_list() -> None:
    set_local_bypass(True)
    try:
        deploy = client.post("/local-ai/deploy", json={"model": "qwen2.5:0.5b", "port": 19100})
        assert deploy.status_code == 200
        assert deploy.json().get("status") == "started"

        resp = client.get("/local-ai/deployments")
        assert resp.status_code == 200
        deployments = resp.json().get("deployments", {})
        assert any(dep.get("port") == 19100 for dep in deployments.values())

        stop = client.post("/local-ai/deploy/stop", json={"model": "qwen2.5:0.5b", "port": 19100})
        assert stop.status_code == 200
        assert stop.json().get("status") == "stopped"
    finally:
        set_local_bypass(None)


def test_optimize_endpoint_returns_suggestions() -> None:
    set_local_bypass(True)
    try:
        resp = client.get("/local-ai/optimize?query=qwen2.5:0.5b")
        assert resp.status_code == 200
        body = resp.json()
        assert "model" in body
        assert "backend" in body
    finally:
        set_local_bypass(None)

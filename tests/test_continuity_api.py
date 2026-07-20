from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_resume_prompt_compact() -> None:
    client = TestClient(create_app())
    response = client.get("/continuity/resume-prompt", params={"active_task": "retarget Grafana"})
    assert response.status_code == 200
    body = response.json()
    assert "prompt" in body
    assert body["prompt"].startswith("### MSB_SESSION_CONTINUITY_V1 ###")
    assert "active_task=retarget Grafana" in body["prompt"]


def test_resume_prompt_json() -> None:
    client = TestClient(create_app())
    response = client.get("/continuity/resume-prompt", params={"format": "json", "topic": "observability"})
    assert response.status_code == 200
    body = response.json()
    assert "compact" in body
    assert "topic=observability" in body["compact"]

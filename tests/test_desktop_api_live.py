from __future__ import annotations

import sys
from pathlib import Path

REPO = Path("/Users/lordwilson/msb-v2").resolve()
sys.path = [p for p in sys.path if "/.hermes/" not in p and "/site-packages" not in p]
sys.path.insert(0, str(REPO))
sys.path.insert(0, "/opt/homebrew/Caskroom/miniforge/base/lib/python3.12/site-packages")

from fastapi.testclient import TestClient  # noqa: E402
from msb_v2.api.web import create_app  # noqa: E402

client = TestClient(create_app())


def test_desktop_health():
    r = client.get("/desktop/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_desktop_status_idle():
    r = client.get("/desktop/status")
    assert r.status_code == 200
    body = r.json()
    assert body["state"] == "idle"


def test_desktop_stop_is_idempotent():
    r = client.post("/desktop/stop")
    assert r.status_code == 200
    body = r.json()
    assert body["stopped"] is True


def test_desktop_execute_requires_env():
    r = client.post("/desktop/execute", json={"goal": "Launch app and delete data", "intent": "desktop"})
    assert r.status_code == 200
    body = r.json()
    assert body["state"] == "blocked"


def test_desktop_route_with_missing_env():
    r = client.post("/desktop/execute", json={"goal": "Automate taking screenshots", "intent": "desktop"})
    assert r.status_code == 200
    body = r.json()
    assert body["state"] in {"pending_confirmation", "blocked"}


def test_desktop_execute_high_risk_returns_blocked_without_env():
    r = client.post("/desktop/execute", json={"goal": "Launch Safari, click a button and send message", "intent": "desktop"})
    assert r.status_code == 200
    body = r.json()
    assert body["state"] == "blocked"
    assert "NEURALAGENT_USER_ACCESS_TOKEN" in body.get("prerequisites", {}).get("missing", [])
    assert body.get("confirm_token") is None


def test_desktop_approve_rejects_invalid_token():
    r = client.post("/desktop/approve?confirm_token=bogus&approved=true")
    assert r.status_code == 200
    body = r.json()
    assert body["state"] == "error"


def test_desktop_approve_rejected(monkeypatch):
    monkeypatch.setenv("NEURALAGENT_USER_ACCESS_TOKEN", "tok")
    monkeypatch.setenv("NEURALAGENT_THREAD_ID", "thr")
    r1 = client.post("/desktop/execute", json={"goal": "Launch Safari and send message", "intent": "desktop"})
    token = r1.json().get("confirm_token")
    assert token
    r2 = client.post(f"/desktop/approve?confirm_token={token}&approved=false")
    assert r2.status_code in {200, 409}
    body = r2.json()
    assert body["state"] == "rejected"


def test_desktop_keyword_meta_route():
    r = client.post("/meta/route", json={
        "query": "Design and automate a desktop workflow that clicks types and launches apps",
        "context": {},
    })
    assert r.status_code == 200
    body = r.json()
    assert body["routing"]["primary"] == "desktop"


def test_brain_meta_run_desktop_intent():
    r = client.post("/brain/meta-run", json={
        "query": "Automate opening Finder and taking a screenshot",
        "intent": "desktop",
        "trace_id": "trace-desktop",
    })
    assert r.status_code == 200
    body = r.json()
    assert body["intent"] == "desktop"
    assert body["meta_routing"]["primary"] == "desktop"

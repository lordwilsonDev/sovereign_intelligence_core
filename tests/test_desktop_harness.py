from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path = [p for p in sys.path if "/.hermes/" not in p and "/site-packages" not in p]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, "/opt/homebrew/Caskroom/miniforge/base/lib/python3.12/site-packages")

from fastapi.testclient import TestClient
from msb_v2.api.web import create_app


client = TestClient(create_app())


def test_desktop_health():
    r = client.get("/desktop/health")
    assert r.status_code == 200
    assert r.json()["module"] == "desktop"


def test_desktop_execute_requires_env(monkeypatch):
    monkeypatch.delenv("NEURALAGENT_API_URL", raising=False)
    monkeypatch.delenv("NEURALAGENT_USER_ACCESS_TOKEN", raising=False)
    monkeypatch.delenv("NEURALAGENT_THREAD_ID", raising=False)
    r = client.post("/desktop/execute", json={"goal": "Open Finder and screenshot", "timeout_s": 1})
    assert r.status_code == 200
    body = r.json()
    assert body["state"] == "blocked"
    assert body["prerequisites"]["missing"]

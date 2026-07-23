"""Observer's Log API mount tests."""
from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


def test_observer_log_routes_mount_from_router() -> None:
    from msb_v2.api.observer_log import router as observer_log_router
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(observer_log_router, prefix="/observer-log")
    client = TestClient(app)
    assert client.get("/observer-log/recent").status_code == 200
    assert client.post("/observer-log/emit", json={"source": "s", "message": "m"}).status_code == 200
    assert client.post("/observer-log/clear").status_code == 200

from __future__ import annotations

from fastapi.testclient import TestClient
from msb_v2.api.web import create_app


def test_ui_index_is_index_html():
    client = TestClient(create_app())
    r = client.get("/ui/")
    assert r.status_code == 200
    assert "<!DOCTYPE html>" in r.text
    assert "Level 33 Dashboard" in r.text


def test_ui_static_css_is_exposed():
    client = TestClient(create_app())
    r = client.get("/ui/static/css/style.css")
    assert r.status_code == 200
    assert "body" in r.text or "container" in r.text



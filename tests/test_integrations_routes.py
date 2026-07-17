from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


client = TestClient(create_app())


def test_integrations_content_articles_empty() -> None:
    r = client.get("/integrations/content/articles")
    assert r.status_code == 200
    assert r.json()["articles"] == []


def test_integrations_content_refresh_empty_urls() -> None:
    r = client.post("/integrations/content/refresh", json={"urls": []})
    assert r.status_code == 200
    assert r.json()["added"] == []


def test_integrations_content_refresh_round_trip() -> None:
    r = client.post(
        "/integrations/content/refresh",
        json={"urls": ["https://example.com/feed.rss"]},
    )
    assert r.status_code == 200
    body = r.json()
    assert "added" in body

    r = client.get("/integrations/content/articles")
    assert r.status_code == 200
    assert len(r.json()["articles"]) == len(body["added"])

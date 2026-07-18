from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app

client = TestClient(create_app())


def test_integrations_content_refresh_returns_status() -> None:
    response = client.post("/integrations/content/refresh", json={})
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)


def test_integrations_content_articles_returns_payload() -> None:
    response = client.get("/integrations/content/articles")
    assert response.status_code == 200
    body = response.json()
    assert "articles" in body
    assert isinstance(body.get("articles"), list)


def test_integrations_content_search_route() -> None:
    response = client.get("/integrations/content/search", params={"q": "test"})
    assert response.status_code == 200
    body = response.json()
    assert "results" in body or "query" in body

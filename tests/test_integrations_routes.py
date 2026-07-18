from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


client = TestClient(create_app())


def test_integrations_search_filter_endpoint():
    r = client.get("/integrations/content/search?q=AI&limit=5")
    assert r.status_code == 200
    body = r.json()
    assert body["query"] == "AI"
    assert "results" in body


def test_integrations_github_issues_endpoint():
    r = client.get("/integrations/github/issues", params={"owner": "octocat", "repo": "Hello-World", "limit": 5})
    assert r.status_code == 200
    body = r.json()
    assert "issues" in body


def test_integrations_github_prs_endpoint():
    r = client.get("/integrations/github/prs", params={"owner": "octocat", "repo": "Hello-World", "limit": 5})
    assert r.status_code == 200
    body = r.json()
    assert "prs" in body

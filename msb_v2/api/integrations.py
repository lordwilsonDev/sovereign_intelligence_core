from __future__ import annotations

from fastapi import APIRouter, Body, Depends, Query
from pydantic import BaseModel

from msb_v2.api.middleware import require_bearer_token
from msb_v2.integrations.article_store import InMemoryArticleStore
from msb_v2.integrations.content_service import ContentService
from msb_v2.integrations.github import fetch_github_issues, fetch_github_prs
from msb_v2.integrations.rss import RSSArticle

from msb_v2.v3.contracts import HarnessContract
from msb_v2.v3.contracts import register as _register_contract
router = APIRouter(tags=["integrations"])

_store = InMemoryArticleStore()
_service = ContentService(store=_store)


class RefreshRequest(BaseModel):
    urls: list[str] = []


@router.post("/integrations/content/refresh", dependencies=[Depends(require_bearer_token)])
def refresh_content(payload: RefreshRequest) -> dict:
    added = _service.refresh_from_rss(payload.urls or [])
    return {"added": [article.link for article in added]}


@router.get("/integrations/content/articles")
def list_articles() -> dict:
    items = [article.__dict__ for article in _service.store.all()]
    return {"articles": items}


@router.get("/integrations/content/search")
def search_articles(q: str = Query(...), limit: int = 20) -> dict:
    store = _service.store
    items = [article.__dict__ for article in store.search(q, limit=limit)]
    return {"query": q, "results": items, "count": len(items)}


@router.get("/integrations/github/issues")
def github_issues(owner: str, repo: str, limit: int = 20) -> dict:
    items = [issue.__dict__ for issue in fetch_github_issues(owner, repo, limit=limit)]
    return {"owner": owner, "repo": repo, "issues": items, "count": len(items)}


@router.get("/integrations/github/prs")
def github_prs(owner: str, repo: str, limit: int = 20) -> dict:
    items = [pr.__dict__ for pr in fetch_github_prs(owner, repo, limit=limit)]
    return {"owner": owner, "repo": repo, "prs": items, "count": len(items)}
# HCL contract registration
_register_contract(HarnessContract(route="/integrations/content/refresh", method="post", allow_anonymous=False))

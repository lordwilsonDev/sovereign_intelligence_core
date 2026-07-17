from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from msb_v2.integrations.article_store import InMemoryArticleStore
from msb_v2.integrations.content_service import ContentService
from msb_v2.integrations.rss import RSSArticle

router = APIRouter(tags=["integrations"])

_store = InMemoryArticleStore()
_service = ContentService(store=_store)


class RefreshRequest(BaseModel):
    urls: list[str] = []


@router.post("/integrations/content/refresh")
def refresh_content(payload: RefreshRequest) -> dict:
    added = _service.refresh_from_rss(payload.urls or [])
    return {"added": [article.link for article in added]}


@router.get("/integrations/content/articles")
def list_articles() -> dict:
    items = [article.__dict__ for article in _service.store.all()]
    return {"articles": items}

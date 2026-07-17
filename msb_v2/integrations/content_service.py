from __future__ import annotations

from typing import List

from msb_v2.integrations.article_store import ArticleStore, RSSArticle
from msb_v2.integrations.rss import fetch_rss_articles


class ContentService:
    def __init__(self, store: ArticleStore) -> None:
        self.store = store

    def refresh_from_rss(self, urls: List[str]) -> List[RSSArticle]:
        added: List[RSSArticle] = []
        for url in urls:
            added.extend(self.refresh_feed(url))
        return added

    def refresh_feed(self, url: str) -> List[RSSArticle]:
        articles = fetch_rss_articles(url)
        return self.store.add_many(articles)

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class RSSArticle:
    title: str
    link: str
    published: str = ""


def fetch_rss_articles(url: str) -> List[RSSArticle]:
    articles: List[RSSArticle] = []
    try:
        import feedparser

        feed = feedparser.parse(url)
    except Exception:
        return articles
    for item in getattr(feed, "entries", []):
        title = getattr(item, "title", "") or ""
        link = getattr(item, "link", "") or ""
        published = getattr(item, "published", "") or ""
        if title and link:
            articles.append(RSSArticle(title=title, link=link, published=published))
    return articles

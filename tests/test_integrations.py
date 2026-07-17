from __future__ import annotations

import types

import pytest

from msb_v2.integrations.article_store import InMemoryArticleStore, SQLiteArticleStore
from msb_v2.integrations.rss import RSSArticle, fetch_rss_articles


class FakeEntry:
    title = "Test Title"
    link = "https://example.com/1"
    published = "2026-01-01"


def test_fetch_rss_articles_parses_entries(monkeypatch: pytest.MonkeyPatch) -> None:
    feed = types.SimpleNamespace(entries=[FakeEntry()])
    module = types.SimpleNamespace(parse=lambda url: feed)
    monkeypatch.setitem(__import__("sys").modules, "feedparser", module)  # type: ignore[arg-type]
    articles = fetch_rss_articles("https://example.com/rss")
    assert len(articles) == 1
    assert articles[0].title == "Test Title"


def test_fetch_rss_articles_handles_missing_dependency(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(__import__("sys").modules, "feedparser", None)  # type: ignore[arg-type]
    articles = fetch_rss_articles("https://example.com/rss")
    assert articles == []


def test_in_memory_store_deduplicates() -> None:
    store = InMemoryArticleStore()
    article = RSSArticle(title="t", link="https://example.com/1")
    assert store.add(article) is True
    assert store.add(article) is False
    assert len(store.all()) == 1


def test_sqlite_store_round_trip(tmp_path: str) -> None:
    db = str(tmp_path / "articles.db")
    store = SQLiteArticleStore(db_path=db)
    article = RSSArticle(title="sqlite", link="https://example.com/sqlite", published="now")
    assert store.add(article) is True
    assert store.add(article) is False
    rows = store.all()
    assert len(rows) == 1
    assert rows[0].title == "sqlite"

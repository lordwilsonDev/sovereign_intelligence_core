from __future__ import annotations

import sqlite3
from pathlib import Path

from msb_v2.integrations.article_store import RSSArticle, SQLiteArticleStore


def test_search_returns_matches(tmp_path):
    db = tmp_path / "articles.db"
    store = SQLiteArticleStore(db_path=str(db))
    store.add_many([
        RSSArticle(title="AI inference", link="https://example.com/1", published="2026-01-01"),
        RSSArticle(title="Rust async", link="https://example.com/2", published="2026-01-02"),
    ])
    results = store.search("AI")
    assert [r.title for r in results] == ["AI inference"]


def test_search_empty_returns_all(tmp_path):
    db = tmp_path / "articles.db"
    store = SQLiteArticleStore(db_path=str(db))
    store.add_many([
        RSSArticle(title="Alpha", link="https://example.com/1"),
        RSSArticle(title="Beta", link="https://example.com/2"),
    ])
    results = store.search("")
    assert len(results) == 2


def test_fts5_mirrors_insert(tmp_path):
    db = tmp_path / "articles.db"
    store = SQLiteArticleStore(db_path=str(db))
    store.add(RSSArticle(title="Hello world", link="https://example.com/1"))
    with sqlite3.connect(db) as conn:
        rows = conn.execute("SELECT title FROM articles_fts WHERE articles_fts MATCH 'hello'").fetchall()
    assert rows == [("Hello world",)]


def test_search_no_results(tmp_path):
    db = tmp_path / "articles.db"
    store = SQLiteArticleStore(db_path=str(db))
    store.add(RSSArticle(title="Alpha", link="https://example.com/1"))
    assert store.search("zzz") == []

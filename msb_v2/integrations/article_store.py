from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Iterable, List, Protocol, runtime_checkable


@dataclass(frozen=True)
class RSSArticle:
    title: str
    link: str
    published: str = ""


@runtime_checkable
class ArticleStore(Protocol):
    def add(self, article: RSSArticle) -> bool: ...
    def add_many(self, articles: Iterable[RSSArticle]) -> List[RSSArticle]:
        ...

    def all(self) -> List[RSSArticle]: ...

    def search(self, query: str, limit: int = 20) -> List[RSSArticle]: ...


class InMemoryArticleStore:
    def __init__(self) -> None:
        self._items: List[RSSArticle] = []
        self._lock = threading.Lock()

    def add(self, article: RSSArticle) -> bool:
        with self._lock:
            if any(item.link == article.link for item in self._items):
                return False
            self._items.append(article)
            return True

    def add_many(self, articles: Iterable[RSSArticle]) -> List[RSSArticle]:
        added: List[RSSArticle] = []
        for article in articles:
            if self.add(article):
                added.append(article)
        return added

    def all(self) -> List[RSSArticle]:
        with self._lock:
            return list(self._items)

    def search(self, query: str, limit: int = 20) -> List[RSSArticle]:
        q = query.casefold().strip()
        if not q:
            return self.all()[:limit]
        scored = []
        for item in self._items:
            text = f"{item.title} {item.link} {item.published}".casefold()
            score = text.count(q)
            scored.append((score, item))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for score, item in scored[:limit] if score > 0]


class SQLiteArticleStore:
    def __init__(self, db_path: str = "data/articles.db") -> None:
        self.db_path = db_path
        self._lock = threading.Lock()
        self._init_schema()

    def _connect(self):  # noqa: ANN001
        import sqlite3

        return sqlite3.connect(self.db_path)

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS articles ("
                "title TEXT NOT NULL, link TEXT NOT NULL PRIMARY KEY, published TEXT)"
            )
            conn.execute(
                "CREATE VIRTUAL TABLE IF NOT EXISTS articles_fts USING fts5(title, link, published, "
                "content='articles', content_rowid='rowid')"
            )
            conn.execute(
                "CREATE TRIGGER IF NOT EXISTS articles_ai AFTER INSERT ON articles BEGIN "
                "INSERT INTO articles_fts(rowid, title, link, published) VALUES (new.rowid, new.title, new.link, new.published); END"
            )
            conn.execute(
                "CREATE TRIGGER IF NOT EXISTS articles_ad AFTER DELETE ON articles BEGIN "
                "INSERT INTO articles_fts(articles_fts, rowid, title, link, published) VALUES ('delete', old.rowid, old.title, old.link, old.published); END"
            )
            conn.execute(
                "CREATE TRIGGER IF NOT EXISTS articles_au AFTER UPDATE ON articles BEGIN "
                "INSERT INTO articles_fts(articles_fts, rowid, title, link, published) VALUES ('delete', old.rowid, old.title, old.link, old.published); "
                "INSERT INTO articles_fts(rowid, title, link, published) VALUES (new.rowid, new.title, new.link, new.published); END"
            )
            conn.commit()

    def add(self, article: RSSArticle) -> bool:
        with self._lock:
            try:
                with self._connect() as conn:
                    conn.execute(
                        "INSERT INTO articles(title, link, published) VALUES(?,?,?)",
                        (article.title, article.link, article.published),
                    )
                    conn.commit()
                    return True
            except Exception:
                return False

    def add_many(self, articles: Iterable[RSSArticle]) -> List[RSSArticle]:
        added: List[RSSArticle] = []
        for article in articles:
            if self.add(article):
                added.append(article)
        return added

    def all(self) -> List[RSSArticle]:
        with self._connect() as conn:
            rows = conn.execute("SELECT title, link, published FROM articles").fetchall()
            return [RSSArticle(title=title, link=link, published=published) for title, link, published in rows]

    def search(self, query: str, limit: int = 20) -> List[RSSArticle]:
        q = query.strip()
        if not q:
            return self.all()[:limit]
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT title, link, published, rank FROM articles_fts WHERE articles_fts MATCH ? ORDER BY rank LIMIT ?",
                (q, limit),
            ).fetchall()
            return [RSSArticle(title=title, link=link, published=published) for title, link, published, _ in rows]

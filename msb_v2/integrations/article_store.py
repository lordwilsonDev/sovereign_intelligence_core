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

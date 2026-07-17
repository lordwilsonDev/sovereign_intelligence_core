from __future__ import annotations

from pathlib import Path
from typing import Iterable, NamedTuple


DATA_SOURCES = [
    Path("/Users/lordwilson/hermes-brain"),
    Path("/Users/lordwilson/Library/Mobile Documents/com~apple~CloudDocs/Standard Notes/jrnlhdeobsidian"),
]


class KnowledgeSnapshot(NamedTuple):
    entries: int
    links: int


_WIKI_LINK_PREFIXES = ("[[", "]",)


def _iter_markdown(paths: Iterable[Path]) -> Iterable[Path]:
    for base in paths:
        if not base.exists():
            continue
        for candidate in base.rglob("*.md"):
            if candidate.is_file():
                yield candidate


def _count_links(candidate: Path) -> int:
    text = candidate.read_text(errors="ignore")
    return text.count("[[") + text.count("]]")


def snapshot(paths=None):
    if paths is None:
        paths = DATA_SOURCES
    files = list(_iter_markdown(paths))
    links = sum(_count_links(path) for path in files)
    return KnowledgeSnapshot(entries=len(files), links=links)

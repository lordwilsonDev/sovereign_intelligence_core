from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class SnapshotResult:
    entries: int
    links: int


def snapshot(paths: List[Path]) -> SnapshotResult:
    entries = 0
    links = 0
    for path in paths:
        if not path.exists():
            continue
        if path.is_file():
            entries += 1
            links += path.read_text().count("[")
        elif path.is_dir():
            for p in path.rglob("*.md"):
                entries += 1
                links += p.read_text(errors="ignore").count("[")
    return SnapshotResult(entries=entries, links=links)

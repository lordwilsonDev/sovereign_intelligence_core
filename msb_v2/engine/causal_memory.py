from __future__ import annotations

from collections import deque
from typing import Dict, List, Optional


def _has_path(links: Dict[str, List[tuple[str, str]]], source: str, target: str) -> bool:
    if source == target:
        return True
    queue = deque([source])
    visited = {source}
    while queue:
        node = queue.popleft()
        for tgt, _ in links.get(node, []):
            if tgt == target:
                return True
            if tgt not in visited:
                visited.add(tgt)
                queue.append(tgt)
    return False


class StateSnapshot:
    """Lightweight continuity proof for a CausalMemory state."""

    __slots__ = ("links", "previous_hash")

    def __init__(self, links: Dict[str, List[tuple[str, str]]], previous_hash: Optional[str] = None) -> None:
        self.links = links
        self.previous_hash = previous_hash

    def payload(self) -> bytes:
        parts = []
        for source in sorted(self.links):
            for target, relation in sorted(self.links[source], key=lambda x: (x[0], x[1])):
                parts.append(f"{source}->{target}:{relation}".encode())
        return b"\x00".join(parts) if parts else b""

    def merkle_parts(self) -> list[str]:
        return [
            f"{source}->{target}:{relation}"
            for source in sorted(self.links)
            for target, relation in sorted(self.links[source], key=lambda x: (x[0], x[1]))
        ]

    @property
    def hash(self) -> str:
        base = self.payload()
        chained = base if self.previous_hash is None else self.previous_hash.encode() + b"|" + base
        return "sha256:" + __import__("hashlib").sha256(chained).hexdigest()


class CausalMemory:
    def __init__(self, snapshot_secret: str = "", max_links: int = 100000) -> None:
        self.links: Dict[str, List[tuple[str, str]]] = {}
        self.previous_hash: Optional[str] = None
        self.snapshot_secret = snapshot_secret
        self.max_links = max_links
        self.link_count = 0

    def link(self, source: str, target: str, relation: str = "caused") -> None:
        if source == target or _has_path(self.links, target, source):
            return
        if self.link_count >= self.max_links:
            raise MemoryError("CausalMemory link budget exceeded")
        self.links.setdefault(source, []).append((target, relation))
        self.link_count += 1
        self.previous_hash = StateSnapshot(self.links, self.previous_hash).hash

    def has_link(self, source: str, target: str) -> bool:
        return any(t == target for t, _ in self.links.get(source, []))

    def reasons_for(self, node: str) -> List[str]:
        out = []
        for src, targets in self.links.items():
            for tgt, relation in targets:
                if tgt == node:
                    out.append(f"{src}->{node}::{relation}")
        return out

    def snapshot(self) -> StateSnapshot:
        return StateSnapshot(self.links, self.previous_hash)

    def current_hash(self) -> str:
        return self.snapshot().hash

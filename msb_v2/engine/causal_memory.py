from __future__ import annotations

from typing import Dict, List


class CausalMemory:
    def __init__(self) -> None:
        self.links: Dict[str, List[tuple[str, str]]] = {}

    def link(self, source: str, target: str, relation: str = "caused") -> None:
        self.links.setdefault(source, []).append((target, relation))

    def has_link(self, source: str, target: str) -> bool:
        relations = self.links.get(source, [])
        return any(t == target for t, _ in relations)

    def reasons_for(self, node: str) -> List[str]:
        out = []
        for src, targets in self.links.items():
            for tgt, relation in targets:
                if tgt == node:
                    out.append(f"{src}->{node}::{relation}")
        return out

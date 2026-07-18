from __future__ import annotations

from typing import Dict, List

from msb_v2.knowledge.graph import KnowledgeGraph


class GraphRanker:
    def __init__(self, graph: KnowledgeGraph) -> None:
        self.graph = graph

    def bfs_rank(self, start: str, depth: int = 2) -> Dict[str, int]:
        visited = {start: 0}
        queue = [start]
        while queue:
            node = queue.pop(0)
            if visited[node] >= depth:
                continue
            for nb in self.graph.neighbors(node):
                nxt = nb["target"]
                if nxt not in visited:
                    visited[nxt] = visited[node] + 1
                    queue.append(nxt)
        return visited

    def top_targets(self, start: str, depth: int = 2, limit: int = 10) -> List[dict]:
        ranks = self.bfs_rank(start, depth=depth)
        scored = []
        for node_id, dist in ranks.items():
            if node_id == start:
                continue
            scored.append({"target": node_id, "distance": dist, "score": round(1.0 / max(1, dist), 2)})
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:limit]

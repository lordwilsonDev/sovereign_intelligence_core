from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass(frozen=True)
class GraphNode:
    node_id: str
    label: str
    node_type: str = "concept"
    weight: float = 0.5


@dataclass(frozen=True)
class GraphEdge:
    source: str
    target: str
    relation: str
    weight: float = 0.5


class KnowledgeGraph:
    def __init__(self, db_path: str = "./knowledge_graph.db") -> None:
        self.db_path = str(Path(db_path).resolve())
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init()

    def _init(self) -> None:
        cur = self._conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS nodes (node_id TEXT PRIMARY KEY, label TEXT NOT NULL, node_type TEXT, weight REAL)"
        )
        cur.execute(
            "CREATE TABLE IF NOT EXISTS edges (source TEXT NOT NULL, target TEXT NOT NULL, relation TEXT NOT NULL, weight REAL, PRIMARY KEY (source, target, relation))"
        )
        cur.execute("CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target)")
        self._conn.commit()

    def add_node(self, node: GraphNode) -> None:
        cur = self._conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO nodes VALUES (?,?,?,?)",
            (node.node_id, node.label, node.node_type, node.weight),
        )
        self._conn.commit()

    def add_edge(self, edge: GraphEdge) -> None:
        cur = self._conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO edges VALUES (?,?,?,?)",
            (edge.source, edge.target, edge.relation, edge.weight),
        )
        self._conn.commit()

    def neighbors(self, node_id: str) -> List[dict]:
        cur = self._conn.cursor()
        cur.execute(
            "SELECT target, relation, weight FROM edges WHERE source = ?", (node_id,)
        )
        return [dict(r) for r in cur.fetchall()]

    def shortest_path(self, start: str, end: str) -> List[str]:
        visited = {start}
        queue = [[start]]
        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node == end:
                return path
            for nb in self.neighbors(node):
                nxt = nb["target"]
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(path + [nxt])
        return []


class LearningEngine:
    def __init__(self, graph: KnowledgeGraph) -> None:
        self.graph = graph
        self.heuristics: dict[str, float] = {}

    def update_from_outcome(self, node_id: str, outcome: str, delta: float = 0.05) -> None:
        current = self.heuristics.get(node_id, 0.5)
        if outcome == "success":
            current = min(1.0, current + delta)
        elif outcome == "failure":
            current = max(0.0, current - delta)
        self.heuristics[node_id] = current

    def recommend(self, node_id: str) -> dict:
        neighbors = self.graph.neighbors(node_id)
        if not neighbors:
            return {"node_id": node_id, "next": None, "confidence": 0.0}
        ranked = sorted(neighbors, key=lambda x: x.get("weight", 0.0), reverse=True)
        nxt = ranked[0]["target"]
        score = self.heuristics.get(nxt, 0.5)
        return {"node_id": node_id, "next": nxt, "confidence": score}

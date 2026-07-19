from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter

router = APIRouter(tags=["knowledge"])


class SimpleKnowledgeGraph:
    def __init__(self) -> None:
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, Any]] = []

    def upsert_node(self, node_id: str, labels: Optional[List[str]] = None, properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self.nodes[node_id] = {"id": node_id, "labels": labels or [], "properties": properties or {}}
        return self.nodes[node_id]

    def add_edge(self, source: str, target: str, relation: str, properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        edge = {"source": source, "target": target, "relation": relation, "properties": properties or {}}
        self.edges.append(edge)
        return edge

    def neighbors(self, node_id: str) -> List[Dict[str, Any]]:
        result = []
        for edge in self.edges:
            if edge["source"] == node_id:
                nid = edge["target"]
            elif edge["target"] == node_id:
                nid = edge["source"]
            else:
                continue
            result.append({"node_id": nid, "node": self.nodes.get(nid), "edge": edge})
        return result


kg = SimpleKnowledgeGraph()


@router.post("/knowledge/nodes")
def knowledge_nodes(body: Dict[str, Any]) -> Dict[str, Any]:
    node_id = str(body.get("id", ""))
    if not node_id:
        return {"error": "id required"}
    return kg.upsert_node(node_id, labels=body.get("labels"), properties=body.get("properties"))


@router.get("/knowledge/neighbors/{node_id}")
def knowledge_neighbors(node_id: str) -> Dict[str, Any]:
    return {"node_id": node_id, "neighbors": kg.neighbors(node_id)}


@router.post("/knowledge/edges")
def knowledge_edges(body: Dict[str, Any]) -> Dict[str, Any]:
    source = str(body.get("source", ""))
    target = str(body.get("target", ""))
    relation = str(body.get("relation", ""))
    if not source or not target or not relation:
        return {"error": "source, target, relation required"}
    return kg.add_edge(source, target, relation, properties=body.get("properties"))

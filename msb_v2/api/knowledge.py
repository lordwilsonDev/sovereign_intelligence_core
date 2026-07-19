from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from msb_v2.api.middleware import require_bearer_token
from msb_v2.knowledge.graph import GraphEdge, GraphNode, KnowledgeGraph

router = APIRouter(tags=["knowledge"])
_graph = KnowledgeGraph(db_path="./knowledge_graph_api.db")


class UpsertNodeRequest(BaseModel):
    id: str
    labels: Optional[List[str]] = None
    properties: Optional[Dict[str, Any]] = None


class AddEdgeRequest(BaseModel):
    source: str
    target: str
    relation: str
    properties: Optional[Dict[str, Any]] = None


@router.post("/knowledge/nodes")
def knowledge_nodes(payload: UpsertNodeRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    node = GraphNode(node_id=payload.id, label=payload.id)
    _graph.add_node(node)
    return {"id": node.node_id, "status": "added"}


@router.get("/knowledge/neighbors/{node_id}")
def knowledge_neighbors(node_id: str) -> Dict[str, Any]:
    return {"node_id": node_id, "neighbors": _graph.neighbors(node_id)}


@router.post("/knowledge/edges")
def knowledge_edges(payload: AddEdgeRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    edge = GraphEdge(source=payload.source, target=payload.target, relation=payload.relation)
    _graph.add_edge(edge)
    return {"source": edge.source, "target": edge.target, "relation": edge.relation, "status": "added"}

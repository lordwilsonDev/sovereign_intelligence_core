from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from msb_v2.knowledge.graph import KnowledgeGraph, LearningEngine, GraphNode, GraphEdge
from msb_v2.knowledge.ranker import GraphRanker

router = APIRouter(tags=["v3-knowledge"])

_graph = KnowledgeGraph()
_learning = LearningEngine(graph=_graph)
_ranker = GraphRanker(graph=_graph)


@router.post("/v3/knowledge/nodes")
def add_node(payload: dict) -> JSONResponse:
    node_id = payload.get("node_id", "")
    label = payload.get("label", node_id)
    node = GraphNode(
        node_id=node_id,
        label=label,
        node_type=payload.get("node_type", "concept"),
        weight=float(payload.get("weight", 0.5)),
    )
    _graph.add_node(node)
    return JSONResponse({"node_id": node_id, "status": "added"})


@router.post("/v3/knowledge/edges")
def add_edge(payload: dict) -> JSONResponse:
    edge = GraphEdge(
        source=payload.get("source", ""),
        target=payload.get("target", ""),
        relation=payload.get("relation", "related"),
        weight=float(payload.get("weight", 0.5)),
    )
    _graph.add_edge(edge)
    return JSONResponse({"source": edge.source, "target": edge.target, "status": "added"})


@router.get("/v3/knowledge/neighbors/{node_id}")
def get_neighbors(node_id: str) -> JSONResponse:
    n = _graph.neighbors(node_id)
    return JSONResponse({"node_id": node_id, "neighbors": n, "count": len(n)})


@router.get("/v3/knowledge/shortest-path")
def shortest_path(start: str, end: str) -> JSONResponse:
    path = _graph.shortest_path(start, end)
    return JSONResponse({"start": start, "end": end, "path": path, "found": bool(path)})


@router.post("/v3/knowledge/update-outcome")
def update_outcome(payload: dict) -> JSONResponse:
    node_id = payload.get("node_id", "")
    outcome = payload.get("outcome", "")
    delta = float(payload.get("delta", 0.05))
    _learning.update_from_outcome(node_id, outcome, delta=delta)
    return JSONResponse({"node_id": node_id, "heuristic": _learning.heuristics.get(node_id, 0.5)})


@router.get("/v3/knowledge/recommend/{node_id}")
def recommend(node_id: str) -> JSONResponse:
    rec = _learning.recommend(node_id)
    return JSONResponse(rec)


@router.get("/v3/knowledge/rank")
def rank_targets(start: str, depth: int = 2, limit: int = 10) -> JSONResponse:
    ranked = _ranker.top_targets(start, depth=depth, limit=limit)
    return JSONResponse({"start": start, "depth": depth, "ranked": ranked, "count": len(ranked)})

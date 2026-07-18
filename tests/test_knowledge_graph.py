from __future__ import annotations

from msb_v2.knowledge.graph import KnowledgeGraph, LearningEngine


def test_graph_nodes_and_edges():
    g = KnowledgeGraph()
    g.add_node(graphmodule.GraphNode(node_id="a", label="A", node_type="concept", weight=0.7))
    g.add_node(graphmodule.GraphNode(node_id="b", label="B", node_type="concept", weight=0.4))
    g.add_edge(graphmodule.GraphEdge(source="a", target="b", relation="depends_on", weight=0.8))
    n = g.neighbors("a")
    assert len(n) == 1
    assert n[0]["target"] == "b"


def test_shortest_path_finds_route():
    g = KnowledgeGraph()
    g.add_node(graphmodule.GraphNode(node_id="a", label="A"))
    g.add_node(graphmodule.GraphNode(node_id="b", label="B"))
    g.add_node(graphmodule.GraphNode(node_id="c", label="C"))
    g.add_edge(graphmodule.GraphEdge(source="a", target="b", relation="next"))
    g.add_edge(graphmodule.GraphEdge(source="b", target="c", relation="next"))
    assert g.shortest_path("a", "c") == ["a", "b", "c"]


def test_learning_engine_updates_heuristic():
    g = KnowledgeGraph()
    engine = LearningEngine(graph=g)
    assert engine.heuristics.get("x", 0.5) == 0.5
    engine.update_from_outcome("x", "success")
    assert engine.heuristics["x"] == 0.55


def test_learning_engine_recommend():
    g = KnowledgeGraph()
    g.add_node(graphmodule.GraphNode(node_id="a", label="A"))
    g.add_node(graphmodule.GraphNode(node_id="b", label="B"))
    g.add_edge(graphmodule.GraphEdge(source="a", target="b", relation="next", weight=0.9))
    engine = LearningEngine(graph=g)
    rec = engine.recommend("a")
    assert rec["next"] == "b"
    assert rec["confidence"] == 0.5


import msb_v2.knowledge.graph as graphmodule

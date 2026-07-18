from __future__ import annotations

from msb_v2.knowledge.graph import KnowledgeGraph, LearningEngine


def test_graph_and_learning_recommend_next_step():
    g = KnowledgeGraph()
    g.add_node(graphmodule.GraphNode(node_id="alpha", label="Alpha", weight=0.8))
    g.add_node(graphmodule.GraphNode(node_id="beta", label="Beta", weight=0.4))
    g.add_edge(graphmodule.GraphEdge(source="alpha", target="beta", relation="next", weight=0.9))

    engine = LearningEngine(graph=g)
    rec = engine.recommend("alpha")
    assert rec["next"] == "beta"
    assert rec["confidence"] == 0.5


def test_learning_engine_updates_heuristic():
    engine = LearningEngine(graph=KnowledgeGraph())
    assert engine.heuristics.get("x", 0.5) == 0.5
    engine.update_from_outcome("x", "success")
    assert engine.heuristics["x"] == 0.55


import msb_v2.knowledge.graph as graphmodule

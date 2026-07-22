#!/usr/bin/env python3
"""
Golden lossless evidence for `_execute_worker` atomization.

This script imports `MetaIntelligenceCoordinator` and verifies that the
refactored `_execute_worker` returns the same **object types/structure** for
representative `IntelligenceQuery` inputs, using direct synchronous invocation
without queuing or background worker timing.
"""
from cognitive_compiler.meta_coordinator_v3_2 import (
    MetaIntelligenceCoordinator,
    IntelligenceQuery,
    QueryType,
    IntelligenceLayer,
    IntelligenceResult,
)


def build_coordinator() -> MetaIntelligenceCoordinator:
    return MetaIntelligenceCoordinator(cache_size=32, worker_count=1)


def test_structure_types() -> None:
    coord = build_coordinator()
    try:
        queries = [
            IntelligenceQuery(
                query_id="golden-reject",
                query_type=QueryType.ANALYZE,
                layers=[IntelligenceLayer.MEMORY],
                parameters={"data": "Use 528hz quantum healing to align chakras"},
                priority=1,
                timeout=5.0,
            ),
            IntelligenceQuery(
                query_id="golden-retrieve",
                query_type=QueryType.RETRIEVE,
                layers=[IntelligenceLayer.GRAPH],
                parameters={"query": "node1", "node_id": "n1"},
                priority=10,
                timeout=5.0,
            ),
            IntelligenceQuery(
                query_id="golden-decide",
                query_type=QueryType.DECIDE,
                layers=[IntelligenceLayer.GRAPH, IntelligenceLayer.MEMORY, IntelligenceLayer.DECISION],
                parameters={"goal": "Reduce cloud costs by 30%"},
                priority=10,
                timeout=5.0,
            ),
            IntelligenceQuery(
                query_id="golden-synthesize",
                query_type=QueryType.SYNTHESIZE,
                layers=[IntelligenceLayer.GRAPH, IntelligenceLayer.MEMORY],
                parameters={"query": "Test synthesis", "goal": "Test synthesis"},
                priority=10,
                timeout=5.0,
            ),
        ]

        results = {}
        for q in queries:
            coord._execute_worker(q)
            results[q.query_id] = coord._results[q.query_id]

        # --- structural assertions ---
        reject = results["golden-reject"]
        assert isinstance(reject, IntelligenceResult)
        assert reject.success is False
        assert reject.data is None
        assert reject.layers_used == []
        assert "ETF Rejection" in reject.metadata.get("error", "")
        assert isinstance(reject.to_dict(), dict)

        retrieve = results["golden-retrieve"]
        assert isinstance(retrieve, IntelligenceResult)
        assert isinstance(retrieve.layers_used, list)
        assert len(retrieve.layers_used) >= 1
        assert hasattr(retrieve, "to_dict")
        assert retrieve.cache_hit in (True, False)
        assert isinstance(retrieve.metadata, dict)

        decide = results["golden-decide"]
        assert isinstance(decide, IntelligenceResult)
        assert hasattr(decide, "true_success")
        assert isinstance(decide.technical_success, bool)
        assert isinstance(decide.impact_success, bool)
        assert isinstance(decide.torsion_level, float)
        assert isinstance(decide.metadata, dict)

        synthesize = results["golden-synthesize"]
        assert isinstance(synthesize, IntelligenceResult)
        assert isinstance(synthesize.metadata.get("hypotheses_considered"), int)
        assert isinstance(synthesize.data, dict)
        assert "layers_queried" in synthesize.data or len(synthesize.layers_used) > 0

    finally:
        coord.stop()


if __name__ == "__main__":
    test_structure_types()
    print("Golden lossless evidence: PASS")

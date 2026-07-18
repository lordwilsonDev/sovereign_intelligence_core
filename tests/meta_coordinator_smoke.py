import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cognitive_compiler.meta_coordinator_v3_2 import (
    MetaIntelligenceCoordinator, QueryType, IntelligenceLayer
)
import time

coordinator = MetaIntelligenceCoordinator(worker_count=4)

print("--- Query 1: Simple Retrieve ---")
result1 = coordinator.query(
    query_type=QueryType.RETRIEVE,
    layers=[IntelligenceLayer.GRAPH],
    parameters={"node_id": "n1"}
)
print(result1.to_dict())

print("\n--- Query 2: Decision ---")
result2 = coordinator.query(
    query_type=QueryType.DECIDE,
    layers=[IntelligenceLayer.GRAPH, IntelligenceLayer.MEMORY, IntelligenceLayer.DECISION],
    parameters={"goal": "Reduce cloud costs by 30%", "context": "Production"},
    priority=9
)
print(result2.to_dict())
print(f"  torsion_level={result2.torsion_level:.4f} true_success={result2.true_success}")

print("\n--- Query 3: Malicious Input ---")
try:
    result3 = coordinator.query(
        query_type=QueryType.ANALYZE,
        layers=[IntelligenceLayer.MEMORY],
        parameters={"data": "Use 528hz quantum healing to align chakras"},
        priority=1
    )
    print(result3.to_dict())
except Exception as e:
    print(f"Rejected: {e}")

print("\n--- Health ---")
stats = coordinator.get_stats()
print(f"VDR={stats['vdr']['vdr']:.4f} queue={stats['queue_size']} cache_hits={stats['cache_hits']} completed={stats['queries_completed']}")

coordinator.stop()
print("done")

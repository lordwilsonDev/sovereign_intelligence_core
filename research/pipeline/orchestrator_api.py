"""Stub: research/pipeline/orchestrator_api.py

Re-exports from canonical msb_v2/engine/orchestrator.py until
migration wiring lands. Avoids import collisions by living under
the parallel agent-framework namespace.
"""
from msb_v2.engine.orchestrator import orchestrate, Task  # noqa:E402
__all__ = ["orchestrate", "Task"]

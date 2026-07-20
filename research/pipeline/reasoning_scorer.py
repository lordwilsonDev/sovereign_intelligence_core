"""Stub: research/pipeline/reasoning_scorer.py

Re-exports from `msb_v2.reasoning.scorer` under the parallel
agent-framework namespace to avoid root-level collisions.
"""
from msb_v2.reasoning.scorer import ConfidenceAssessment, score_from_events  # noqa:E402
__all__ = ["ConfidenceAssessment", "score_from_events"]

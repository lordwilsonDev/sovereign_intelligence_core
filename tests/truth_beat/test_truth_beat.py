"""Truth Beat engine smoke tests."""
from __future__ import annotations

from typing import Any, Dict

from msb_v2.truth_beat.harness import TruthBeat


def test_truth_beat_strip_returns_expected_envelope() -> None:
    engine = TruthBeat()
    result = engine.strip("AI will replace all human jobs by 2030")
    assert result["original"] == "AI will replace all human jobs by 2030"
    assert "inversion" in result
    assert "moie_dialectic" in result
    assert "sac_verdict" in result
    assert "empirical_grounding" in result
    assert result["verdict"] in {"TRUTH", "LIE"}


def test_truth_beat_helpers_are_callable() -> None:
    engine = TruthBeat()
    assert callable(getattr(engine, "_call_research", None))
    assert callable(getattr(engine, "_call_kb4", None))
    assert callable(getattr(engine, "_call_sac", None))
    assert callable(getattr(engine, "_call_grounding", None))


def test_truth_beat_router_routes_include_expected_paths() -> None:
    from msb_v2.truth_beat.harness import router as truth_beat_router

    routes = {r.path for r in truth_beat_router.routes}
    assert "/truth-beat/pulse" in routes
    assert "/truth-beat/strip" in routes

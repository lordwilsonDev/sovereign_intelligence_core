import json
from pathlib import Path
from cognitive_compiler.router_observer import RouterObserver
from cognitive_compiler.meta_router_v2 import MetaRoutingResult, HarnessDecision, CognitiveTemperature
from cognitive_compiler.shared_cognitive_state import SharedCognitiveState


def _fake_result(primary="building", secondary=None, confidence=1.0, rerouted=False, temp_score=0.0):
    decision = HarnessDecision(primary=primary, secondary=secondary, confidence=confidence)
    decision.rerouted = rerouted
    return MetaRoutingResult(
        decision=decision,
        scs=SharedCognitiveState(problem_statement="q"),
        temperature=CognitiveTemperature(score=temp_score),
        rerouted=rerouted,
        elapsed_s=0.1,
    )


def test_record_routes_and_confidence():
    obs = RouterObserver(log_path="runtime/test_observer_unit.jsonl")
    rec = _fake_result()
    obs.record(rec, "q1")
    assert obs.buffer[-1].query == "q1"
    assert obs.buffer[-1].primary == "building"
    assert obs.buffer[-1].rerouted is False


def test_summarize_empty():
    obs = RouterObserver(log_path="runtime/test_observer_unit_empty.jsonl")
    assert obs.summarize() == {
        "count": 0.0,
        "rerouted_rate": 0.0,
        "hybrid_rate": 0.0,
        "avg_confidence": 0.0,
        "avg_primary_execution_time_s": 0.0,
        "avg_secondary_execution_time_s": 0.0,
        "primary_error_rate": 0.0,
        "secondary_error_rate": 0.0,
        "fallback_rate": 0.0,
    }


def test_summarize_hybrid_and_rerouted():
    obs = RouterObserver(log_path="runtime/test_observer_unit_metrics.jsonl")
    obs.record(_fake_result(primary="a"), "q1")
    obs.record(_fake_result(primary="b", secondary="a", confidence=0.75, rerouted=True, temp_score=0.2), "q2")
    obs.record(_fake_result(primary="c", secondary="b", confidence=0.9), "q3 rerouted")

    summary = obs.summarize(last_n=2)
    assert summary["count"] == 2
    assert summary["hybrid_rate"] == 1.0
    assert summary["rerouted_rate"] == 0.5
    assert 0.0 <= summary["avg_confidence"] <= 1.0


def test_jsonl_file_contains_expected_lines(tmp_path):
    log = tmp_path / "routing.jsonl"
    obs = RouterObserver(log_path=str(log))
    obs.record(_fake_result(primary="research", secondary="building", confidence=0.9, rerouted=True, temp_score=0.4), "query-x")
    lines = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert lines[-1]["query"] == "query-x"
    assert lines[-1]["primary"] == "research"
    assert lines[-1]["secondary"] == "building"
    assert lines[-1]["rerouted"] is True
    assert 0.0 <= lines[-1]["temperature_score"] <= 1.0
    assert lines[-1]["elapsed_s"] == 0.1

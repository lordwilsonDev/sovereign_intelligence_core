from __future__ import annotations

import types


def test_operational_telemetry_singleton_and_snapshot():
    from cognitive_compiler.operational_telemetry import OperationalTelemetry, HarnessMetrics
    t1 = OperationalTelemetry()
    t2 = OperationalTelemetry()
    assert t1 is t2
    assert t1.get_dashboard_snapshot() == {}
    t1.record(HarnessMetrics(harness_name="h", duration_ms=10.0, assumption_debt=1, falsification_theatricality_score=0.5, epistemic_diversity_index="Low", human_escalation_triggered=False, predictions_generated=1, predictions_tested=0, errors_corrected=0))
    snap = t1.get_dashboard_snapshot()
    assert snap["latest_harness"] == "h"
    assert snap["avg_assumption_debt"] == 1.0
    assert snap["total_errors_corrected"] == 0


def test_architecture_cicd_lifecycle():
    from cognitive_compiler.architecture_cicd import ArchitectureCICD
    prompts = {"template_a": "hello", "template_b": "world"}
    pipe = ArchitectureCICD(baseline_prompts=prompts)
    assert pipe.get_active_prompts() == prompts
    new_prompts = {"template_a": "hello2", "template_b": "world"}
    vid = pipe.propose_candidate(new_prompts, "change prompt")
    assert vid in pipe.versions
    pipe.start_canary(vid, traffic_percent=0.2)
    assert pipe.canary_version_id == vid
    pipe.record_test_result(vid, "bench_1", 0.85)
    assert not pipe.should_rollback(degradation_threshold=0.05)
    pipe.record_test_result(pipe.active_version_id, "bench_1", 0.95)
    assert pipe.should_rollback(degradation_threshold=0.05)
    pipe.resolve_canary("rollback")
    assert pipe.canary_version_id is None


def test_human_in_the_loop_escalation():
    from cognitive_compiler.human_in_the_loop import HumanInTheLoop
    hitl = HumanInTheLoop({
        "min_confidence_for_auto": 0.9,
        "max_assumption_debt_auto": 2,
        "require_human_domains": ["healthcare", "legal"],
    })
    should_escalate, reason = hitl.should_escalate({"updated_confidence": 0.4, "assumption_debt": 3, "predictions_tested": 0}, domain="healthcare")
    assert should_escalate is True
    report = hitl.generate_handoff({"updated_confidence": 0.4, "assumption_debt": 3, "summary": "Low confidence path"}, reason)
    d = report.to_dict()
    assert d["escalation_reason"]
    assert d["confidence"] == 0.4


def test_failure_mode_engine_detection():
    from cognitive_compiler.failure_mode_engine import FailureModeEngine
    engine = FailureModeEngine()
    hits = engine.detect({"loop_iterations": 9, "assumption_debt": 6, "fts": 0.82})
    ids = [m.get("id") for m in hits]
    assert "endless-inversion-loop" in ids
    assert "assumption-debt-overload" in ids
    assert "confident-hallucination-with-falsification" in ids

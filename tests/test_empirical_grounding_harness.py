from __future__ import annotations

from cognitive_compiler.empirical_grounding_harness_v1 import EmpiricalGroundingHarness


def test_empty_source_payload_returns_blocked_result():
    h = EmpiricalGroundingHarness()
    out = h.evaluate("ground this", {})
    assert out.ok is False
    assert out.event == "evaluated:empty"
    assert out.payload["assumption_debt"] == 0
    assert out.payload["fts"] == 1.0
    assert out.payload["escalation_triggered"] is True
    assert out.payload["updated_confidence"] == 0.0


def test_uses_present_predictions_and_calibrates_confidence():
    h = EmpiricalGroundingHarness(fts_block=0.95, assumption_debt_threshold=20)
    source = {
        "predictions": [
            {"statement": "p99 latency < 200ms", "status": "confirmed"},
            {"statement": "success rate >= 99%", "status": "untested"},
            {"statement": "error rate <= 0.1%", "status": "refuted"},
        ],
        "assumptions": [
            {"text": "cluster CPU headroom always available", "risk": "HIGH"},
        ],
        "confidence": 0.72,
    }
    out = h.evaluate("ground output", {"source_payload": source})
    assert out.payload["predictions_generated"] == 3
    assert out.payload["predictions_tested"] == 2
    assert out.payload["assumption_debt"] == 1
    assert out.payload["updated_confidence"] < 0.72


def test_assumption_debt_escalates_when_threshold_exceeded():
    h = EmpiricalGroundingHarness(assumption_debt_threshold=1)
    source = {
        "predictions": [],
        "assumptions": [
            {"text": "all users always have network", "risk": "HIGH"},
            {"text": "no message loss ever", "risk": "HIGH"},
        ],
    }
    out = h.evaluate("check assumptions", {"source_payload": source})
    assert out.payload["high_risk_untested"] >= 1
    assert out.payload["escalation_triggered"] is True

from __future__ import annotations

import unittest.mock

from cognitive_compiler.sac_self_audit import SacSelfAuditor, SacSelfAuditResult


def test_sac_self_audit_runs_without_error() -> None:
    auditor = SacSelfAuditor()
    result = auditor.run_audit()
    assert isinstance(result, SacSelfAuditResult)
    assert result.mirage_detected in (True, False)
    assert result.sas_confidence_weight in (0.5, 1.0)


def test_sac_self_audit_detects_mirage_when_metrics_degrade() -> None:
    auditor = SacSelfAuditor()

    fake_record = unittest.mock.Mock()
    fake_record.verdict = "mirage"
    fake_record.metric_deltas = {
        "latency_ms": {"before": 100.0, "after": 80.0, "delta": -20.0},
        "rnr_ratio": {"before": 0.40, "after": 0.38, "delta": -0.02},
    }

    def fake_run_cma(baseline):
        return fake_record

    auditor._run_cma = fake_run_cma
    result = auditor.run_audit()
    assert result.mirage_detected is True
    assert result.sas_confidence_weight == 0.5
    assert result.cma_verdict == "mirage"
    assert "latency_ms" in result.cma_details

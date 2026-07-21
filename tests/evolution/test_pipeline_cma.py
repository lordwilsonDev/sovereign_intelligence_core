"""Ouroboros Pipeline CMA tests."""

from __future__ import annotations

from pathlib import Path

from msb_v2.evolution.pipeline_cma import PipelineCMA


def test_pipeline_cma_counts_rollback_events(tmp_path: Path) -> None:
    audit = tmp_path / "audit.jsonl"
    audit.write_text(
        '{"type":"SOVEREIGN_ARTIFACT_REJECTED","artifact_id":"a1"}\n{"type":"SOVEREIGN_ROLLBACK","reason":"low-sas"}\n',
        encoding="utf-8",
    )
    cma = PipelineCMA(root=tmp_path, audit_log_path=audit)
    out = cma.scan()
    assert out["rejected_artifacts"] == 1
    assert out["mirage_alerts"] == 0


def test_pipeline_cma_counts_mirage_alerts(tmp_path: Path) -> None:
    audit = tmp_path / "audit.jsonl"
    audit.write_text(
        '{"type":"PIPELINE_MIRAGE_ALERT","note":"override"}\n{"type":"PIPELINE_MIRAGE_ALERT"}\n',
        encoding="utf-8",
    )
    cma = PipelineCMA(root=tmp_path, audit_log_path=audit)
    out = cma.scan()
    assert out["mirage_alerts"] == 2

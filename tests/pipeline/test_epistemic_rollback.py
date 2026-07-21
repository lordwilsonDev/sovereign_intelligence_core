"""Epistemic rollback tests."""

from __future__ import annotations

from pathlib import Path

from msb_v2.evolution.scanner import OuroborosScanner


def test_epistemic_rollback_logs_event(tmp_path: Path) -> None:
    audit_log = tmp_path / "audit.jsonl"
    scanner = OuroborosScanner(tmp_path)
    event = {
        "type": "SOVEREIGN_ROLLBACK",
        "reason": "test",
        "previous_image": "img-old",
        "current_image": "img-new",
        "pre_deployment_kg": str(tmp_path / "kg-pre.json"),
        "post_deployment_kg": str(tmp_path / "kg-post.json"),
    }
    with open(audit_log, "w", encoding="utf-8") as handle:
        handle.write(str(event) + "\n")
    events_post = scanner.scan()
    assert "hotspots" in events_post
    assert "duplication" in events_post
    assert "dead_symbols" in events_post

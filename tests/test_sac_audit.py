"""Test SacAuditLog persistence + recent retrieval."""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from msb_v2.audit.sac_audit import SacAuditEvent, get_audit_log, _DEFAULT_LOG


@pytest.fixture(autouse=True)
def _reset_audit_log(monkeypatch, tmp_path):
    path = tmp_path / "audit.jsonl"
    monkeypatch.setenv("MSB_SAC_AUDIT_PATH", str(path))
    import msb_v2.audit.sac_audit as mod
    monkeypatch.setattr(mod, "_DEFAULT_LOG", None)
    yield
    if path.exists():
        path.unlink()


def test_audit_log_append_and_recent():
    log = get_audit_log()
    log.append(SacAuditEvent(event_id="e1", kind="dispatch", actor="system", payload={"x": 1}))
    log.append(SacAuditEvent(event_id="e2", kind="result", actor="worker", payload={"x": 2}))
    recent = log.recent(10)
    assert len(recent) == 2
    assert recent[-1]["event_id"] == "e2"
    assert recent[0]["kind"] == "dispatch"

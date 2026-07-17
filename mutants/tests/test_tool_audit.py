from __future__ import annotations

from msb_v2.engine.tool_audit import ToolAudit


def test_tool_audit_records_call() -> None:
    audit = ToolAudit()
    entry = audit.record(tool="get_time", args_hash="abc", phase="observe")
    assert entry.allowed is True
    assert entry.blocked_reason == ""


def test_tool_audit_blocked_count_counts_only_blocked() -> None:
    audit = ToolAudit()
    audit.record(tool="safe", args_hash="h1", phase="observe", allowed=True)
    audit.record(tool="danger", args_hash="h2", phase="execute", allowed=False, blocked_reason="pattern")
    assert audit.recent()[-1]["tool"] == "danger"
    assert audit.blocked_count() == 1

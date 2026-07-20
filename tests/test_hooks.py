"""Explicit hook emission + HTTP surface test."""
from __future__ import annotations

import os


def test_hooks_emit_queued_event():
    from msb_v2.api.hooks import emit

    result = emit("dispatch", "task-1", {"foo": "bar"}, trace_id="trace-1")
    assert result["status"] == "queued"
    assert result["kind"] == "dispatch"
    assert result["subject"] == "task-1"

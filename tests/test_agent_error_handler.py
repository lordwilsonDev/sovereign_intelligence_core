from __future__ import annotations

import pytest

from msb_v2.agent.error_handler import ErrorDecision, analyze_error, generate_fix


def test_analyze_error_transient_retry() -> None:
    recovery = analyze_error({"tool": "web_search"}, "temporary timeout", attempt=1)
    assert recovery.decision == ErrorDecision.RETRY


def test_analyze_error_exhausted_replan() -> None:
    recovery = analyze_error({"tool": "web_search"}, "unknown failure", attempt=3)
    assert recovery.decision == ErrorDecision.REPLAN


def test_generate_fix_returns_noop_fallback() -> None:
    step = {"step": 1, "tool": "web_search", "description": "search", "critical": True}
    fix = generate_fix(step, "boom", "backup search")
    assert fix["tool"] == "noop"
    assert fix["step"] == 1
    assert fix["critical"] is True

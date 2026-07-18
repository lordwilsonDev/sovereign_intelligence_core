from __future__ import annotations

import pytest

from msb_v2.agent.error_handler import ErrorDecision, analyze_error, generate_fix


def test_analyze_error_timeout() -> None:
    d = analyze_error({"tool": "web_search"}, "Request timed out after 5s")
    assert d.decision in (ErrorDecision.RETRY, ErrorDecision.REPLAN, ErrorDecision.ABORT)


def test_analyze_error_rate_limit() -> None:
    d = analyze_error({"tool": "web_search"}, "HTTP 429 Too Many Requests")
    assert d.decision in (ErrorDecision.RETRY, ErrorDecision.REPLAN, ErrorDecision.ABORT)


def test_generate_fix_returns_string() -> None:
    result = generate_fix({"tool": "web_search"}, "timeout", "use alternative provider")
    assert isinstance(result, dict)
    assert "tool" in result

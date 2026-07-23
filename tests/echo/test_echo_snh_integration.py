"""Integration tests for Echo → SNH critical notification flow."""

from __future__ import annotations

from typing import Any, Dict
from unittest.mock import patch

import pytest

from msb_v2.echo.harness import EchoHarness


@pytest.fixture()
def harness() -> EchoHarness:
    return EchoHarness()


def _critical_payload() -> Dict[str, Any]:
    return {
        "intent": {
            "action": "shutdown",
            "is_destructive": True,
            "has_universal_quantifier": True,
            "specificity": 0.2,
            "target_criticality": 0.9,
            "is_reversible": False,
            "raw_text": "shut down everything",
            "targets": ["database"],
            "providers": [],
        },
        "blast_analysis": {
            "score": 0.95,
            "affected": 20,
            "stateful_at_risk": 5,
            "client_facing_at_risk": 10,
            "details": [
                {"name": "web-1", "critical": True, "stateful": True, "provider": "aws"},
                {"name": "worker-1", "critical": False, "stateful": False, "provider": "aws"},
                {"name": "job-1", "critical": False, "stateful": False, "type": "gpu", "provider": "gcp"},
            ],
        },
        "cognitive_state": {
            "fatigue": 0.8,
            "frustration": 0.1,
        },
    }


def _safe_payload() -> Dict[str, Any]:
    return {
        "intent": {
            "action": "query",
            "is_destructive": False,
            "has_universal_quantifier": False,
            "specificity": 0.9,
            "target_criticality": 0.1,
            "is_reversible": True,
            "raw_text": "how many workloads are running",
            "targets": ["workloads"],
            "providers": [],
        },
        "blast_analysis": {
            "score": 0.0,
            "affected": 0,
            "stateful_at_risk": 0,
            "details": [],
        },
        "cognitive_state": {
            "fatigue": 0.1,
            "frustration": 0.1,
        },
    }


def test_critical_echo_triggers_snh_notification(harness: EchoHarness) -> None:
    with patch.object(harness, "_notify_critical") as mock_notify:
        decision = harness.evaluate(_critical_payload())
        assert decision["should_echo"] is True
        assert decision["severity"] == "critical"
        mock_notify.assert_called_once()
        notified_payload = mock_notify.call_args[0][0]
        assert notified_payload["decision_id"]
        assert notified_payload["severity"] == "critical"


def test_non_critical_echo_does_not_trigger_snh(harness: EchoHarness) -> None:
    with patch.object(harness, "_notify_critical") as mock_notify:
        decision = harness.evaluate(_safe_payload())
        assert decision["should_echo"] is False
        mock_notify.assert_not_called()


def test_snh_failure_does_not_block_echo_decision(harness: EchoHarness) -> None:
    with patch("msb_v2.sn.engine.NotificationEngine", side_effect=RuntimeError("SNH down")):
        decision = harness.evaluate(_critical_payload())
        assert decision["should_echo"] is True
        assert decision["severity"] == "critical"
        assert len(decision["echo_message"]) > 0


def test_echo_decision_includes_alternatives(harness: EchoHarness) -> None:
    with patch("msb_v2.echo.harness.EchoHarness._notify_critical"):
        decision = harness.evaluate(_critical_payload())
        assert decision["should_echo"] is True
        assert len(decision["alternatives"]) > 0
        for alt in decision["alternatives"]:
            assert "description" in alt
            assert "affected" in alt
            assert "safe" in alt

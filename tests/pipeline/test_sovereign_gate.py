"""Sovereign Gate tests."""

from __future__ import annotations

from typing import Any

import pytest

from msb_v2.pipeline.sovereign_gate import GateDecision, SovereignGate


def test_gate_passes_good_artifact() -> None:
    gate = SovereignGate(threshold=80.0)
    decision = gate.evaluate({
        "artifact_id": "artifact-good",
        "sas": 90.0,
        "rnr": 0.9,
        "fts": 0.1,
        "sas_a": 90.0,
    })
    assert decision.verdict == "PASS"
    assert "reason" in decision.__dict__


def test_gate_rejects_low_sas_a() -> None:
    gate = SovereignGate(threshold=80.0)
    decision = gate.evaluate({
        "artifact_id": "artifact-bad",
        "sas": 70.0,
        "rnr": 0.7,
        "fts": 0.1,
        "sas_a": 70.0,
    })
    assert decision.verdict == "REJECT"
    assert decision.reason is not None


def test_gate_rejects_high_fts() -> None:
    gate = SovereignGate(threshold=80.0)
    decision = gate.evaluate({
        "artifact_id": "artifact-fts",
        "sas": 92.0,
        "rnr": 0.92,
        "fts": 0.6,
        "sas_a": 92.0,
    })
    assert decision.verdict == "REJECT"


def test_assess_returns_decision_keys() -> None:
    gate = SovereignGate(threshold=80.0)
    result = gate.assess("demo-image:latest")
    assert result["verdict"] in {"PASS", "REJECT"}
    assert "sas_a" in result
    assert "audit_receipt" in result


def test_evaluate_audit_chain_event() -> None:
    gate = SovereignGate(threshold=80.0)
    decision = gate.evaluate({
        "artifact_id": "artifact-evidence",
        "sas": 88.0,
        "rnr": 0.88,
        "fts": 0.12,
        "sas_a": 88.0,
    })
    assert decision.audit_receipt is None or isinstance(decision.audit_receipt, str)

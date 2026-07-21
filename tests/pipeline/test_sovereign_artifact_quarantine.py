"""Sovereign Artifact Quarantine Gate tests."""

from __future__ import annotations

from typing import Any

import pytest

from msb_v2.pipeline.sovereign_artifact_quarantine import (
    ProbeResult,
    SovereignArtifactQuarantine,
)


def test_container_artifact_classification() -> None:
    gate = SovereignArtifactQuarantine()
    result = gate.classify_artifact({"kind": "image", "name": "acme/app:v1"})
    assert result["type"] == "container"


def test_model_artifact_classification() -> None:
    gate = SovereignArtifactQuarantine()
    result = gate.classify_artifact({"source": "hf://acme/model", "kind": "weights"})
    assert result["type"] == "model"


def test_probe_results_accumulate() -> None:
    gate = SovereignArtifactQuarantine()
    artifact = {"id": "artifact-1", "kind": "image"}
    artifact_type = gate.classify_artifact(artifact)
    probe_results = gate.probe_artifact(artifact, artifact_type)
    assert len(probe_results) == len(gate._prompts) or len(probe_results) >= 1


def test_scoring_produces_sas_a() -> None:
    gate = SovereignArtifactQuarantine()
    probes = [ProbeResult(prompt_id="p1", response='{"content":"trust evidence","status":"ok"}', score=0.95)]
    scored = gate.score_artifact({"id": "a1", "kind": "image"}, probes)
    assert 0.0 <= scored.sas_a <= 100.0


def test_good_artifact_is_accepted() -> None:
    gate = SovereignArtifactQuarantine(threshold=80.0)
    probe_results = [ProbeResult(prompt_id="p1", response='{"content":"limits","status":"bounded_trust"}', score=0.92)]
    scored = gate.score_artifact({"id": "a-good", "kind": "image"}, probe_results)
    assert gate.is_artifact_acceptable(scored) is True


def test_bad_artifact_is_rejected() -> None:
    gate = SovereignArtifactQuarantine(threshold=50.0)
    gate.audit_chain = _FakeChain()
    artifact = {"id": "a-bad", "kind": "image", "name": "bad"}
    low_score = 0.0
    
    def fake_score(probe, response):
        return low_score
    
    import msb_v2.pipeline.sovereign_artifact_quarantine as mod
    original = mod.SovereignArtifactQuarantine._score_response
    mod.SovereignArtifactQuarantine._score_response = fake_score  # type: ignore[assignment]
    try:
        result = gate.run_quarantine(artifact)
    finally:
        mod.SovereignArtifactQuarantine._score_response = original  # type: ignore[assignment]
    assert result["verdict"] == "rejected"
    assert "audit_receipt" in result


def test_quarantine_returns_expected_keys() -> None:
    gate = SovereignArtifactQuarantine()
    result = gate.run_quarantine({"id": "artifact-ok", "kind": "generic", "name": "generic-artifact"})
    assert result["verdict"] in {"accepted", "rejected"}
    assert "artifact_id" in result
    assert "sas_a" in result
    assert "sas" in result
    assert "rnr" in result
    assert "fts" in result


class _FakeChain:
    def append(self, event):
        return "receipt-1"

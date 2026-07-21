"""Pipeline Integrity Token tamper-abort tests."""

from __future__ import annotations

import pytest

from msb_v2.pipeline.pit import PipelineIntegrityToken


def test_pit_fails_on_tampered_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    token = PipelineIntegrityToken()
    monkeypatch.setattr(token, "sign", lambda payload: "sig" if payload == "workflow-payload" else None)
    assert token.verify("workflow-payload", "sig") is True
    assert token.verify("workflow-payload-alt", "sig") is False


def test_pit_tampered_payload_rejects_even_if_guessed_signature(monkeypatch: pytest.MonkeyPatch) -> None:
    token = PipelineIntegrityToken()
    monkeypatch.setattr(token, "sign", lambda payload: "sig" if payload == "workflow-payload" else None)
    assert token.verify("tampered-workflow-payload", "sig") is False
    assert token.verify("tampered-workflow-payload", "fake-signature") is False


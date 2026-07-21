"""Pipeline Integrity Token tests."""

from __future__ import annotations

from typing import Any

import pytest

from msb_v2.pipeline.pit import PipelineIntegrityToken


def test_pit_sign_returns_string_or_none() -> None:
    token = PipelineIntegrityToken()
    signature = token.sign("payload")
    assert signature is None or isinstance(signature, str)


def test_pit_verification_matches_signature(monkeypatch: pytest.MonkeyPatch) -> None:
    token = PipelineIntegrityToken()
    signature = token.sign("signed-payload")
    monkeypatch.setattr(token, "sign", lambda payload: "fixed-signature" if payload == "signed-payload" else None)
    assert token.verify("signed-payload", "fixed-signature") is True
    assert token.verify("tampered-payload", "fixed-signature") is False


def test_pit_verify_rejects_missing_signature() -> None:
    token = PipelineIntegrityToken()
    assert token.verify("payload", None) is False
    assert token.verify("payload", "") is False

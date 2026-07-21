from __future__ import annotations

from typing import Any, Dict, List

import pytest

from msb_v2.api.deepseek import _provider, _sov_provider


class DummyResponse:
    def __init__(self, payload):
        self.payload = payload or {}

    def json(self):
        return self.payload


class FakeRequests:
    def __init__(self, response=None, exc=None):
        self.response = response
        self.exc = exc
        self.calls = 0

    def post(self, url, headers=None, json=None, timeout=None, **kwargs):
        self.calls += 1
        if self.exc:
            raise self.exc
        return self.response or DummyResponse({})


def test_sovereign_wrapper_initializes_when_enabled(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test")
    monkeypatch.setenv("DEEPSEEK_SOVEREIGN_WRAPPER", "1")
    monkeypatch.setenv("MSB_AUDIT_ROOT", str(tmp_path))

    import importlib
    import msb_v2.api.deepseek as deepseek_mod
    importlib.reload(deepseek_mod)

    assert deepseek_mod._sov_provider is not None
    assert isinstance(deepseek_mod._sov_provider.__dict__.get("provider"), type(deepseek_mod._provider))


def test_sovereign_wrapper_disabled_by_default(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test")
    monkeypatch.delenv("DEEPSEEK_SOVEREIGN_WRAPPER", raising=False)
    monkeypatch.setenv("MSB_AUDIT_ROOT", str(tmp_path))

    import importlib
    import msb_v2.api.deepseek as deepseek_mod
    importlib.reload(deepseek_mod)

    assert deepseek_mod._sov_provider is None

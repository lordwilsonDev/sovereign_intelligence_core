from __future__ import annotations

from typing import Any, Dict, List

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.deepseek import _provider, _sov_provider


def test_sovereign_wrapper_initializes_when_enabled(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test")
    monkeypatch.setenv("MSB_SOVEREIGN_PROVIDER", "1")
    monkeypatch.setenv("MSB_AUDIT_ROOT", str(tmp_path))

    import importlib
    import msb_v2.api.deepseek as deepseek_mod
    importlib.reload(deepseek_mod)

    assert deepseek_mod._sov_provider is not None
    assert isinstance(deepseek_mod._sov_provider.__dict__.get("provider"), type(deepseek_mod._provider))


def test_sovereign_wrapper_disabled_by_default(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test")
    monkeypatch.delenv("MSB_SOVEREIGN_PROVIDER", raising=False)
    monkeypatch.setenv("MSB_AUDIT_ROOT", str(tmp_path))

    import importlib
    import msb_v2.api.deepseek as deepseek_mod
    importlib.reload(deepseek_mod)

    assert deepseek_mod._sov_provider is None


def test_chat_uses_wrapper_when_enabled(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test")
    monkeypatch.setenv("MSB_SOVEREIGN_PROVIDER", "1")
    monkeypatch.setenv("MSB_AUDIT_ROOT", str(tmp_path))

    import msb_v2.api.deepseek as deepseek_mod
    import importlib

    def fake_wrapper(provider):
        class Wrapper:
            def __init__(self, inner):
                self.provider = inner
                self.source_label = "test"
                self.provider_trusted = True
                self._veto_count = 0
                self._coherence_sum = 0.0
                self._coherence_samples = 0
            def chat(self, messages, max_tokens=256, **kwargs):
                result = self.provider.chat(messages, max_tokens=max_tokens, **kwargs)
                return {**result, "provider_metadata": {"risk": "LOW", "coherence": 1.0, "provider_trusted": True}}
        return Wrapper(provider)

    monkeypatch.setattr(deepseek_mod, "SovereignProviderWrapper", fake_wrapper)
    importlib.reload(deepseek_mod)

    client = TestClient(deepseek_mod.router)
    response = client.post("/chat", json={"messages": [{"role": "user", "content": "ping"}]}, headers={"Authorization": "Bearer test"})
    body = response.json()
    assert response.status_code == 200
    assert "provider_metadata" in body
    assert body["provider_metadata"]["risk"] == "LOW"

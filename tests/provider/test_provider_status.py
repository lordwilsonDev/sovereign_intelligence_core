from __future__ import annotations

from typing import Any, Dict

import pytest

from msb_v2.api.middleware import set_local_bypass
from msb_v2.provider.sovereign_provider import SovereignProviderWrapper, ProviderStatus


class DummyProvider:
    def chat(self, messages, max_tokens=256, **kwargs):
        return {"role": "assistant", "content": "ok", "model": "dummy", "latency_ms": 1.0, "tokens": {}}


def test_deepseek_provider_status_when_wrapper_disabled() -> None:
    set_local_bypass(True)
    try:
        from msb_v2.api.web import create_app
        from fastapi.testclient import TestClient

        app = create_app()
        client = TestClient(app)
        response = client.get("/deepseek/provider/status")
        assert response.status_code == 200
        body = response.json()
        assert body.get("provider") == "deepseek-legacy"
        assert body.get("msb_sov_provider") is False
    finally:
        set_local_bypass(None)


def test_deepseek_provider_status_when_wrapper_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    from msb_v2.api.deepseek import _provider

    wrapper = SovereignProviderWrapper(_provider, source_label="test")
    monkeypatch.setattr("msb_v2.api.deepseek._sov_provider", wrapper)
    set_local_bypass(True)
    try:
        from msb_v2.api.web import create_app
        from fastapi.testclient import TestClient

        app = create_app()
        client = TestClient(app)
        response = client.get("/deepseek/provider/status")
        assert response.status_code == 200
        body = response.json()
        assert body["source_label"] == "test"
        assert "veto_count" in body
        assert "coherence_avg" in body
        assert "sovereignty_score" in body
        assert body["jitter_min_ms"] == 5.0
        assert body["jitter_max_ms"] == 50.0
    finally:
        set_local_bypass(None)

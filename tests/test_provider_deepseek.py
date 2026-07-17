from __future__ import annotations

from typing import Any

import json

import pytest

from msb_v2.provider.deepseek import DeepSeekProvider


def test_returns_none_when_api_key_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("DEEPSEEK_API_KEY_DIRECT", raising=False)
    provider = DeepSeekProvider()
    result = provider.chat([{"role": "user", "content": "ping"}])
    assert result is None


def test_plan_reports_missing_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("DEEPSEEK_API_KEY_DIRECT", raising=False)
    provider = DeepSeekProvider()
    result = provider.plan("ping")
    assert result["status"] == "error"
    assert result["confidence"] == 0.0


def test_chat_parses_json_response(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test")

    class _FakeResp:
        def read(self) -> bytes:
            return json.dumps({
                "id": "test",
                "model": "deepseek-chat",
                "choices": [
                    {"message": {"role": "assistant", "content": "pong"}}
                ],
            }).encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, *args: Any, **kwargs: Any) -> None:
            pass

    import urllib.request as _urllib_request
    monkeypatch.setattr(_urllib_request, "urlopen", lambda req, timeout=None: _FakeResp(), raising=False)
    provider = DeepSeekProvider()
    result = provider.chat([{"role": "user", "content": "ping"}])
    assert result is not None
    assert result["content"] == "pong"
    assert result["model"] == "deepseek-chat"

"""SAC quarantine enforcement for sovereign local inference."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from msb_v2.local_ai.client import LocalInferenceClient
from msb_v2.local_ai.inference_engine import InferenceEngine


@pytest.mark.parametrize(
    "blocked_token",
    ["http://", "https://"],
)
def test_inference_engine_rejects_external_url_tokens(blocked_token: str) -> None:
    engine = InferenceEngine(base_url="http://127.0.0.1:11434")
    prompt = f"Summarize this page: {blocked_token}example.com"
    with pytest.raises(ValueError, match="Prompt rejected by quarantine"):
        engine.generate(model_id="qwen2.5:0.5b", prompt=prompt)


def test_inference_engine_rejects_excessive_length() -> None:
    engine = InferenceEngine(base_url="http://127.0.0.1:11434")
    prompt = "a" * (500_000 + 1)
    with pytest.raises(ValueError, match="excessive length"):
        engine.generate(model_id="qwen2.5:0.5b", prompt=prompt)


def test_inference_engine_local_only_prompt_passes_quarantine() -> None:
    engine = InferenceEngine(base_url="http://127.0.0.1:11434")
    prompt = "Explain sovereign inference in one sentence."
    fake_body = b'{"model":"qwen2.5:0.5b","created_at":"2026-07-23T00:00:00Z","response":"local sovereign output.","done":true}'
    fake_ctx = MagicMock()
    fake_ctx.__enter__ = lambda self: self
    fake_ctx.__exit__ = lambda self, *exc: False
    fake_ctx.read = lambda *args, **kwargs: fake_body
    with patch("msb_v2.local_ai.inference_engine.urllib.request.urlopen", return_value=fake_ctx):
        result = engine.generate(model_id="qwen2.5:0.5b", prompt=prompt)
    assert result.text == "local sovereign output."
    assert result.backend == "ollama"
    assert result.model == "qwen2.5:0.5b"


def test_local_inference_client_local_only_prompt_path() -> None:
    client = LocalInferenceClient(base_url="http://test", model="test-model")
    with patch("requests.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.return_value = {"text": "ok"}
        mock_post.return_value = mock_resp
        text = client.generate("sovereign local prompt")
    assert text == "ok"

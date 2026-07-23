"""Tests for the shared LocalInferenceClient."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from msb_v2.local_ai.client import LocalInferenceClient


def test_client_generate_calls_local_ai() -> None:
    client = LocalInferenceClient(base_url="http://test", model="test-model")
    with patch("requests.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.return_value = {"response": "hello"}
        mock_post.return_value = mock_resp

        result = client.generate("test prompt")
        assert result == "hello"
        mock_post.assert_called_once()


def test_client_handles_error_gracefully() -> None:
    client = LocalInferenceClient(base_url="http://test", model="test-model")
    with patch("requests.post", side_effect=Exception("Connection refused")):
        result = client.generate("test prompt")
        assert "unreachable" in result.lower()


def test_client_prefers_text_fallback_keys() -> None:
    client = LocalInferenceClient(base_url="http://test", model="test-model")
    with patch("requests.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.return_value = {"generated_text": "fallback"}
        mock_post.return_value = mock_resp

        result = client.generate("test prompt")
        assert result == "fallback"


def test_client_returns_raw_json_when_no_text_key() -> None:
    client = LocalInferenceClient(base_url="http://test", model="test-model")
    with patch("requests.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.return_value = {"unexpected": 1}
        mock_post.return_value = mock_resp

        result = client.generate("test prompt")
        assert "1" in result

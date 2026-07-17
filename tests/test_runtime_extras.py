from __future__ import annotations

import logging

import pytest

from msb_v2.runtime.logging import configure_logging, get_logger
from msb_v2.runtime.secrets import SecretsLoader


def test_configure_logging_is_idempotent() -> None:
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.WARNING)

    configure_logging("info")
    configure_logging("debug")
    assert root.level == logging.INFO
    assert len(root.handlers) == 1


def test_get_logger_returns_named_logger() -> None:
    configure_logging()
    logger = get_logger("tests")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "tests"


def test_secrets_loader_loads_prefixed_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MSB_SECRET_API_KEY", "abc123")
    loader = SecretsLoader()
    secrets = loader.load_env()
    assert "api_key" in secrets
    assert secrets["api_key"].value == "abc123"


def test_secrets_loader_get_default() -> None:
    loader = SecretsLoader()
    secret = loader.get("missing", default="fallback")
    assert secret.value == "fallback"

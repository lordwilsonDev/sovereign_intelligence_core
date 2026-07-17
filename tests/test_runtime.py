from __future__ import annotations


import pytest

from msb_v2.runtime.config import RuntimeConfig
from msb_v2.runtime.version_registry import VersionRegistry


def test_runtime_config_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MSB_REASONING_SCORER", raising=False)
    cfg = RuntimeConfig()
    assert cfg.app_name == "msb-v2"
    assert cfg.port == 8766
    assert cfg.log_level == "info"
    assert cfg.reasoning_scorer is False


def test_runtime_config_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MSB_PORT", "9000")
    monkeypatch.setenv("MSB_REASONING_SCORER", "1")
    cfg = RuntimeConfig()
    assert cfg.port == 9000
    assert cfg.reasoning_scorer is True


def test_version_registry_register_and_get() -> None:
    registry = VersionRegistry()
    registry.register("api", "0.2.0", sha="abc123", since="2026-07-16")
    record = registry.get("api")
    assert record is not None
    assert record.version == "0.2.0"
    assert record.sha == "abc123"
    assert len(registry.all()) == 1

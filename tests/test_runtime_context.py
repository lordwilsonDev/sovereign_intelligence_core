from __future__ import annotations

import pytest

from msb_v2.runtime.context import RuntimeContext
from msb_v2.runtime.version_registry import VersionRegistry


def test_runtime_context_builds_defaults() -> None:
    ctx = RuntimeContext()
    assert ctx.config.app_name == "msb-v2"
    assert ctx.config.port == 8766
    assert isinstance(ctx.events.__class__, type)
    assert isinstance(ctx.versions, VersionRegistry)


def test_runtime_context_accepts_config(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MSB_PORT", "9000")
    monkeypatch.setenv("MSB_REASONING_SCORER", "0")
    from msb_v2.runtime.config import RuntimeConfig

    cfg = RuntimeConfig()
    ctx = RuntimeContext(config=cfg)
    assert ctx.config.port == 9000
    assert ctx.config.reasoning_scorer is False

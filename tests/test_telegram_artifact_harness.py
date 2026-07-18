from __future__ import annotations

import importlib
from pathlib import Path

import pytest


def test_evaluate_creates_local_registry(tmp_path):
    import cognitive_compiler.telegram_artifact_harness_v1 as mod
    importlib.reload(mod)
    h = mod.TelegramArtifactHarness(artifact_dir=tmp_path)
    out = h.evaluate("make a sales widget", {"artifact_html": "<html>A</html>", "artifact_title": "Sales", "artifact_kind": "html"})
    assert out.ok is True
    assert out.event == "delivered"
    assert out.payload["id"]
    assert out.payload["status"] == "delivered"
    assert (tmp_path / f"{out.payload['id']}.html").exists() is True

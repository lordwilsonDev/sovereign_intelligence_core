from __future__ import annotations

from typing import Any, Dict

from msb_v2.aura.eve_tools import refresh_manifest


FIXTURE_ROOT = "/Users/lordwilson/msb-v2/tests/fixtures/eve_agent"


def test_refresh_manifest_returns_counts() -> None:
    payload: Dict[str, Any] = refresh_manifest(root=FIXTURE_ROOT)
    assert payload["status"] == "ok"
    assert payload["manifest"]["kind"] == "msb-eve-compiled-manifest"
    assert payload["manifest"]["version"] == 1
    assert payload["manifest"]["tool_count"] >= 1

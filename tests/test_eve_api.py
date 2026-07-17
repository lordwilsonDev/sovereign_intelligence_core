from __future__ import annotations

from pathlib import Path
from typing import Any, Dict


from msb_v2.api.eve import eve_manifest

FIXTURE_ROOT = Path("/Users/lordwilson/msb-v2/tests/fixtures/eve_agent")


def test_eve_manifest_returns_compiled_manifest() -> None:
    payload: Dict[str, Any] = eve_manifest(root=str(FIXTURE_ROOT))
    assert payload["kind"] == "msb-eve-compiled-manifest"
    assert payload["version"] == 1
    assert len(payload["tools"]) >= 1
    assert payload["tools"][0]["name"] == "get_time"
    assert payload["skills"][0]["name"] == "sovereign"
    assert payload["schedules"][0]["name"] == "morning_check"
    assert payload["skills"][0]["sha256"]
    assert payload["schedules"][0]["sha256"]

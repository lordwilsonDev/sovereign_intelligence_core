from __future__ import annotations

from pathlib import Path

from msb_v2.api.eve_schedules import eve_schedules

FIXTURE_ROOT = Path("/Users/lordwilson/msb-v2/tests/fixtures/eve_agent")


def test_eve_schedules_returns_schedule_entries() -> None:
    entries = eve_schedules(root=str(FIXTURE_ROOT))
    names = [entry["name"] for entry in entries]
    assert "morning_check" in names
    assert entries[0]["sha256"]

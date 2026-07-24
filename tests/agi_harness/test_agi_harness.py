"""AGI Harness tests."""
from __future__ import annotations

from unittest.mock import patch

import pytest

from msb_v2.agi_harness.engine import AGIHarness


@pytest.fixture()
def harness():
    return AGIHarness(base_url="http://testserver")


def test_cycle_returns_status(harness: AGIHarness) -> None:
    with patch("msb_v2.agi_harness.engine.requests.get") as mock_get, \
         patch("msb_v2.agi_harness.engine.requests.post") as mock_post, \
         patch("msb_v2.agi_harness.engine.emit_thought"):
        mock_get.return_value.ok = False
        mock_post.return_value.ok = False
        result = harness.cycle()
    assert "cycle_id" in result
    assert "observations" in result
    assert "actions" in result


def test_status_returns_running_flag() -> None:
    harness = AGIHarness()
    assert harness.running is False

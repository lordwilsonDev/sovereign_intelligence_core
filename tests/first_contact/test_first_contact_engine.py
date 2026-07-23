"""First Contact engine tests."""

from __future__ import annotations

import pytest

from msb_v2.first_contact.engine import FirstContactEngine, FirstContactSession


@pytest.fixture()
def engine() -> FirstContactEngine:
    return FirstContactEngine()


def test_start_creates_session(engine: FirstContactEngine) -> None:
    session = engine.start()
    assert session["session_id"]
    assert session["current_step"] == "welcome"
    assert session["completed"] is False


def test_advance_records_assumption(engine: FirstContactEngine) -> None:
    session = engine.start()
    advanced = engine.advance(session["session_id"], {"step": "assumption", "text": "AI cannot reason"})
    assert advanced["participant_assumption"] == "AI cannot reason"
    assert advanced["current_step"] == "invert"


def test_advance_records_inversion(engine: FirstContactEngine) -> None:
    session = engine.start()
    engine.advance(session["session_id"], {"step": "assumption", "text": "AI cannot reason"})
    advanced = engine.advance(session["session_id"], {"step": "invert", "text": "AI might reason"})
    assert any(p["inverted"] == "" and p["text"] == "AI might reason" for p in advanced["proposals"])


def test_advance_records_reveal(engine: FirstContactEngine) -> None:
    session = engine.start()
    engine.advance(session["session_id"], {"step": "assumption", "text": "AI cannot reason"})
    engine.advance(session["session_id"], {"step": "invert", "text": "AI might reason"})
    advanced = engine.advance(session["session_id"], {"step": "reveal", "text": "maybe I assumed too quickly"})
    assert advanced["revealed_assumption"] == "maybe I assumed too quickly"
    assert advanced["completed"] is True

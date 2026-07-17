from __future__ import annotations

from pathlib import Path

from msb_v2.aura.persistence import Persistence


def test_persistence_offline_replay_empty_when_no_file() -> None:
    persistence = Persistence(":memory:")
    assert persistence.replay_offline() == []


def test_persistence_replay_round_trip(tmp_path: Path) -> None:
    db_path = str(tmp_path / "events.sqlite")
    persistence = Persistence(db_path)
    record = {"type": "event", "payload": {"event_id": "e1"}}
    persistence._enqueue_replay(record)
    replay_path = persistence._replay_path
    assert replay_path.exists()
    loaded = persistence.replay_offline()
    assert loaded == [record]

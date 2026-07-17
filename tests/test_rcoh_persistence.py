from msb_v2.engine.rcoh_persistence import RCOHPersistence
from msb_v2.engine.rcoh import RCOHState, Phase
import tempfile
import os


def test_persistence_roundtrip():
    fd, path = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    store = RCOHPersistence(path)
    state = RCOHState(cycle_id="r1", current_phase=Phase.CONFIDENCE, confidence=0.84)
    store.save(state)
    loaded = store.load("r1")
    assert loaded is not None
    assert loaded.current_phase == Phase.CONFIDENCE
    assert loaded.confidence == 0.84
    recent = store.recent(5)
    assert len(recent) == 1
    assert recent[0]["cycle_id"] == "r1"

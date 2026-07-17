from __future__ import annotations

from msb_v2.engine.learning_fingerprint import LearningFingerprint


def test_learning_fingerprint_records_novel_pairs() -> None:
    fingerprint = LearningFingerprint()
    assert fingerprint.is_novel("ship service", "local-only") is True
    fingerprint.record("ship service", "local-only")
    assert fingerprint.is_novel("ship service", "local-only") is False
    assert fingerprint.is_novel("ship service", "cloud-backup") is True


def test_learning_fingerprint_history_blocking_duplicates() -> None:
    fingerprint = LearningFingerprint()
    fingerprint.record("alpha", "hypothesis-a")
    fingerprint.record("alpha", "hypothesis-a")
    assert len(fingerprint.history) == 1

from __future__ import annotations

from msb_v2.engine.priority_decay import PriorityDecay, PriorityScore


def test_composite_score_weights() -> None:
    score = PriorityScore(label="urgent", urgency=1.0, impact=0.0, confidence=0.0)
    assert abs(score.composite() - 0.4) < 1e-9


def test_priority_decay_ranks_highest_first() -> None:
    decay = PriorityDecay()
    decay.add(PriorityScore(label="low", urgency=0.1, impact=0.1, confidence=0.1))
    decay.add(PriorityScore(label="high", urgency=1.0, impact=1.0, confidence=1.0))
    ranked = decay.ranked()
    assert ranked[0][0] == "high"
    assert ranked[-1][0] == "low"

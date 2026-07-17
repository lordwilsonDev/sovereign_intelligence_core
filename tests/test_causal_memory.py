from __future__ import annotations

from msb_v2.engine.causal_memory import CausalMemory


def test_causal_memory_links_are_stored() -> None:
    memory = CausalMemory()
    memory.link("receipt", "bag", "produced")
    assert memory.has_link("receipt", "bag") is True
    assert memory.has_link("bag", "receipt") is False


def test_causal_memory_reasons_returns_directed_edges() -> None:
    memory = CausalMemory()
    memory.link("soil", "tree", "nourishes")
    memory.link("rain", "tree", "waters")
    reasons = memory.reasons_for("tree")
    assert len(reasons) == 2
    assert any("nourishes" in reason for reason in reasons)

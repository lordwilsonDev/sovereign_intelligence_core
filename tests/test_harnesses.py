from cognitive_compiler.building_harness_v1 import BuildingHarness
from cognitive_compiler.research_harness_v1 import ResearchHarness


def test_building_harness_returns_output():
    bh = BuildingHarness()
    out = bh.execute("Design a fault-tolerant event bus")
    assert out["goal"] == "Design a fault-tolerant event bus"
    assert out["plan"]["confidence"] >= 0.0
    assert len(out["requirements"]) >= 1


def test_research_harness_returns_output():
    rh = ResearchHarness()
    out = rh.execute("Literature review on causal inference")
    assert out["question"] == "Literature review on causal inference"
    assert len(out["evidence"]) >= 1
    assert len(out["hypotheses"]) >= 1

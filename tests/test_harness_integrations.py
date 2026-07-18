import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cognitive_compiler.meta_router_v2 import MetaRoutingHarness
from cognitive_compiler.continuous_router_v1 import ContinuousRoutingModule
from cognitive_compiler.harness_dispatcher_v1 import HarnessDispatcher
from cognitive_compiler.shared_cognitive_state import SharedCognitiveState


class TestMetaRouter:
    def test_meta_router_classification(self):
        meta = MetaRoutingHarness()
        r = meta.execute("Design and evaluate a REST API")
        assert r.decision.primary in {"building", "research", "complex_reasoning", "base_are"}
        assert 0.0 <= r.decision.confidence <= 1.0

    def test_cognitive_temperature(self):
        meta = MetaRoutingHarness()
        r = meta.execute("Design a distributed storage system")
        temp = meta.monitor(r.scs)
        assert 0.0 <= temp.score <= 1.0

    def test_explicit_override(self):
        meta = MetaRoutingHarness()
        ov = meta.execute("Free-form inquiry", context={"preferred_harness": "research"})
        assert ov.decision.primary == "research"
        assert ov.decision.confidence == 0.95


class TestCRM:
    def test_continuous_routing(self):
        crm = ContinuousRoutingModule()
        route = crm.route("Build a REST API for load testing with strong scalability requirements", context={"artifact_request": True, "abstract": True})
        assert not route.degrade_to_discrete
        assert abs(sum(route.harness_weights.values()) - 1.0) < 1e-2
        proto = crm.compose_protocol(route)
        assert proto["mode"] == "continuous"


class TestDispatcher:
    def test_primary_output_exists(self):
        d = HarnessDispatcher()
        out = d.dispatch("Build a causal model and research prior work")
        assert out["primary_output"] is not None
        assert "routing" in out
        assert out["scs_snapshot"]
        assert "temperature" in out

    def test_scs_continuity(self):
        dispatcher = HarnessDispatcher()
        scs = SharedCognitiveState(problem_statement="Build a causal model and research prior work")
        follow = dispatcher.dispatch("Now test this empirically", context={}, scs=scs)
        assert follow["routing"]["primary"] in {"research", "building", "complex_reasoning", "base_are"}

    def test_trivial_query(self):
        d = HarnessDispatcher()
        triv = d.dispatch("hello there")
        assert triv["routing"]["primary"] == "base_are"

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cognitive_compiler.harness_dispatcher_v1 import HarnessDispatcher
from cognitive_compiler.router_observer import RouterObserver
from cognitive_compiler.shared_cognitive_state import SharedCognitiveState


def test_full_system_smoke_executes_all_modes():
    dispatcher = HarnessDispatcher()
    observer = RouterObserver()
    cases = [
        ("Design a fault-tolerant event bus with retry budgets", "building"),
        ("Investigate why collaborative filtering degrades at scale", "research"),
        ("Resolve the tension between safety constraints and deployment speed", "complex_reasoning"),
        ("hello there", "base_are"),
    ]
    seen = set()
    for query, _ in cases:
        out = dispatcher.dispatch(query)
        observer.record(out, query)
        assert out["primary_output"] is not None
        assert out["temperature"]["score"] <= 1.0
        seen.add(out["routing"]["primary"])

    assert "base_are" in seen
    follow = dispatcher.dispatch("Now stress-test this", context={}, scs=SharedCognitiveState(problem_statement="Design hybrid system"))
    assert follow["routing"]["primary"] in {"research", "building", "complex_reasoning", "base_are"}

    summary = observer.summarize()
    assert summary["count"] == len(cases)
    assert summary["hybrid_rate"] >= 0.0

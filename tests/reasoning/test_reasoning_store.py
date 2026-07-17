from __future__ import annotations

from msb_v2.reasoning.store import ReasoningStore
from msb_v2.reasoning.types import (
    JustificationKind,
    ReasoningStatus,
    ReasoningStep,
    ReasoningTrace,
)


def _make_trace(trace_id="id-1", decision_id=None, memory_ids=(), conclusion="stop", status: ReasoningStatus | None = None):
    return ReasoningTrace(
        trace_id=trace_id,
        title="t",
        status=status or ReasoningStatus.COMPLETED,
        steps=(
            ReasoningStep(step_index=0, claim="x", evidence_refs=(), confidence=1.0, metadata={"kind": JustificationKind.HEURISTIC}),
        ),
        decision_id=decision_id,
        memory_ids=memory_ids,
        conclusion=conclusion,
    )


def test_add_and_get_trace():
    store = ReasoningStore()
    t = store.add_trace(_make_trace("t1", "d1", ("m1", "m2")))
    assert t.conclusion == "stop"
    assert store.get_trace("t1").decision_id == "d1"


def test_duplicate_trace_rejected():
    store = ReasoningStore()
    store.add_trace(_make_trace("t1"))
    try:
        store.add_trace(_make_trace("t1"))
        assert False, "expected duplicate error"
    except KeyError:
        pass


def test_list_filter_status():
    store = ReasoningStore()
    store.add_trace(_make_trace("t1"))
    store.add_trace(_make_trace("t2", conclusion="stop", status=ReasoningStatus.ACTIVE))
    assert [i.trace_id for i in store.list_traces()] == ["t1", "t2"]
    assert [i.trace_id for i in store.list_traces(ReasoningStatus.ACTIVE)] == ["t2"]


def test_set_status_and_backfill():
    store = ReasoningStore()
    store.add_trace(_make_trace("t1"))
    updated = store.set_status("t1", ReasoningStatus.ACTIVE)
    assert updated.status is ReasoningStatus.ACTIVE

    updated = store.backfill_decision("t1", "d99")
    assert updated.decision_id == "d99"
    again = store.backfill_decision("t1", "d99")
    assert again.decision_id == "d99"


def test_refs_propagation():
    store = ReasoningStore()
    store.add_trace(_make_trace("t1", "dec-1", ("mem-a", "mem-b")))
    dec_refs = store.refs_for("dec-1")
    assert len(dec_refs) == 1
    assert dec_refs[0].trace_id == "t1"
    for mem in ("mem-a", "mem-b"):
        assert any(r.memory_ids == (mem,) for r in store.refs_for(mem))


def test_trace_requires_steps():
    store = ReasoningStore()
    bad = ReasoningTrace(
        trace_id="missing",
        title="bad",
        steps=(),
        status=ReasoningStatus.DRAFT,
    )
    try:
        store.add_trace(bad)
        assert False, "expected no-steps validation"
    except ValueError:
        pass


def test_health_emitting():
    store = ReasoningStore()
    [store.add_trace(_make_trace("n1", status=ReasoningStatus.COMPLETED)) for _ in range(1)]
    [store.add_trace(_make_trace("n2", status=ReasoningStatus.CONTRADICTED)) for _ in range(1)]
    assert len(store.list_traces()) == 2
    assert len(store.refs_for("d-none")) == 0
    assert store.get_trace("n1").title == "t"
    assert store.get_trace("n2").status is ReasoningStatus.CONTRADICTED

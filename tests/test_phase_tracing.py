from __future__ import annotations

from msb_v2.engine.phase_tracing import PhaseTracer


def test_phase_tracer_records_span() -> None:
    tracer = PhaseTracer()
    span = tracer.begin("observe", task_id="t1")
    tracer.end(span, result="ok")
    exported = tracer.export()
    assert exported[0]["phase"] == "observe"
    assert exported[0]["result"] == "ok"
    assert exported[0]["duration_ms"] >= 0.0


def test_phase_tracer_metadata_carry_through() -> None:
    tracer = PhaseTracer()
    span = tracer.begin("evidence", batch_id="b9", mode="fast")
    tracer.end(span, result="failed", evidence_count=2)
    payload = tracer.export()[0]
    assert payload["metadata"]["batch_id"] == "b9"
    assert payload["metadata"]["mode"] == "fast"
    assert payload["evidence_count"] == 2

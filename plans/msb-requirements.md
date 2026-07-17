# MSB v2.0 — Requirements & Architecture Notes

## 1. Observability Gaps (Current State)

This section tracks known observability gaps. A gap is **resolved** when a test or live endpoint proves the missing behavior is actually implemented, not just planned.

### 1.1 Trace Provenance Verification
- **Original gap:** Traces were stored alongside execution, not derived from it. There was no way to prove a trace represented the actual sequence of atomic actions in an event log.
- **Resolution:** `msb_v2/reasoning/integrity.py:EventStreamStore` now implements an append-only event stream. Each `ExecutionEvent` carries `previous_hash` and `integrity_hash`, forming a hash chain. Traces are constructed by reading from this event stream.
- **Verification endpoint:** `GET /trace/verify/{decision_id}` recomputes the hash chain for the underlying events and returns `{"valid": bool, "broken_at": Optional[str], "expected_hash": ..., "actual_hash": ...}`.
- **Status:** RESOLVED.
- **Evidence:** live on `http://127.0.0.1:8766`; see `WIREUP.md` and `/observability/console` for runtime proof.

## 2. Live Endpoints (8766)

- `/health`
- `/reasoning/traces`
- `/reasoning/traces/{trace_id}`
- `/reasoning/traces/{trace_id}/status`
- `/reasoning/traces/{trace_id}/decision`
- `/reasoning/refs/dec-{decision_id}`
- `/reasoning/integrity/events`
- `/reasoning/integrity/trace/{trace_id}`
- `/reasoning/integrity/trace/verify/{decision_id}`
- `/reasoning/counterfactual/branch`
- `/reasoning/counterfactual/scan`
- `/reasoning/drift/{trace_id}`
- `/observability/metrics`
- `/observability/dashboard`
- `/observability/console`
- `/demo/query`
- `/demo/query-adk`

## 3. Test Status

Run from `msb-v2` root:
```bash
PYTHONPATH=/Users/lordwilson/msb-v2 python -m pytest tests/ -q
```

Current baseline: **162 passed**, 0 failed.

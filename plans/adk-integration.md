# ADK-Python Integration Plan — Daedalus Stack

## Current Reality

- Local clone at `/Users/lordwilson/adk-python/` with ADK 2.0 code
- ADK `Event` model exists but is not a drop-in replacement for our `ExecutionEvent`
- ADK provides higher-value building blocks elsewhere: `Agent`, `Runner`, workflow graph, tasks, tools, session/memory services, evaluation, telemetry

## What We Already Confirmed

- ADK imports work under `PYTHONPATH=/Users/lordwilson/adk-python/src:/Users/lordwilson/msb-v2`
- Our existing scorer/counterfactual/demo endpoints run clean on 8766
- Test suite is green at 162 tests

## Revised Pragmatic Integration

### Phase 1 — Runner/Agent Thin Adapter
- Add `msb_v2/adk/agent_adapter.py` wrapping our reasoning orchestrator in ADK `Agent`+`Runner` semantics
- Keep `/deepseek/chat`, `/cognitive`, `/moie/slug` endpoints stable
- Use ADK tools abstraction for provider/model routing

### Phase 2 — Memory/Session Bridging
- Replace inner store with ADK `SessionService` + `MemoryService` interfaces
- Keep FastAPI endpoints unchanged; benefit is pluggable backend

### Phase 3 — Evaluation Hookup
- Route `/deepseek/score` ground-truth events into ADK `Evaluator`
- Give MSB offline regression harness without rewriting scorer logic

## Out of Scope
- Rewriting `ExecutionEvent` to ADK `Event`; too much schema churn for too little gain
- Full fork maintenance; use vendored dependency or pyproject override

## Next Artifact
Phase 1 adapter: one ADK `Agent` that executes our existing demo reasoning and loads ADK tools without breaking endpoints.


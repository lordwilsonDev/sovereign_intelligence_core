# VY-NEXUS 24h Loop Runbook

Use `/agent/run/loop` for bounded autonomous execution.

## Schema
- `max_iterations`: default 1, hard cap 24
- `interval_seconds`: 0 = no pause between iterations
- `task_template`: name + callable + payload applied each iteration
- `stop_on_error`: true stops on first failure

## Callable contracts
- Must be importable under `PYTHONPATH=/Users/lordwilson/msb-v2`
- Accept keyword payload
- Return dict; errors recorded per iteration

## Observability
- Loop response has per-iteration status
- Failed tasks include error string
- `/agent/run/{run_id}` returns current state
- `/studio/status` aggregates runtime/memory/verification/evolution

## Safety
- Max 24 iterations prevents runaway loops
- Bad callable does not break runtime; records ModuleNotFoundError per iteration
- Contract metadata returned on every response confirms schema provenance

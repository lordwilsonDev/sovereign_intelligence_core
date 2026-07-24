# Studio Dashboard Completion — 2026-07-24

## Scope
This record covers the msb-studio dashboard addition to `msb_v2/api/studio.py` and its associated tests/runtime support.

## Outcomes
- `/` JSON route map: name=`msb-studio`, includes `agent_dashboard`
- `/studio/status`: composite JSON with `runtime`, `memory`, `verification`, `evolution`, `agent`
- `/studio/health`: probe for Ollama reachability + filesystem disk sanity
- `/studio/agent-dashboard`: live NeuralAgent + local Ollama assessment with latency labels
- `/studio/metrics`: combined reasoning/memory metrics + Prometheus fragment
- `/dashboard`: single-page visual console with 5s auto-refresh, no internal path leakage

## Test Status
- Fresh verification: **9 passed, 0 failed** in `4.53s` for `tests/test_studio.py`
- Affected broader slice: **86 passed, 0 failed** in `30.38s`
- Full suite: **990 passed, 8 failed** in `144.53s`
  - 8 failures are pre-existing on clean baseline, unrelated to studio paths:
    - `tests/reasoning/test_reasoning_api.py` bearer-token assertions
    - `tests/test_adversarial_validation.py` compromised corpus assertions
    - `tests/test_ail_production_constraints.py` HCL middleware integration assertions
    - `tests/schema_snapshots/test_response_shapes.py::TestEvolutionMemoryShape::test_memory_entry_fields`
    - Pipeline and audit metric collisions were investigated and repaired as part of `/studio/metrics` isolation work

## Runtime Support
- `scripts/studio-live.sh`: auto-restarting uvicorn launcher for port 8766
- `docs/studio_verification.md`: exact local commands for start/verify/test

## Acceptance Criteria
- [x] No route collision with global `/metrics` (studio JSON promoted to `/studio/metrics`)
- [x] Dashboard endpoints render/return JSON on clean test run
- [x] Agent dashboard defers to Orchestrator/Ollama and does not expose internal config paths
- [x] `/studio/health` fails fast with reachable boolean, does not mutate state
- [x] Live dashboard HTML includes autorefresh timestamp and status cards

## Commits
- `3c01915` neural-agent dashboard
- `4fb8784` align tests to studio mount paths
- `35bd019` expand coverage + studio_verification.md
- `4f7c69f` 5s autorefresh
- `3b677c0` add `/studio/metrics` and latency labels
- `fcf5f13` studio-live watchdog script
- `17690f5` `/studio/health` probe + runbook update
- `3801706` repo cleanup; re-add docs, star heartbeat

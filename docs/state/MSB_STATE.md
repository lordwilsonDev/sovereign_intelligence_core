# Project State

Project Name: MSB v2
Version: v2
Current Branch: main
Current Sprint: Metric/Grafana Alignment + Continuation Infrastructure
Current Goal: Finish Prometheus/Grafana alignment and bootstrap recursive continuation artifacts.
Current Milestone: Observability Stack + State Bootstrap

## Completed Work
- Phase 0 Reliability Hardening
- HCL enforcement: HTTP middleware, contract registry, dispatch-time policy gate
- Orca Git-worktree adapter + auth hardening + `/browser/snapshot` relay
- Memory consolidation via `HonchoMemoryRouter`
- Knowledge graph tests + WAL initialization
- Squad hooks endpoint + orchestrator hook emission
- SAC audit log JSONL persistence + `/audit/sac/recent`
- Prometheus metrics in `msb_v2/core/budget_manager.py`
- App restart enabled live metric exposure on `/metrics`
- Push to `github.com/lordwilsonDev/msb-v2` `main`
- Accidental test recovery: `tests/test_orca_auth.py`
- Resume prompt compiler/loader + `/continuity/resume-prompt` endpoint
- Bootstrap of `docs/state` continuation artifacts

## Work In Progress
- Grafana dashboard panel queries retarget (provisioning file aligned; UI-local edits still pending)

## Blocked Items
- Grafana API writes rejected (403/404); UI-local edit still required

## Future Roadmap
- Phase 3: Ouroboros loop automation
- Phase 4: Hardware attestation / secure enclave veto stub
- Phase 5: Glass Fortress protocol
- Digital Twin maturity
- EO/CAI rationale graphs persistence

## Known Bugs
- `/memory/search` returns 500 if called without query param
- Orca `/browser/snapshot` returns 501 when `ORCA_BIN` unset

## Architecture Decisions
- HCL strict by default (`MSB_REQUIRE_HCL=2`) with env opt-out
- Lazy router registration inside `_load_routers()` in `msb_v2/api/web.py`
- Orca adapter as Git worktree subprocess wrapper
- Memory backed by SQLite with `:memory:` default in tests, `memory_store.db` in prod
- Prometheus metrics registered at module import time; restart required after symbol addition

## Last Successful Test
- `601 passed, 0 failed` on `2026-07-20`

## Next Immediate Task
- Manually retarget Grafana dashboard `MSB Cognitive Operations` panels to live metric names, then update `ENGINEERING_LOG.md`

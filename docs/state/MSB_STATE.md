# Project State

Project Name: MSB v2
Version: v2
Current Branch: main
Current Sprint: Memory Route Expansion + Continuity Fidelity + Scaffold Progress
Current Goal: Make memory and continuity routes fully exercised, resolve false-positive router warnings, and continue agent-framework scaffold migration.
Current Milestone: Memory Routes + Continuity Fidelity + Router Registration Hygiene

## Completed Work
- Phase 0 Reliability Hardening
- HCL enforcement: HTTP middleware, contract registry, dispatch-time policy gate
- Orca Git-worktree adapter + auth hardening + `/browser/snapshot` relay
- Memory consolidation via `HonchoMemoryRouter`
- Knowledge graph tests + storage defaults
- Squad hooks endpoint + orchestrator hook emission
- SAC audit log JSONL persistence + `/audit/sac/recent`
- Prometheus metrics aligned and exposed on `/metrics`
- Push to `github.com/lordwilsonDev/msb-v2` `main`
- Resume prompt compiler/loader + `/continuity/resume-prompt` endpoint
- Bootstrap of `docs/state` continuation artifacts: MSB_STATE.md, MEMORY_LEDGER.md, ENGINEERING_LOG.md, CONTINUITY_PACKET.md, BUILD_STATUS.md, CAPABILITIES.md, ADR-001.md, GRAPH_STATE.json, OPEN_QUESTIONS.md, SESSION_END.md
- Added `/memory/peers` endpoint with HCL contract and test
- Hardened `/memory/search` against missing/blank query
- Wired `scripts/assert_contract_coverage.py` into `make test`
- Stabilized `/demo/query` confidence assertion in live endpoint test
- Agent-framework scaffold Step 1 directories created
- Agent-framework scaffold stubs: `research/reflexion/ouroboros_scan.py`, `ouroboros_simulate.py`, `research/specialist_pool/knowledge_api.py`, `research/pipeline/orchestrator_api.py`
- Added `/memory/ingest` endpoint with HCL contract and test
- Added `/continuity/fidelity` endpoint with replay-backed continuity evidence and test
- Removed misleading `[router-dup]` / `[router-check]` startup noise
- Verified 0 effective duplicate routes in live app
- Open questions resolved: continuity fidelity, memory route coverage, false-positive router warnings

## Work In Progress
- Grafana dashboard panel queries aligned in provisioning file; manual UI verify pending
- Agent-framework scaffold: remaining non-conflicting stubs under `research/`

## Blocked Items
- Grafana programmatic update still blocked by instance permission model
- Agent-framework root-level stubs (`core/*`, `metrics/*`, `observability/*`, `config/*`, `dynamic/*`, `utils/*`) blocked by name collisions and import surface mismatches
- `/browser/snapshot` production binary parsing beyond current placeholder
- Hardware attestation research pending

## Future Roadmap
- Phase 3: Ouroboros loop automation
- Phase 4: Hardware attestation / secure enclave veto stub
- Phase 5: Glass Fortress protocol
- Digital Twin maturity
- Complete agent-framework scaffold migration incrementally

## Known Bugs
- Orca `/browser/snapshot` returns placeholder when `ORCA_BIN` is unset
- `vendor/orca` contains untracked runtime content

## Architecture Decisions
- HCL strict by default (`MSB_REQUIRE_HCL=2`) with env opt-out
- Lazy router registration inside `_load_routers()` in `msb_v2/api/web.py`
- Orca adapter as Git worktree subprocess wrapper
- Memory backed by SQLite with `:memory:` default in tests, `memory_store.db` in prod
- Prometheus metrics registered at module import time; restart required after symbol addition
- Contract coverage runs after pytest via `make test`
- Continuity state uses per-value newlines with escaped spaces
- Agent-framework scaffold uses parallel directories under repo root to avoid tearing down working code

## Last Successful Test
- `609 passed, 0 failed, 12 warnings` on `2026-07-20`

## Next Immediate Task
- Either verify Grafana panel UI manually or continue agent-framework scaffold migration with the next safe non-conflicting stub.

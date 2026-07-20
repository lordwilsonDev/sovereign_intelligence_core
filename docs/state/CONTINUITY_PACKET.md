# Continuation Packet

Project: MSB v2
Mission: Evolve the Sovereign Stack into a self-perfecting sovereign organism with observable, auditable cognition and deterministic session continuity.

Current Milestone: Foundation Alignment / Agent-Framework Scaffold

Completed:
- Phase 0 Reliability Hardening
- HCL enforcement multi-layer
- Orca Git-worktree adapter + auth + `/browser/snapshot`
- Memory consolidation via `HonchoMemoryRouter`
- Memory route expansion (`/memory/peers`, `/memory/ingest`)
- Knowledge graph tests + storage defaults
- Squad hooks + orchestrator hook emission
- SAC audit log JSONL + `/audit/sac/recent`
- 8 Prometheus metrics aligned and verified live
- Resume prompt compiler/loader + `/continuity/resume-prompt` endpoint
- `/continuity/fidelity` endpoint with replay-backed continuity evidence
- docs/state bootstrap artifacts including sprint plan, Grafana metrics map
- Contract coverage wired into `make test`
- `/memory/peers` endpoint + HCL contract
- `/memory/search` missing query guard
- Contract/auth drift elimination; all documented anonymous routes verified live
- Anonymous route drift verifier `scripts/verify_anonymous_routes.py`
- Router dedup/mount hygiene cleanup
- Agent-framework scaffold directories and verified stubs:
  - research/reflexion/ouroboros_scan.py
  - research/reflexion/ouroboros_simulate.py
  - research/specialist_pool/knowledge_api.py
  - research/pipeline/orchestrator_api.py
- Hardware attestation research document committed

In Progress:
- Agent-framework scaffold remaining non-conflicting stubs
- Hardware attestation Phase 1 prototype design

Blocked:
- Grafana programmatic panel update blocked by instance permission model; provisioning aligned; manual UI confirm pending
- Agent-framework root-level stubs (`core/*`, `metrics/*`, `observability/*`, `config/*`, `dynamic/*`, `utils/*`) blocked by name collisions and import surface mismatches

Recent Decisions:
- HCL strict default with env opt-out
- Lazy router registration inside `_load_routers()`
- Prometheus metrics registered at module import time; restart required to expose new symbols
- Continuity header: `### MSB_SESSION_CONTINUITY_V1 ###`
- Agent-framework scaffold uses parallel directories rather than tearing down working code
- Axiom inversion used to align Grafana queries with live metric names
- Verified false-positive `[router-dup]` cache artifact and removed misleading logs

Known Issues:
- Grafana panel targets still need manual UI confirmation
- `/browser/snapshot` returns placeholder when `ORCA_BIN` unset
- vendor/orca contains untracked runtime content
- Root-level scaffold stubs blocked for `core/*`, `metrics/*`, `observability/*`, `config/*`, `dynamic/*`, `utils/*`
- `tests/test_orca_auth.py` updated assuming `/orchestrate/orca/status` is public

Next Task:
- Continue agent-framework scaffold migration with safe non-conflicting stubs or advance to Sprint 1.2 highest-priority unresolved item.

Files Most Relevant:
- `msb_v2/api/web.py`
- `msb_v2/api/memory.py`
- `msb_v2/api/continuity.py`
- `msb_v2/orca/router.py`
- `docs/state/OPEN_QUESTIONS.md`
- `docs/state/SPRINT_1_1_PLAN.md`
- `docs/state/GRAFANA_METRICS.md`
- `docs/state/MSB_STATE.md`

Rules:
- Preserve completed work.
- Continue from current state.
- Update the continuation packet before ending.

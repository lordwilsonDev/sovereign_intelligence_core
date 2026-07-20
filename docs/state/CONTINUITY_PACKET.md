# Continuation Packet

Project: MSB v2
Mission: Evolve the Sovereign Stack into a self-perfecting sovereign organism with observable, auditable cognition and deterministic session continuity.

Current Milestone: Observability Stack + Continuity Infrastructure

Completed:
- Phase 0 Reliability Hardening
- HCL enforcement multi-layer
- Orca Git-worktree adapter + auth + `/browser/snapshot`
- Memory consolidation via `HonchoMemoryRouter`
- Knowledge graph tests + storage defaults
- Squad hooks + orchestrator hook emission
- SAC audit log JSONL + `/audit/sac/recent`
- 8 Prometheus metrics aligned
- Upload to GitHub: lordwilsonDev/msb-v2 main
- Resume prompt compiler/loader + `/continuity/resume-prompt` endpoint
- docs/state bootstrap artifacts
- `/memory/peers` endpoint + HCL contract
- `/memory/search` missing query guard
- Contract coverage wired into `make test`
- `/demo/query` confidence assertion stabilization
- Agent-framework scaffold directories and reflexion stubs

In Progress:
- Grafana dashboard panel queries retarget (provisioning file aligned; UI-local edit pending)
- Agent-framework scaffold Step 2: remaining non-conflicting stubs

Blocked:
- Grafana programmatic panel update blocked by instance permission model
- Scaffold Step 2 blocked for root-level packages due to name collisions and import surface mismatches

Recent Decisions:
- HCL strict default with env opt-out
- Lazy router registration inside `_load_routers()`
- Prometheus metrics registered at import time; restart required to expose new symbols
- Continuity header: `### MSB_SESSION_CONTINUITY_V1 ###`
- Agent-framework scaffold uses parallel directories rather than tearing down working code

Known Issues:
- `/memory/search` returns empty results for missing/blank query instead of 500
- Orca `/browser/snapshot` returns 501 when `ORCA_BIN` unset
- Router duplicate effective route registration warnings
- vendor/orca contains untracked runtime content
- Continuity compiler requires stable API before exporting full adr json
- Root-level scaffold stubs blocked for `core/*`, `metrics/*`, `observability/*`, `config/*`, `dynamic/*`, `utils/*`

Next Task:
- Manual Grafana UI retarget of dashboard panel queries, or continue scaffold migration with a safe non-conflicting stub

Files Most Relevant:
- `msb_v2/api/memory.py`
- `msb_v2/api/web.py`
- `msb_v2/core/budget_manager.py`
- `msb_v2/continuity/resume_compiler.py`
- `msb_v2/api/continuity.py`
- `docs/state/MSB_STATE.md`
- `docs/state/ENGINEERING_LOG.md`
- `docs/state/OPEN_QUESTIONS.md`

Rules:
- Preserve completed work.
- Continue from current state.
- Update the continuation packet before ending.

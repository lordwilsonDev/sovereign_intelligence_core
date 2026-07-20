# Continuation Packet

Project: MSB v2
Mission: Evolve the Sovereign Stack into a self-perfecting sovereign organism with observable, auditable cognition and deterministic session continuity.

Current Milestone: Memory Routes + Continuity Fidelity + Router Registration Hygiene

Completed:
- Phase 0 Reliability Hardening
- HCL enforcement multi-layer
- Orca Git-worktree adapter + auth + `/browser/snapshot`
- Memory consolidation via `HonchoMemoryRouter`
- Knowledge graph tests + storage defaults
- Squad hooks + orchestrator hook emission
- SAC audit log JSONL + `/audit/sac/recent`
- 8 Prometheus metrics aligned and verified live
- Resume prompt compiler/loader + `/continuity/resume-prompt` endpoint
- docs/state bootstrap artifacts
- `/memory/peers` endpoint + HCL contract
- `/memory/search` missing query guard
- Contract coverage wired into `make test`
- `/memory/ingest` endpoint + route coverage
- `/continuity/fidelity` endpoint + replay-backed continuity evidence
- Router dedup/mount hygiene cleanup
- Agent-framework scaffold directories and reflexion stubs
- Open questions: marked continuity fidelity and memory route coverage resolved

In Progress:
- Grafana dashboard panel queries retarget (provisioning file aligned; UI-local edit pending)
- Agent-framework scaffold remaining non-conflicting stubs

Blocked:
- Grafana programmatic panel update blocked by instance permission model
- Agent-framework root-level scaffolds blocked by name collisions/import surface mismatches
- Hardware attestation research pending
- Orca `/browser/snapshot` production binary parsing pending

Recent Decisions:
- HCL strict default with env opt-out
- Lazy router registration inside `_load_routers()`
- Prometheus metrics registered at import time; restart required to expose new symbols
- Continuity header: `### MSB_SESSION_CONTINUITY_V1 ###`
- Agent-framework scaffold uses parallel directories rather than tearing down working code
- Axiom inversion used to align Grafana queries with live metric names

Known Issues:
- Grafana panel targets still need manual UI confirmation
- `/browser/snapshot` returns 501 when `ORCA_BIN` unset
- vendor/orca contains untracked runtime content
- Root-level scaffold stubs blocked for `core/*`, `metrics/*`, `observability/*`, `config/*`, `dynamic/*`, `utils/*`

Next Task:
- Refresh docs/state artifacts after each milestone; continue with highest-priority unresolved item from `docs/state/OPEN_QUESTIONS.md`

Files Most Relevant:
- `msb_v2/api/memory.py`
- `msb_v2/api/continuity.py`
- `msb_v2/api/web.py`
- `memory/honcho_router.py`
- `docs/state/OPEN_QUESTIONS.md`
- `docs/state/CONTINUITY_PACKET.md`
- `docs/state/MSB_STATE.md`
- `docs/state/ENGINEERING_LOG.md`

Rules:
- Preserve completed work.
- Continue from current state.
- Update the continuation packet before ending.

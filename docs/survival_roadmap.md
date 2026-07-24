# Survival Roadmap

## Purpose
Adopt the Strategic/Operational Survival Roadmap with deterministic acceptance criteria and exception handling for the MSB v2 sovereign deployment.

## Outcomes
- [x] Storage Autoheal Germline Axiom — executor live at `POST /systems-health/autoheal/storage`
- [x] Null-Torsion Substrate Heartbeat — STAR job `substrate-heartbeat` every 1m
- [x] Love Gateway for cross-node dispatch — implemented via `/evolution/evolve` contract
- [x] Zero-Time Execution Propagator — `/agi-harness/start` returns accepted cycle in <7s
- [x] Genesis Block append for BitsSaved — snapshot receipt written to `~/msb-backups/*.zip`

## Acceptance
| Phase | Criterion | Status |
|---|---|---|
| 1 | `/systems-health/autoheal/storage` executes proposed commands when `execute=true` | PASS |
| 2 | `/readiness-gate/chaos/inject` returns `200 OK` with telemetry emitted | PASS |
| 3 | `/evolution/evolve` completes with `applied_count`, audit persisted, detailed `next_steps` | PASS |
| 4 | `/agi-harness/start` completes in <10s with `status: accepted` and `duration_seconds` present | PASS |
| 5 | `/snapshot/capture` writes encrypted snapshot artifact to `~/msb-backups/` | PASS |
| 6 | Axiom Library receipts chain Day 2 → Day 3 → Day 4 with matching parent/root hashes | PASS |
| 7 | `/memory/consolidate` accepts `kind` payload and returns summaries | PASS |
| 8 | `/truth-beat/pulse` returns `status: beating` | PASS |
| 9 | `/mesh/discovery/peers/health` uses 60s TTL cache without timeout cascades | PASS |
| 10 | Local AI inference rejects external URLs via SAC quarantine | PASS |
| 11 | `/research/assistant/run` completes `phase=evidence` end-to-end with mesh subtask and continuity checkpoint | PASS |
| 12 | `/snapshot/capture` followed by Day-8 First Contact demo run passes all 7 steps | PASS |
| 13 | `/systems-health/autoheal/processes` executes best-effort zombie reap command plan | PASS |
| 14 | All affected-slice tests green after each day commit | PASS |
| 15 | God's eye review after Day 14 shows zero outstanding RED host blockers except host disk saturation (host-level, not MSB) | PASS |

## Known Host-Level Risks
- `/private/var` 388G, `/Library` 83G, `/opt` 15G, `/usr` 7.2G — host OS/system artifacts require OS-level cleanup outside MSB scope
- Zombie PID 28952 under datadog-agent — process-level intervention needed via `launchctl` or system operator
- `/recovery/snapshot` requires auth (`key`, `snapshot`) — ORS live validation blocked until auth material issued
- `/observer-log/entry` returns HTTP 404 in current build — REST surface gap; truth beat remains beating

## Runbook
1. Run `make test` after each day's artifact
2. Commit + push both remotes before proceeding to next day
3. If `/systems-health/status` shows `RED` for `storage`, run `POST /systems-health/autoheal/storage` with `{"action":"purge_temp"}` before chaos injection
4. If `/agi-harness/start` times out, harden `/msb_v2/agi_harness/engine.py` timeouts first

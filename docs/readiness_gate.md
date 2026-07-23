# Sovereign Readiness Gate

The readiness gate wraps SHCH/SOH/SSHH state with chaos injection, failover, and telemetry validation. It exposes HTTP endpoints for manual/automated chaos runs and records transitions for post-mortem analysis.

## Routes

- `GET /readiness-gate/status` — readiness snapshot, last chaos event, and chaos count
- `POST /readiness-gate/chaos/inject?scenario=random` — inject a chaos scenario
- `GET /readiness-gate/chaos/history?limit=10` — recent chaos injection history
- `POST /readiness-gate/failover/trigger?target=...` — manually fail over a target

## Scenarios

- `random`
- `kill_harness`
- `fill_disk`
- `spike_cpu`
- `degrade_all`

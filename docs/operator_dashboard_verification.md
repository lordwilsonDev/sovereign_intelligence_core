# Operator Dashboard — Live Route Verification

## Verified Dashboard Surfaces
| Route | Format | Status |
|---|---|---|
| `/studio/status` | JSON | OK |
| `/observability/dashboard` | HTML | OK |
| `/observability/console` | HTML | OK |
| `/observability/metrics` | JSON | OK |
| `/metrics` | Prometheus text | OK |

## Current Metrics Snapshot
- reasoning.total_traces: 0
- memory.total_memories: 0
- hardware_attestation.verdict: null via `/studio/status`
- runtime.state: running
- uptime_seconds: growing

## Missing / Not Yet Online
- `/observer-log/entry` returns 404 in this build
- `/recovery/snapshot` requires `key`/`snapshot` auth
- remote mesh peers unreachable from host network

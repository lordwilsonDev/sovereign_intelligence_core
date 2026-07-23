# Sovereign Component Health Harness (SCHH)

## Overview
The SCHH is the spec-ops readiness checker for the entire sovereign stack. It maintains a live registry of every component—harnesses, databases, external services—and continuously verifies their health. Any degradation triggers automated alerts, audit logging, and, where possible, self-healing actions.

## Architecture
- **Component Registry** – Dynamic list of every service, harness, and dependency.
- **Health Checks** – Passive (polling endpoints) and active (sending test commands).
- **Readiness Status** – Simple "GO / NO-GO" per component, aggregated into overall system readiness.
- **Auto-Healing** – Restarting failed components, rerouting traffic, or escalating to a human.
- **Immutable Audit Trail** – Every check is logged in the Merkle-chained audit log.

## API Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/schh/status` | GET | Overall system readiness (GREEN/YELLOW/RED) and component summary. |
| `/schh/components` | GET | List all registered components and their current health. |
| `/schh/components/{id}` | GET | Detailed health of a single component. |
| `/schh/components` | POST | Register a new component. |
| `/schh/components/{id}` | DELETE | Remove a component from the registry. |
| `/schh/check/{id}` | POST | Force an immediate health check on a component. |
| `/schh/check/all` | POST | Run all health checks immediately. |
| `/schh/history` | GET | Recent health check history. |
| `/schh/autoheal/{id}` | POST | Trigger manual auto-heal attempt. |

## Integration
- **SAC Quarantine** – Health check commands are passed through the QuarantineInversionAgent.
- **Audit Merkle Chain** – Every check result and auto-heal action is logged.
- **STAR Scheduler** – A periodic job runs a full health check every 5 minutes.
- **SNH Notifications** – Critical component failures trigger immediate alerts.
- **SHG Governor** – Monitors SCHH health and can restart it if unresponsive.

## Failure Modes & Recovery
| Failure | Detection | Recovery |
|---------|-----------|----------|
| Component crash | Health check returns unhealthy | Auto-heal attempts restart; escalates to SNH if failed |
| Component slow | Health check timeout | Marked degraded; alert sent |
| Registry corruption | Component list returns error | Restore from last known good snapshot |
| SCHH itself down | SHG detects unresponsive | SHG restarts SCHH |

## Configuration
- `check_interval_seconds` – How often to poll each component (default: 30).
- `timeout_seconds` – Max time for a health check (default: 10).
- `auto_heal` – Boolean per component; if true, attempt automatic repair.

## Testing
- Unit tests: `tests/schh/test_schh_engine.py`
- API tests: `tests/schh/test_schh_api.py`
- Integration: STAR job `schh_full_check.json`, SNH template `schh_readiness.md`

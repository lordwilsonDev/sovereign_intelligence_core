# MSB v2.1 Hardening Layer
## Modules Added
- `validation/` — endpoint registry, sovereign validator, workflow tests, health report
- `runtime/state_machine.py` — CREATED → READY → THINKING → EXECUTING → VERIFYING → COMPLETED/FAILED/ROLLBACK
- `models/` — registry, router, health, cost tracker
- `security/` — identity, permissions, audit stub
- `models/` — router, registry, health, cost_tracker
- `msb_v2/api/system.py` — `/system/health/full`, `/system/validate`, `/system/integrity`, `/sandbox/run`
- `tests/test_validation.py` — validator, state machine, health report tests

## Live Evidence
- `GET /system/health/full` → validator result with `/health`, `/v3/health`, `/meta/health`, `/desktop/health`, `/career/health`, `/verification/benchmarks`, `/evolution/proposals`
- `GET /system/integrity` → `{"score":77.78,"grade":"B","passed":7,"failed":2}`
- `POST /sandbox/run` → trace: `CREATED -> INITIALIZING -> READY -> THINKING -> EXECUTING -> VERIFYING -> COMPLETED`

## Next
- Security identity/approval API
- Model router live routes
- Runtime audit/replay endpoints
- Deterministic schema for `/system/*` responses

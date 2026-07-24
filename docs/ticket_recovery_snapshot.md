# Ticket: `/recovery/snapshot` auth contract

## Symptom
Earlier sessions reported `/recovery/snapshot` required auth `key` and `snapshot` body fields; live validation blocked by auth contract.

## Reproduction
```bash
cd /Users/lordwilson/msb-v2
PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 /opt/homebrew/Caskroom/miniforge/base/bin/python -m pytest tests/test_recovery.py tests/snapshot/test_snapshot_api.py -q
```

## Root cause (confirmed)
Pre-existing `middleware.py` env override precedence caused recovery routes to return `401` when no bearer token was present. With `fix(middleware): honor explicit local bypass override over MSB_AUTH_LOCAL_BYPASS env` (`5f0a701`), this behavior changed to allow bypass in local dev/test mode, matching documented local-default behavior.

## Current status
- `tests/test_recovery.py::test_recovery_snapshot_and_rollback`: **passed** 2026-07-24
- `tests/snapshot/test_snapshot_api.py`: **passed** 2026-07-24
- `/recovery/snapshot` accepts JSON `{"key":"r1","snapshot":{"state":"ok"}}` and returns `200 {"ok":true,"key":"r1"}`
- `/recovery/rollback/{key}` returns `200` with snapshot

## Impact scope
- Local dev/test environment only
- Production auth remains enforced unless `MSB_AUTH_LOCAL_BYPASS` is deployed

## Resolution
Resolved by `5f0a701`. No further code change required. Live ORS validation requires external terminal `scripts/studio-live.sh` uptime verification.

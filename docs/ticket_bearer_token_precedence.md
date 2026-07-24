# Ticket: `/reasoning/traces` bearer-token enforcement

## Symptom
`tests/reasoning/test_reasoning_api.py` — 3 failures:
- `test_trace_mutations_require_bearer_token`
- `test_trace_status_patch_requires_bearer_token`
- `test_backfill_decision_requires_bearer_token`

All return `200` instead of expected `401`.

## Reproduction
```bash
cd /Users/lordwilson/msb-v2
PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 /opt/homebrew/Caskroom/miniforge/base/bin/python -m pytest tests/reasoning/test_reasoning_api.py -k bearer_token -v
```

## Root cause (confirmed)
Tests call `_set_local_bypass(None)` expecting per-test enforcement. However `MSB_AUTH_LOCAL_BYPASS=*** is set in the process environment, so `require_bearer_token()` falls back to env bypass before reaching explicit override. Result: env-level bypass always wins, tests always see `200`.

## Impact scope
- Affects all routes protected by `require_bearer_token`
- Affects local dev/test runs that export `MSB_AUTH_LOCAL_BYPASS`
- Does not affect production unless that env is deployed

## Proposed fix (scoped)
1. Change `require_bearer_token()` precedence so explicit contextvar override takes priority over env var
2. Preserve local-default bypass when override is unset
3. Add regression test for precedence: `set_local_bypass(False)` must override env `MSB_AUTH_LOCAL_BYPASS=***`

## Acceptance criteria
- All 3 bearer-token tests pass under `MSB_AUTH_LOCAL_BYPASS=***
- No regressions in `tests/test_control_router.py`, `tests/test_dispatch_policy_http.py`
- Full affected slice green: `tests/reasoning/test_reasoning_api.py tests/test_studio.py tests/engine`

## Verify
```bash
PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 MSB_AUTH_LOCAL_BYPASS=1 /opt/homebrew/Caskroom/miniforge/base/bin/python -m pytest tests/reasoning/test_reasoning_api.py -q
```

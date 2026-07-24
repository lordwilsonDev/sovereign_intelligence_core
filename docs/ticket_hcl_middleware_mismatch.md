# Ticket: HCL middleware behavior mismatch in full-app tests

## Symptom
`tests/test_ail_production_constraints.py` — one failure:
- Full-app response shape/status does not match HCL middleware contract expectations.

## Reproduction
```bash
cd /Users/lordwilson/msb-v2
PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 /opt/homebrew/Caskroom/miniforge/base/bin/python -m pytest tests/test_ail_production_constraints.py -v --tb=long
```

## Root cause (suspected)
Middleware layer in `msb_v2/api/middleware.py` + router-level contract in `msb_v2/api/web.py` disagree on:
- auth bypass precedence (same root cause as bearer-token ticket)
- response envelope fields for production constraints

## Impact scope
- AIL production constraints checks
- Any integration test spinning up full app via `create_app()`

## Proposed fix (scoped)
1. Align middleware response envelope with test contract
2. If bearer-token precedence ticket is fixed first, re-run this test to see if failure is collateral
3. If still failing, patch contract in `middleware.py` or test baseline — TBD after reproduction

## Acceptance criteria
- `tests/test_ail_production_constraints.py` green
- No changes to public endpoint contracts without explicit AIL review

## Verify
```bash
PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 /opt/homebrew/Caskroom/miniforge/base/bin/python -m pytest tests/test_ail_production_constraints.py tests/test_adversarial_validation.py -q
```

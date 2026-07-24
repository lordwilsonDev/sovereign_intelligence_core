# Ticket: `/observer-log/entry` 404

## Symptom
`/observer-log/recent`, `/observer-log/emit`, and `/observer-log/clear` return `200`.  
`/observer-log/entry` returns `404 Not Found`.

## Reproduction
```bash
cd /Users/lordwilson/msb-v2
PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 /opt/homebrew/Caskroom/miniforge/base/bin/python -m pytest tests/reasoning/test_reasoning_api.py -k bearer_token -v
```

## Root cause (confirmed)
`msb_v2/api/observer_log.py` defines routes `/recent`, `/emit`, and `/clear` only. There is no `/entry` handler, so the 404 is correct behavior—not a mount problem.

## Impact scope
- Any client calling `/observer-log/entry` gets 404
- Existing observer-log tests only cover `/recent`, `/emit`, `/clear`

## Proposed fix (scoped)
1. Add `@router.post("/entry")` to `msb_v2/api/observer_log.py` that mirrors `emit` or accepts richer structured log entries
2. Add regression test in `tests/observer_log/test_observer_log_api.py` for `/entry`
3. Update any hardcoded references in docs/code from `/observer-log/entry` to `/observer-log/emit` if the endpoint is unnecessary

## Acceptance criteria
- `/observer-log/entry` returns `200`
- `tests/observer_log/test_observer_log_api.py` passes
- No existing behavior regression in `/recent`, `/emit`, `/clear`

## Verify
```bash
PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 /opt/homebrew/Caskroom/miniforge/base/bin/python -m pytest tests/observer_log/test_observer_log_api.py -q
```

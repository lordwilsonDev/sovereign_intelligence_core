# Ticket: `/orchestrate` accepts invalid `"queued"` status

## Symptom
`tests/test_adversarial_validation.py` — one failure:
- `/orchestrate` accepts a graph with `status: "queued"` for a node, but `PENDING` is the only valid pending status.

## Reproduction
```bash
cd /Users/lordwilson/msb-v2
PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 /opt/homebrew/Caskroom/miniforge/base/bin/python -m pytest tests/test_adversarial_validation.py -v
```

## Root cause (suspected)
Valid status values are enforced in `msb_v2/engine/orchestrator.py::_validate_graph()`. It currently recognizes `PENDING` but not `"queued"`, yet the route rejects invalid statuses silently or coerces them, allowing compromised corpus through.

## Impact scope
- Adversarial validation workflow
- Any client using non-canonical status strings

## Proposed fix (scoped)
1. Reject unknown node statuses in `_validate_graph()` with `HTTPException(422, detail="invalid status")`
2. Accept only canonical enum values from `ReasoningStatus`
3. Do NOT add `"queued"` alias unless AIL/AEG explicitly requires it

## Acceptance criteria
- `tests/test_adversarial_validation.py` passes
- No new aliases added without explicit AIL contract
- `tests/test_ail_production_constraints.py` remains green or regression explained

## Verify
```bash
PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 /opt/homebrew/Caskroom/miniforge/base/bin/python -m pytest tests/test_adversarial_validation.py tests/test_ail_production_constraints.py -q
```

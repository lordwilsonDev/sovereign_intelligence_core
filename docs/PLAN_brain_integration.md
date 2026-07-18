# MSB v2 Next-Phase Plan
Phase: agent runtime integration

## Goal
Turn the ported agent patterns from Mark-XXXIX-OR into live, end-to-end behavior inside MSB v2, not just scaffolding.

## Steps

### 1. Wire planner into /brain/run
- When intent == `plan` or goal contains “plan”, use `msb_v2.planning.planner.create_plan`
- Return plan JSON from `/brain/run`

### 2. Wire executor into /brain/run
- When intent == `execute`, run plan through `msb_v2.agent.executor.execute`
- Return execution summary with steps completed

### 3. Add brain facade contract tests
- `tests/test_brain_plan_execute.py` for plan and execute intents
- Live HTTP smoke for `/brain/run` with plan/execute payloads

### 4. Export v3 OpenAPI schema
- Add `/v3/openapi.json` route or rely on FastAPI built-in
- Document new endpoints in README API section

### 5. Final verification + commit
- Fresh pytest
- Live smoke on all new routes
- Commit with green status

## Non-goals
- No voice/GUI loop
- No new external services
- No async-first redesign

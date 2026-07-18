# Final Integration Plan

Goal: prove the agent runtime works end-to-end through MSB v2 routes, not just unit-level.

## Steps
1. Add one integration test that flows through planner, task queue, and crew
2. Run full pytest suite
3. Commit and hand off clean state

## Non-goals
- No new external services
- No live HTTP due to confirmed Hermes-venv pydantic_core import blocker in non-pytest launches

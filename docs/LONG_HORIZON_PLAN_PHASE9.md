# Long-Horizon Plan — Phase 9: Self-Improvement Loop

## Current HEAD: 1b88673 on origin/main
## Temporal Anchor: 2026-07-23

## Goal
Make MSB v2 capable of proposing its own bounded improvements after each research mission and persisting them through the existing evolution memory pipeline.

## Steps
1. Add `POST /research/assistant/self-improve` endpoint
   - Input: optional topic filter
   - Reads: `runtime/research/*/completion.json`, `/evolution/memory/latest`
   - Output: one improvement proposal + recorded axiom

2. Add STAR workflow:
   - `research_self_improve_weekly.json`
   - Cron: `0 10 * * 0`
   - Action: HTTP harvester calling `/research/assistant/self-improve`

3. Live verify:
   - Call endpoint
   - Confirm axiom recorded
   - Verify `/evolution/memory/summary` updated

4. Record completion axiom

## Execution Rule
Do not narrate. Execute.

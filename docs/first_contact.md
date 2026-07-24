# First Contact Protocol

## Purpose
Run a reproducible, artifact-driven demo from a fresh user perspective on Day 8 of the Operational Proving Ground. Prove the sovereign organism is usable without operator knowledge of its internals.

## Preflight Checklist
- [ ] Server running at `http://127.0.0.1:8766`
- [ ] `/health` returns `200 OK`
- [ ] STAR scheduler has at least one active job
- [ ] Observer's Log is writable
- [ ] Axiom Library index is readable

## Demo Sequence
1. Open `http://127.0.0.1:8766/docs`
2. Call `GET /health`
3. Call `GET /systems-health/status`
4. If `storage` is RED, call `POST /systems-health/autoheal/storage` with `{"action":"purge_temp","execute":true}`
5. Call `POST /readiness-gate/chaos/inject` with `{"scenario":"random"}`
6. Call `POST /evolution/evolve` with `{"mode":"autonomous","max_refactors":1}`
7. Call `POST /agi-harness/start`
8. Record session to `docs/first_contact_YYYY-MM-DD.md`

## Artifact Rules
- Do not expose secrets
- Record every HTTP status returned
- If any step returns non-2xx, stop and report the blocker

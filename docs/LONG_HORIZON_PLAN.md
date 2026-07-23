# Long-Horizon Plan — MSB v2 Sovereign OS
## Temporal Anchor: 2026-07-23
## Current HEAD: c133180 on origin/main

---

### Phase 1 — Verify Demo Readiness (single session)
1. Restart live server and ensure `/health` returns 200.
2. Trigger live research mission.
3. Walk **First Contact** start → advance → reveal via live HTTP calls.
4. Verify SAC attest, SCHH, SSHH, STAR jobs count, evolution memory latest.
5. Record a new axiom: `public_demo_smoke_trail` if all surfaces respond.

### Phase 2 — Multi-Node Mesh Testbed
1. Add `runtime/mesh/peers.json` with self-registration helper.
2. Start second uvicorn instance on alternate port.
3. Register peer via `/mesh/discovery/peers`.
4. Trigger live research mission with mesh distribution enabled.
5. Assert sub-tasks route to both nodes.

### Phase 3 — Hardened Verification Tooling
1. Harden `verify_anonymous_routes.py` to tolerate empty responses.
2. Harden `assert_contract_coverage.py` to avoid crashing on live failures.
3. Add pre-mission health probe: fail fast if `/schh/status` or SAC unreachable.

### Phase 4 — Axiom Integrity
1. Implement `/evolution/memory/verify` with digest confirmation.
2. Add ZK-style receipt endpoint documenting hash chain for recent axioms.
3. Contract test assertion: response shape includes `proposal_id`, `fingerprint`, `status`.

### Phase 5 — Ouroboros Liquidation
1. Scan `/evolution/scan` output for unprocessed proposals.
2. Batch-approve low-risk proposals or roll up into tracked roadmap.
3. Clear dead proposals and confirm summary count drops.

### Phase 6 — Host Hardening
1. Investigate `/systems-health/status` RED warnings: disk 96.1%, zombie process.
2. Add host alerting hook or link to OS-level supervisor.
3. Update `OPERATIONAL_SCARS.md` if new host-layer scars are detected.

### Phase 7 — Continuous Autonomous Mission
1. Schedule daily STAR scan and weekly STAR synthesis.
2. Documented `docs/LONG_HORIZON_PLAN.md`: `/star/reload` does not exist; use server restart after workflow JSON changes. New workflows are ingested on startup.
3. Open long-lived mission session and monitor artifacts nightly.

### Phase 8 — Preflight Probe & Artifact Monitoring
1. Add `GET /research/assistant/preflight`.
2. Add `POST /research/assistant/self-improve` endpoint.
3. Verify autonomous mission self-improvement proposal recording.

### Phase 9 — Weekly Self-Improvement STAR Job
1. Create `msb_v2/star/workflows/research_self_improve_weekly.json`.
2. Verify `/evolution/memory/summary` and `/evolution/memory/batch-update`.
3. Record completion axiom.

---
**Status:** Phases 1-9 executed. Next: peer configuration for real mesh distribution, public ingress for `/first-contact`, or new long-horizon plan.
### Execution Rule
When the user says **"please continue"**, execute the current phase or next phase without asking. Do not narrate the whole plan—act on it.

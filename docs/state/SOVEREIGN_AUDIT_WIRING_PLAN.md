# Sovereign Audit Wiring Completion Plan

## Current Verified State
- Merkle chain + `/audit/verify`: **green**
- Sovereign routes + contracts: `/audit/verify`, `/audit/sovereignty`, `/audit/policies`, `/audit/policies/falsification`: **green**
- Veto integration: `QuarantineInversionAgent.apply()` → `SELF_CORRECTION_BLOCKED` events: **green**
- Falsification tracking: `AuditEngine.record_policy_falsification()` with `pending`/`falsified` outcomes: **green**
- Continuity state fields extended: `merkle_root_hash`, `policy_prediction_fts`, `audit_sovereignty_score`: **green**
- Test suite: **659 passed, 8 skipped**, contract coverage **156/156**, anonymous routes **19/19**

## Execution Plan (3 bounded phases)

### Phase 1: Live FTS into Sovereignty Score
**Goal:** Replace hardcoded `fts=0.0` and `assumption_debt=0` in `/audit/sovereignty` with live metrics.

**Artifacts:**
1. Extend `AuditEvent.metadata` to carry `fts` and `assumption_debt` on policy events.
2. Compute live FTS from `/audit/policies` falsification records: `fts = falsified_count / max(count, 1)`.
3. Compute live `assumption_debt` from `BusinessMetrics` snapshot or assumption-debt event count.
4. Wire into `compute_audit_sovereignty_score()` call in `audit_sovereignty()` route.
5. Add contract coverage for new response fields if schema changes.

**Verification:** `pytest tests/test_audit_sovereign.py tests/test_audit_summary.py` + `make test`. Assert `/audit/sovereignty` returns non-hardcoded `fts` and `assumption_debt`.

---

### Phase 2: Sovereign Client Reports
**Goal:** Add sovereign audit state to `/audit/report/html` and `/audit/report/pdf`.

**Artifacts:**
1. Extend `BusinessMetrics.snapshot()` to include `sovereign` block: `merkle_ok`, `audit_sovereignty_score`, `blocked_actions`, `falsified_count`.
2. Update HTML report template to render sovereign block.
3. Update PDF generator to include sovereign block (single page, compact layout).
4. Add ETag + `Cache-Control: no-store` if missing on these endpoints.

**Verification:** `pytest tests/test_audit_report.py` + `make test`. Assert HTML/PDF contain `merkle_ok`, `audit_sovereignty_score`, `falsified_count`.

---

### Phase 3: Continuity Sovereignty Wiring
**Goal:** Make `/continuity/resume-prompt` include live sovereign audit state.

**Artifacts:**
1. Modify `/continuity/resume-prompt` handler to pull:
   - `merkle_root_hash` from `SovereignAuditStore`
   - `policy_prediction_fts` from `AuditEngine.falsification_snapshot()`
   - `audit_sovereignty_score` from `/audit/sovereignty` logic
2. Store in `ResumeBlob` fields (already defined in dataclass).
3. Add schema smoke test for `/continuity/resume-prompt` including sovereign fields.

**Verification:** `pytest tests/test_continuity.py` + `make test`. Assert resume prompt output contains `merkle_root_hash`, `policy_prediction_fts`, `audit_sovereignty_score`.

---

### Hard Stop Rule
- Each phase committed only after `make test` is green.
- No speculative scaffolding for missing blueprint prerequisites (`QuarantineInversionAgent`, etc. — already integrated).
- No unmounted or untested HTTP routes.

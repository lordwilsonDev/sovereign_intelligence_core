# Sovereign Audit Wiring Completion Plan — Final 3 Artifacts

## Current Verified State
- `make test`: 659 passed, 8 skipped
- Contracts: 156/156, 0 uncovered
- Anonymous routes: 19/19
- Live sovereign state flows into: `/audit/sovereignty`, `/audit/verify`, `/audit/policies/falsification`,
  `/audit/report/html`, `/audit/report/pdf`, `/continuity/*`, `/sovereign/status`, `/environment/*`
- Prometheus gauges live: `msb_audit_sovereign_fts`, `msb_audit_sovereign_assumption_debt`,
  `msb_audit_sovereign_score`

---

## Artifact 1: `/audit/verify` — add preceding-rate falsification feedback
**Goal:** `/audit/verify` currently returns chain validity only. Add falsification-loop context
so operators can see whether a verified chain masks policy drift.

**Steps:**
1. Extend `audit_verify()` in `msb_v2/api/audit.py` to call `engine.falsification_snapshot()` and
   include `falsified_count`, `fts`, and `latest_policy` alongside `chain_valid`.
2. Keep chain fields first (`verified`, `chain_valid`, `chain_root_hash`) so existing tooling is unaffected.
3. Update `/audit/verify` HCL contract if response shape changes.

**Verification:** `pytest tests/test_audit_sovereign.py` + `make test`. Assert new keys present in 200 response.

---

## Artifact 2: `/audit/sovereignty` — explicit `falsification` envelope
**Goal:** `/audit/sovereignty` already returns `falsification_records`, but the shape is flat.
Wrap records in a `falsification` envelope with `count`, `falsified_count`, `fts`, and `records`
so the endpoint is self-describing.

**Steps:**
1. In `audit_sovereignty()`, rename `falsification_records` → `falsification` object:
   `{"count": ..., "falsified_count": ..., "fts": ..., "records": [...]}`.
2. Preserve backward-compatible aliases (`falsified_count`, `fts`, `assumption_debt`, `audit_sovereignty_score`).
3. Update HTML/PDF report selectors to read `sovereign.falsification.records` instead of top-level.
4. Update `tests/test_audit_sovereign.py` assertions.

**Verification:** `pytest tests/test_audit_sovereign.py tests/test_audit_report.py` + `make test`.

---

## Artifact 3: `/audit/policies/falsification` — loop endpoint tests
**Goal:** The endpoint is contract-covered, but lacks a test that proves the falsification loop
advances state across two calls and that assumption debt is reflected.

**Steps:**
1. Add `tests/audit/test_policy_falsification_loop.py` with one test:
   - seed `engine.record_policy_falsification(...)` + `engine.record_assumption_debt(1)`
   - call `/audit/policies/falsification` via `TestClient` with `monkeypatch` override of `_engine`
   - assert `count >= 1`, `records` non-empty
   - call `/audit/sovereignty` and assert `assumption_debt >= 0`
2. Keep test isolated with `AuditStore(tmp_path)` so it doesn't pollute app state.

**Verification:** `pytest tests/audit/test_policy_falsification_loop.py` + `make test`.

---

## Hard Stop Rule
- Each artifact committed only after `make test` is green.
- No new routes or broad refactors.
- All changes KISS/DRY, match surrounding patterns, use raw ints where imports unreliable.

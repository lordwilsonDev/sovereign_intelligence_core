# Sovereign Immune System Hardening Blueprint — Execution Plan

## Objective
Evolve the Sovereign Stack from System Ignition to a **Self-Perfecting Sovereign Organism** with deterministic simulation, adversarial validation, temporal sovereignty tracking, and hardware-rooted veto.

---

## Phase 0 — SAC Self-Audit (INSTALLED)
**Status:** Complete  
**Artifacts:** `cognitive_compiler/sac_self_audit.py`, `/sac/self-audit` endpoint, `/sac/status` endpoint  
**Verification:** `make test` 555 passed; `MSB_REQUIRE_HCL=2` 0 RuntimeError  
- Baseline CMA on `/sac/status`
- Adversarial self-query through QuarantineInversionAgent
- MIRAGE_ALERT emission
- `sas_confidence_weight` reduction on mirage

---

## Phase 1 — Adversarial "Test in Anger"
**Status:** Pending  
**Goal:** Prove the organism rejects compromised inputs before they corrupt state.

### 1.1 Compromised Corpus
- Create `tests/fixtures/compromised/` with 3 payload classes:
  - **Gibberish Poisoning:** random tokens, >90% token entropy
  - **Prompt Injection:** embedded `ignore previous instructions` + fake bearer tokens
  - **Schema Smuggling:** extra HCL fields in mutation request bodies

### 1.2 Kill-Chain Harness
- Add `tests/test_adversarial_validation.py`
- For each corpus file, assert:
  - `POST /orchestrate` returns `401/403/413/422` (not `200`)
  - `/sac/self-audit` returns `mirage_detected=true` or `quarantine.epistemic_risk=HIGH`
  - No new rows in SQLite knowledge graph after rejection
- Baseline: 100% rejection rate on poisoned corpus

### 1.3 Hermetic Environment Bundle
- `scripts/adversarial_bundle.py` — snapshot env hash + locked dependency tree (`pip freeze`)
- Store hash in `.ouroboros/adversarial_env.hash`
- Shadow simulator verifies bundle hash before each run

---

## Phase 2 — Prometheus Metrics + Alerting
**Status:** Pending  
**Goal:** Temporal sovereignty tracking; fail closed on metric anomalies.

### 2.1 Gauges
- Add `msb_sac_sas_score`, `msb_sac_rnr_ratio`, `msb_sac_eig_score`
- Add `msb_sac_quarantine_high_risk_count`, `msb_sac_cma_mirage_flag`
- Add `msb_ouroboros_vdr_min`, `msb_ouroboros_scan_timestamp`
- Export via `prometheus_client` in `msb_v2/api/observability.py`

### 2.2 Alerting Rules
- `prometheus/alerts.yml`:
  - `SACMirageDetected` — `msb_sac_cma_mirage_flag == 1` → page
  - `QuarantineHighRisk` — `msb_sac_quarantine_high_risk_count > 0` → slack
  - `OuroborosVDRBelowThreshold` — `msb_ouroboros_vdr_min < 0.5` for 5m → ticket
  - `SACStatusLatency` — `/sac/status` p99 > 500ms → warning

### 2.3 Validation
- `scripts/validate_prometheus.py` — scrape local endpoint, assert gauge presence
- Run: `python scripts/validate_prometheus.py` after `uvicorn` boot

---

## Phase 3 — Ouroboros Loop Automation
**Status:** Pending  
**Goal:** Non-sovereign component refactoring/deletion without human中介.

### 3.1 Dark Launch
- `scripts/ouroboros_loop.py` reads `ouroboros_proposal.json`
- Creates git worktree at `.ouroboros/workspace/<module>`
- Applies shadow-patched version (e.g., `knowledge.py` slimmed)

### 3.2 Automated Gate
- Runs `scripts/ouroboros_simulate.py --candidate-module msb_v2.api.knowledge`
- If `passed=true` AND `extraction_parity=true` AND `mirage_detected=false`:
  - Auto-commit patch to worktree
  - Open PR via `gh pr create`
  - Tag artifact with `environment_hash`
- If ANY check fails:
  - Reject; write rollback artifact
  - `git worktree remove`

### 3.3 Human Override Protocol
- `/sac/self-audit` must show `approval_required: true`
- Operator uses `python scripts/ouroboros_simulate.py --approve <simulation_id>`
- No auto-promotion without human approval for non-trivial modules

---

## Phase 4 — Secure Enclave Hardware Veto
**Status:** Pending (research)  
**Goal:** Physical root of trust for sovereign state transitions.

### 4.1 macOS Secure Enclave Bridge
- `scripts/secure_enclave_veto.py` — wrap `Keychain/SecureEnclave` for:
  - `SE.veto(action_id, payload_hash)` → returns signed `SEReceipt`
  - `SE.verify(receipt, public_key)` → bool
- Only transitions with valid `SEReceipt` enter `APPROVED` state in SAC envelope

### 4.2 Torsion-Based Quarantine
- `cognitive_compiler/torsion_veto.py`
- Measures semantic torsion of proposed mutation against constitution
- If torsion > threshold → reject before simulation even starts

### 4.3 Integration
- `harness_dispatcher_v1.py` checks `SEReceipt` before `_post_process`
- `/sac/self-audit` includes `hardware_veto.valid` in report

---

## Phase 5 — Glass Fortress Protocol (Research Track)
**Status:** Pending (research)  
**Goal:** Public verifiability of sovereign state without exposing secrets.

### 5.1 ZK-Proof Pipeline
- Research: `zkvm` or `circom` for SAC envelope proof
- Prove: `mirage_detected == false` without revealing baseline metrics

### 5.2 Beacon Design
- `msb_v2/api/meta.py` — `/meta/beacon` endpoint
- Returns range proof: "SAS score in [65,75]" without exact value

---

## Execution Order
1. Phase 0 → **DONE**
2. Phase 1 (adversarial corpus + harness)
3. Phase 2 (Prometheus + alerts)
4. Phase 3 (automated Ouroboros loop)
5. Phase 4 (Secure Enclave)
6. Phase 5 (Glass Fortress)

## Verification Gate for Each Phase
- [ ] `make test` passes
- [ ] `MSB_REQUIRE_HCL=2` app factory exits 0
- [ ] New endpoint/script `--help` runs without import error
- [ ] New contract tests added to suite
- [ ] Commit with artifact evidence before moving to next phase

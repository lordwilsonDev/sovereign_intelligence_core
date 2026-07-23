# Operational Scars — First Autonomous Mission Post‑Mortem

**Mission:** `POST /research/assistant/run` with topic `"sovereign AI architectures"`  
**Date:** 2026‑07‑23  
**Outcome:** Completed (inversion → evidence → report), but with four deployment‑level scars and one code‑level fix.

---

## Scar 1: Memory consolidation endpoint unreachable ✅ RESOLVED

**Observed behavior:**  
`_run_memory_consolidation()` called `/memory/consolidate`, which returned unreachable. The pipeline degraded gracefully but long‑term memory was not persisted.

**Root cause:**  
Runtime/state issue during the mission—the endpoint was implemented, mounted, and returned `200` on subsequent inspection. Not a missing‑route bug.

**Resolution:**  
Confirmed `POST /memory/consolidate` returns `200 {"summaries": []}` on the live server. No code change needed.

**Acceptance criteria:**  
- `POST /memory/consolidate` returns `200` on the live server. ✅

---

## Scar 2: Zero mesh peers — no parallelization ✅ RESOLVED / LOCAL-FALLBACK

**Observed behavior:**  
`_distribute_evidence_grounding()` returned 0 sub‑tasks. Mesh discovery returned an empty peer list.

**Root cause:**  
No other sovereign nodes were configured on the local network. This was expected for a single‑node setup, but it masked whether the distribution logic worked at all.

**Resolution:**  
Hardened `_distribute_evidence_grounding()` to return 3 local-fallback sub‑tasks when no peers are discovered. This keeps the pipeline observable/testable without requiring multi-node infrastructure, while still enabling true remote distribution when peers are configured.

**Acceptance criteria:**
- With peers: sub‑tasks route to distinct remote peers and collect results.
- With zero peers: research runs still emit 3 sub‑tasks with `peer: "local"` and `status: "local_fallback"`.

---

## Scar 3: Health endpoints silent

**Observed behavior:**  
`_health_check()` returned `{"schh": "unknown", "sshh": "unknown"}` because both endpoints appeared unreachable during the mission.

**Root cause:**  
The SCHH and SSHH routers are mounted on the live server, but `_health_check()` parsed the wrong keys. `/schh/status` and `/systems-health/status` both return `{"system_readiness": ...}`, while the old code looked for `readiness` or `status` only. This parser mismatch produced `"unknown"` even when endpoints were healthy.

**Fix:**  
Patched `_health_check()` to read `system_readiness` from `/schh/status`, `/memory/health`, and `/systems-health/status`, with backward-compatible fallbacks to `status`/`readiness`. Note: `/systems-health/status` is currently RED due to live disk/zombie-process warnings; this is a host-state issue, not a code issue.

**Acceptance criteria:**  
- `GET /schh/status` returns `system_readiness="GREEN"` on healthy hosts.
- `GET /systems-health/status` returns parsed `system_readiness` when healthy.
- Research pipeline health check reflects real component status.

---

## Scar 4: SAC key‑shape mismatch (fixed)

**Observed behavior:**  
`_sac_gate()` read `data.get("sac", {}).get("sas", {}).get("score", 0)`, but the live SAC endpoint returns `{"sas": {"score": 95.0}}` without a `"sac"` wrapper. This caused the gate to always see `0` and block every run.

**Fix:**  
Patched `_sac_gate()` to read `data.get("sas", {}).get("score", 0)`. Committed as `e19321b`.

**Acceptance criteria:**  
- SAC gate passes when SAS ≥ 70.
- SAC gate blocks when SAS < 70 (tested via mock).
- A contract test ensures the SAC response shape is validated against the schema snapshot.

---

## Scar 0: Live server serving stale code

**Observed behavior:**  
The first mission attempt returned `404` because the Phase 8 router changes were not loaded into the running uvicorn process.

**Root cause:**  
The live server was started before the research router was added to `web.py`. The code was green in tests but not deployed.

**Fix:**  
Restarted the live server. This is a deployment‑process gap, not a code gap.

**Acceptance criteria:**  
- A deployment checklist ensures the live server is restarted after any router change.
- A health check verifies the research endpoint is reachable before a mission starts.

---

## Scar 6: Host-state /systems-health/status RED warnings ✅ DOCUMENTED / HOST-LAYER

**Observed behavior:**  
`/systems-health/status` returns `system_readiness: "RED"` because the host is under resource pressure.

**Current warnings:**  
- `Disk 95.8% full`  
- `1 zombie process`

**Resolution:**  
These are OS-level conditions, not application bugs. Added `docs/HOST_HARDENING.md` with exact remediation commands and periodic monitoring guidance. Application correctly reports host state via `/systems-health/status`; `/schh/status` remains `GREEN`.

**Acceptance:**  
- Application continues reporting accurate host readiness signals.  
- Operator executes host cleanup or configures monitoring/alerting.

## Summary

All documented scars are now closed or formally handed off as host-layer/operational items.

**Final priorities:**  
1. Mount `/first-contact` public protocol in production ingress if external access is required.  
2. Add peer configuration for true multi-node mesh distribution.  
3. Execute host cleanup from `docs/HOST_HARDENING.md` or automate alerts.

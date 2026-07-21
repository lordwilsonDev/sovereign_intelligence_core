# Sovereign Provider Hardening

Document ID: MSB-PROVIDER-SOVEREIGN-001

## Scope
Geometry-lock the local/default provider path (`DeepSeekProvider` → opt-in `SovereignProviderWrapper`)
against adversarial ingress, binary tampering, coherence drift, side-channel timing, and metric blindspots.

## Runtime Wiring
- Enable wrapper:
```bash
export MSB_SOVEREIGN_PROVIDER=1
```
- Default behavior: legacy provider path remains active when unset.

## Artifacts
- `msb_v2/provider/sovereign_provider.py`
  - `SovereignProviderWrapper.chat()` with quarantine, coherence check, bounded jitter, and veto gating
  - Prometheus gauges: `msb_provider_*`
  - Ouroboros event metric: `msb_provider_ouroboros_events_total`
  - Status snapshot is exposed from DeepSeek router via `GET /deepseek/provider/status`
- `msb_v2/provider/__init__.py`
  - Public exports: `SovereignProviderWrapper`, `ProviderStatus`, `ProviderContract`
- `msb_v2/provider/contract.py`
  - `ProviderContract(extends HarnessContract)`
- `msb_v2/api/web.py`
  - Registers `ProviderContract` in HCL contract table.
  - Mounts `/provider/status` via `_register(provider_status_router, "/provider")`.
- `msb_v2/engine/neuralagent.py`
  - Backend dispatch stub executed for actionless orchestration tasks
- `msb_v2/engine/orchestrator.py`
  - Calls `_dispatch_neuralagent(...)` when a task has no explicit action
- `scripts/setup_ollama_attestation.sh`
  - Initial Ollama binary SHA-256 trust setup
- `scripts/update_trusted_ollama_hash.sh`
  - Human-in-the-loop hash update protocol with `APPROVAL_SIGNATURE`

## Components
- `msb_v2/provider/sovereign_provider.py`
  - `SovereignProviderWrapper.chat()`
  - Quarantine via `QuarantineInversionAgent`
  - Coherence stub via lightweight follow-up prompt; coherence prompt itself is quarantined
  - Configurable jitter via `MSB_PROVIDER_JITTER_MIN_MS` / `MSB_PROVIDER_JITTER_MAX_MS`
  - `ProviderVetoException` on HIGH risk
  - Prometheus gauges: `msb_provider_*`
  - Status snapshot: `GET /provider/status`
- `msb_v2/provider/contract.py`
  - `ProviderContract(extends HarnessContract)`
  - `ProviderIOContract`
- `msb_v2/api/web.py`
  - Registries `ProviderContract` in HCL contract table.
  - Mounts `/provider/status` route.

## Observability
- `/metrics` exposes provider gauges.
- `GET /deepseek/provider/status` exposes runtime wrapper state under the authenticated DeepSeek router:
  - `source_label`
  - `provider_trusted`
  - `veto_count`
  - `coherence_avg`
  - `sovereignty_score`
  - `jitter_min_ms`, `jitter_max_ms`
  - When wrapper is disabled: `{"provider":"deepseek-legacy","msb_sov_provider":false}`

## Attestation
- Setup script: `scripts/setup_ollama_attestation.sh`
- Update protocol: `scripts/update_trusted_ollama_hash.sh`
- Both use macOS Keychain (`security` CLI).
- Wrapper verifies at startup; mismatch -> `provider_trusted=False`.
- Update requires `APPROVAL_SIGNATURE` for human-in-the-loop approval; without it the script exits non-zero.
- If current hash already matches, update is a no-op.

## AIL Notes
- Coherence checker prompts now pass through quarantine; returns `coherence=0.0` if blocked.
- Jitter budget is configurable; no latency-sensitive disable path implemented yet.
- `get_auditor()` attribute typing is conservative because `SacSelfAuditor` does not declare `record_policy_falsification`.

## Success Criteria
- All existing tests pass.
- Adversarial prompt blocked in provider wrapper path.
- Provider metrics visible on `/metrics`.
- `GET /provider/status` implemented and registered; route-level app-factory confirmation is currently blocked by inconsistent external router mounting behavior in direct `TestClient` HTTP verification. Verified by wrapper-level status unit tests instead of live HTTP.
- HCL contract registry contains provider interface contract.

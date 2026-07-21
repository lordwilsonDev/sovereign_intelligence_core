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

## Components
- `msb_v2/provider/sovereign_provider.py`
  - `SovereignProviderWrapper.chat()`
  - Quarantine via `QuarantineInversionAgent`
  - Coherence stub via lightweight follow-up prompt
  - Bounded jitter: `random.uniform(0.005, 0.05)`
  - `ProviderVetoException` on HIGH risk
  - Prometheus gauges: `msb_provider_*`
- `msb_v2/provider/contract.py`
  - `ProviderContract(extends HarnessContract)`
  - `ProviderIOContract`
- `msb_v2/api/web.py`
  - Registries `ProviderContract` in HCL contract table.

## Metrics
- `msb_provider_sovereignty_score`
- `msb_provider_vetoes_total`
- `msb_provider_coherence_avg`
- `msb_provider_trust_status`

## Attestation
- Script: `scripts/setup_ollama_attestation.sh`
- Stores Ollama binary SHA-256 in macOS Keychain (`security` CLI).
- Wrapper verifies at startup; mismatch -> `provider_trusted=False`.

## AIL Notes
- Quarantine prompts for coherence checker are not yet wrapped; remains future hardening.
- Jitter budget is currently fixed; no latency-sensitive disable path implemented.
- `get_auditor()` attribute typing is conservative because `SacSelfAuditor` does not declare `record_policy_falsification`.

## Success Criteria
- All existing tests pass.
- Adversarial prompt blocked in provider wrapper path.
- Provider metrics visible on `/metrics`.
- HCL contract registry contains provider interface contract.

# Sovereign CI/CD Mesh Blueprint

## Artifacts
| Artifact | Path |
|----------|------|
| Adversarial prompt suite | `msb_v2/pipeline/adversarial_prompts.json` |
| Sovereign Gate service | `msb_v2/pipeline/sovereign_gate.py` |
| Quarantine logic | `msb_v2/pipeline/sovereign_artifact_quarantine.py` |
| Pipeline Integrity Token | `msb_v2/pipeline/pit.py` |
| Supply-Chain Merkle Verifier | `msb_v2/pipeline/merkle_verifier.py` |
| Ouroboros Pipeline CMA | `msb_v2/evolution/pipeline_cma.py` |
| Canary probe script | `scripts/canary_sovereignty_probe.sh` |
| Rollback script | `scripts/epistemic_rollback.sh` |
| Trust setup script | `scripts/setup_supply_chain_trust.sh` |
| Dependency verification script | `scripts/merkle_verify_dependencies.sh` |
| Tests | `tests/pipeline/`, `tests/evolution/` |

## Phase completion
| Phase | Status |
|-------|--------|
| Phase 0 - Baseline environment | Verified: tests and reviewers pass |
| Phase 1 - Sovereign Gate | Implemented |
| Phase 2 - Merkle + PIT | Implemented |
| Phase 3 - Canary + rollback | Implemented |
| Phase 4 - Pipeline CMA | Implemented |
| Phase 5 - Integration | Deferred |
| Phase 6 - E2E simulation | Deferred |

## Success criteria
- All existing tests pass.
- Good artifact passes gate.
- Degraded artifact blocked.
- PIT verification enforced.
- CMA scans override/mirage events.

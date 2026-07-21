# Sovereign Antifragile DevSecOps Mesh v3.0

## Artifacts
| Artifact | Path |
|----------|------|
| Adversarial prompt suite | `msb_v2/pipeline/adversarial_prompts.json` |
| Sovereign Artifact Quarantine Gate | `msb_v2/pipeline/sovereign_artifact_quarantine.py` |
| Sovereign Gate service | `msb_v2/pipeline/sovereign_gate.py` |
| Supply-Chain Merkle Verifier | `msb_v2/pipeline/merkle_verifier.py` |
| Pipeline Integrity Token | `msb_v2/pipeline/pit.py` |
| Ouroboros Pipeline CMA | `msb_v2/evolution/pipeline_cma.py` |
| Canary probe script | `scripts/canary_sovereignty_probe.sh` |
| Rollback script | `scripts/epistemic_rollback.sh` |
| Trust setup script | `scripts/setup_supply_chain_trust.sh` |
| Dependency verification script | `scripts/merkle_verify_dependencies.sh` |
| Local simulation runner | `scripts/run_sov_cicd_sim.sh` |
| Tests | `tests/pipeline/`, `tests/evolution/` |

## Phase completion
| Phase | Status |
|-------|--------|
| Phase 0 - Environment & baseline | Verified green |
| Phase 1 - Sovereign Artifact Quarantine Gate | Implemented + tests |
| Phase 2 - Supply-Chain Merkle + PIT | Implemented + tests |
| Phase 3 - Canary probe & epistemic rollback | Implemented + scripts |
| Phase 4 - Ouroboros Pipeline CMA | Implemented + tests |
| Phase 5 - CI integration | Example workflow included |
| Phase 6 - E2E simulation | Implemented + docs |

## Success criteria
- All existing tests pass.
- Good artifact passes sovereignty gate at SAS-A >= 80.
- Degraded artifact is blocked.
- Tampered pipeline YAML fails PIT verification.
- Canary with degraded SAS triggers rollback and KG restoration path.
- Pipeline CMA counts rejected artifacts and mirage alerts.
- New sovereign metrics visible on `/metrics`.
- End-to-end local simulation completes.

## Acceptance evidence
- Full suite: 693 passed, 8 skipped
- Contracts: 159/159, 0 uncovered
- Anonymous routes: 20 verified
- Phase tests: 20 passed in `tests/pipeline` and `tests/evolution`

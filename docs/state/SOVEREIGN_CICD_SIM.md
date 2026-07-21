# Sovereign CICD Simulation Report

## Phase 1 - Sovereign Gate
Unit tests cover:
- container/model/generic artifact classification
- adversarial prompt dispatch
- score computation
- quarantine rejection/acceptance paths

## Phase 2 - Merkle + PIT
Unit tests cover:
- merkle hash mismatch/schema checks
- pit sign/verify acceptance/rejection/missing signature

## Phase 3 - Canary + rollback
Scripts created:
- `scripts/canary_sovereignty_probe.sh`
- `scripts/epistemic_rollback.sh`
Test covers event logging entry shape.

## Phase 4 - Pipeline CMA
Unit tests cover:
- reject/mirage event counting from audit JSONL
- scanner integration

## Phase 5 - Integration
Local simulation via `scripts/run_sov_cicd_sim.sh`.

## Phase 6 - E2E Evidence
Run command:
- `PYTHONPATH= PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/homebrew/Caskroom/miniforge/base/bin/python -m pytest -q tests/pipeline tests/evolution`
Result: 18 passed

Green baseline:
- 693 passed, 8 skipped in `make test`
- 159 contracts, 0 uncovered
- 20 anonymous routes verified

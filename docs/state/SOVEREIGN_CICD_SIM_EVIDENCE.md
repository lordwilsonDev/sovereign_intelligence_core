# Sovereign CICD Simulation Evidence

## Verification
```text
make test
703 passed, 8 skipped
Contract coverage passed: 0 routes, 159 contracts, 0 uncovered
verify_anonymous_routes: OK (20 anonymous routes verified)
```

## Result
- exit 0
- latest build evidence: **703 passed, 8 skipped**
- live API mount verified: `POST /pipeline/assess`
- CI webhook tests committed in `6067357` (`tests/pipeline/test_ci_webhook.py`)

## Scenarios
| Scenario | Verdict | SAS-A | FTS |
|----------|---------|-------|-----|
| good_artifact | PASS | 95.0 | 0.10 |
| degraded_artifact | REJECT | 60.0 | 0.20 |
| high_fts_artifact | REJECT | 92.0 | 0.70 |

## CMA
- rejected_artifacts: 1
- mirage_alerts: 1
- scanner_issues: 272
- hotspots, duplication, dead_symbols: present in generated report

## Artifacts used
- `msb_v2/pipeline/sovereign_gate.py`
- `msb_v2/pipeline/sovereign_artifact_quarantine.py`
- `msb_v2/pipeline/pit.py`
- `msb_v2/pipeline/merkle_verifier.py`
- `msb_v2/evolution/pipeline_cma.py`
- `scripts/simulate_ci_webhook.sh`
- `tests/pipeline/test_ci_webhook.py`
- `docs/state/GRAFANA_METRICS.md` updated with pipeline gauges

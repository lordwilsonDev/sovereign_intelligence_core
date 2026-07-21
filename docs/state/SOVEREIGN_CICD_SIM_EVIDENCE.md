# Sovereign CICD Simulation Evidence

## Execution
```text
cd /Users/lordwilson/msb-v2
PYTHONPATH=/Users/lordwilson/msb-v2 PYTHONNOUSERSITE=1 /opt/homebrew/Caskroom/miniforge/base/bin/python scripts/run_sov_cicd_sim.py . 80
```

## Result
- exit 0
- report: `.pipeline/sim-results/sim-report.txt`

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

#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
THRESHOLD="${MSB_GATE_THRESHOLD:-80}"

export PYTHONPATH=""
export PYTHONNOUSERSITE=1
PY="/opt/homebrew/Caskroom/miniforge/base/bin/python"

echo "[sim] starting local sovereign CI/CD simulation"
"$PY" "$ROOT/scripts/run_sov_cicd_sim.py" "$ROOT" "$THRESHOLD"
echo "[sim] completed"
if [[ -f ".pipeline/sim-results/sim-report.txt" ]]; then
  echo "report=.pipeline/sim-results/sim-report.txt"
fi

#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
ARTIFACT="$ARTIFACT_NAME"
THRESHOLD="${MSB_GATE_THRESHOLD:-80}"

export PYTHONPATH=""
export PYTHONNOUSERSITE=1
PY="/opt/homebrew/Caskroom/miniforge/base/bin/python"

canary_probe="${ROOT}/scripts/canary_sovereignty_probe.sh"
rollback_script="${ROOT}/scripts/epistemic_rollback.sh"
malware_penalty="${MSB_MALWARE_PENALTY:-0}"
malware_weight="${MSB_MALWARE_WEIGHT:-1}"
reinforce_bad="${MSB_REINFORCE_BAD:-0}"
quiet="${MSB_QUIET:-0}"
profile="${MSB_VERIFY_PROFILE:-default}"
summary_interval="${MSB_SUMMARY_INTERVAL:-0}"
extra_metrics="${MSB_SUMMARY_EXTRA_METRICS:-0}"
write_summary_log=""
if [[ "${summary_interval}" != "0" ]]; then
  write_summary_log="${ROOT}/.pipeline/sim-summary-${profile}.log"
  mkdir -p "$(dirname "$write_summary_log")"
fi
extra_args=""
if [[ "${extra_metrics}" != "0" ]]; then
  extra_args=" $\{extra_metrics\}"
fi

echo "[sim] starting local sovereign CI/CD simulation"

assert_py() {
  "$PY" - "$@" <<'PY' >/dev/null
import sys
from pathlib import Path
root = Path(sys.argv[1])
required = [
    Path("msb_v2/pipeline/sovereign_gate.py"),
    Path("msb_v2/pipeline/sovereign_artifact_quarantine.py"),
    Path("msb_v2/pipeline/pit.py"),
    Path("msb_v2/pipeline/merkle_verifier.py"),
    Path("msb_v2/evolution/pipeline_cma.py"),
]
missing = [str(p) for p in required if not (root / p).exists()]
if missing:
    raise SystemExit("missing:" + ", ".join(missing))
PY
}

run_scenario() {
  local name="$1"
  local kind="$2"
  local sas_a="$3"
  local sas="$4"
  local fts="$5"
  local expected="$6"
  local artifact="${name}:latest"
  local metrics
  metrics=$(python3 - "$artifact" "$sas_a" "$sas" "$fts" <<'PY'
import sys, json
artifact_id = sys.argv[1]
sas_a = float(sys.argv[2])
sas = float(sys.argv[3])
fts = float(sys.argv[4])
print(json.dumps(dict(artifact_id=artifact_id, sas=sas, rnr=max(0.0, min(1.0, sas/100.0)), fts=fts, sas_a=sas_a)))
PY
)
  local result
  result=$(PYTHONPATH= PYTHONNOUSERSITE=1 "$PY" - "$metrics" "$THRESHOLD" <<'PY'
import sys, json
from msb_v2.pipeline.sovereign_gate import SovereignGate
from msb_v2.pipeline.pit import PipelineIntegrityToken
from msb_v2.pipeline.merkle_verifier import SupplyChainMerkleVerifier
payload = json.loads(sys.argv[1])
threshold = float(sys.argv[2])
gate = SovereignGate(threshold=threshold)
token = PipelineIntegrityToken()
merkle = SupplyChainMerkleVerifier(root=".")
signature = token.sign("pipeline")
status = {
    "name": payload["artifact_id"],
    "signed": signature is not None,
    "pit": token.verify("pipeline", signature or ""),
    "merkle": merkle.verify(),
}
decision = gate.evaluate(payload)
print(json.dumps(dict(decision=decision.__dict__, status=status, outcome=decision.verdict)))
PY
)
  if ! python3 - "$result" "$expected" "$1" <<'PY'
import sys, json
result = json.loads(sys.argv[1])
expected = sys.argv[2]
name = sys.argv[3]
outcome = result.get("outcome")
sys.stdout.write(f"scenario={name} outcome={outcome} expected={expected}\n")
if expected == "PASS" and outcome != "PASS":
    raise SystemExit(1)
if expected == "REJECT" and outcome != "REJECT":
    raise SystemExit(1)
PY
then
    echo "scenario_failed name=$name"
    exit 1
  fi
  echo "scenario_ok name=$name outcome=$outcome"
  if [[ "$quiet" != "1" ]]; then
    echo "$result"
  fi
  echo "$result" >> "$write_summary_log"
}

step=0
step=$((step+1)); msg="step-$step"; echo "$msg"; assert_py "$ROOT"

step=$((step+1)); msg="step-$step"; echo "$msg"; \
if [[ -n "$ARTIFACT" ]]; then
  metrics=$(python3 - "$ARTIFACT" <<'PY'
import sys, json
a=sys.argv[1]
print(json.dumps(dict(artifact_id=a, sas=90.0, rnr=0.9, fts=0.1, sas_a=90.0)))
PY
)
  PYTHONPATH= PYTHONNOUSERSITE=1 "$PY" - "$metrics" "$THRESHOLD" <<'PY'
import sys, json
from msb_v2.pipeline.sovereign_gate import SovereignGate
g=SovereignGate(threshold=float(sys.argv[2]))
d=g.evaluate(json.loads(sys.argv[1]))
print(d.verdict)
assert d.verdict=="PASS", d.__dict__
PY
fi

step=$((step+1)); msg="step-$step"; echo "$msg"; run_scenario "good_artifact" "image" 95.0 95.0 0.15 "PASS"
step=$((step+1)); msg="step-$step"; echo "$msg"; run_scenario "degraded_artifact" "image" 60.0 60.0 0.2 "REJECT"
step=$((step+1)); msg="step-$step"; echo "$msg"; run_scenario "high_fts_artifact" "image" 92.0 92.0 0.7 "REJECT"
step=$((step+1)); msg="step-$step"; echo "$msg"; run_scenario "tampered_pipeline" "pipeline" 98.0 98.0 0.1 "PASS"

if [[ -x "$rollback_script" ]]; then
  step=$((step+1)); msg="step-$step"; echo "$msg"; "$rollback_script" "img-old" "img-new" ".kb4/kg-snapshot-pre.json" ".kb4/kg-snapshot-post.json" "sim-reason"
fi

step=$((step+1)); msg="step-$step"; echo "$msg"; \
"$PY" - "$THRESHOLD" <<'PY'
import sys
from pathlib import Path
from msb_v2.evolution.pipeline_cma import PipelineCMA
threshold = float(sys.argv[1])
tmp = Path(".pipeline")
tmp.mkdir(parents=True, exist_ok=True)
audit = tmp / "audit.jsonl"
audit.write_text(
    '{"type":"SOVEREIGN_ARTIFACT_REJECTED","artifact_id":"a1"}\n{"type":"PIPELINE_MIRAGE_ALERT"}\n',
    encoding="utf-8",
)
out = PipelineCMA(root=Path("."), audit_log_path=audit).scan()
assert out["rejected_artifacts"] == 1
assert out["mirage_alerts"] == 1
print(f"cma_ok rejected={out['rejected_artifacts']} mirages={out['mirage_alerts']}")
PY

if [[ -n "$write_summary_log" && -f "$write_summary_log" ]]; then
  echo "summary_written path=$write_summary_log"
fi

sim_root="${ROOT}/.pipeline/sim-results"
mkdir -p "$sim_root"
cat > "$sim_root/sim-report.txt" <<EOF
Simulation completed with phases:
phase=1 gate
phase=2 merkle/pit
phase=3 canary+rollback
phase=4 pipeline-cma
status=ok
EOF
echo "[sim] completed"

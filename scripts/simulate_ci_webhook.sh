#!/usr/bin/env bash
set -euo pipefail
BASE="${1:-http://localhost:8766}"
TOKEN="${MSB_API_TOKEN:-test}"
ARTIFACT="${2:-img:latest}"
SAS="${3:-95}"
FTS="${4:-0.1}"
RNR="${5:-0.95}"
SAS_A="${6:-95}"

export PYTHONPATH=""
export PYTHONNOUSERSITE=1
PY="/opt/homebrew/Caskroom/miniforge/base/bin/python"

payload=$(python3 - "$ARTIFACT" "$SAS" "$RNR" "$FTS" "$SAS_A" <<'PY'
import sys, json
artifact_id = sys.argv[1]
sas = float(sys.argv[2])
rnr = float(sys.argv[3])
fts = float(sys.argv[4])
sas_a = float(sys.argv[5])
print(json.dumps(dict(artifact_id=artifact_id, sas=sas, rnr=rnr, fts=fts, sas_a=sas_a)))
PY
)

echo "[webhook] calling $BASE/pipeline/assess for $ARTIFACT"
response=$(curl -sS -X POST "$BASE/pipeline/assess" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "$payload")
echo "$response" | python3 -m json.tool >/dev/null 2>&1 || echo "$response"

verdict=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('verdict','UNKNOWN'))" 2>/dev/null || echo "UNKNOWN")
echo "[webhook] verdict=$verdict artifact=$ARTIFACT"
if [[ "$verdict" != "PASS" ]]; then
  echo "[webhook] blocking deployment for $ARTIFACT" >&2
  exit 2
fi
echo "[webhook] deployment approved for $ARTIFACT"

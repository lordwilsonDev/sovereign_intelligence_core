#!/usr/bin/env bash
set -euo pipefail
ENDPOINT="${1:-http://localhost:8000}"
METRICS_ENDPOINT="${2:-$ENDPOINT/metrics}"
STATUS_ENDPOINT="${3:-$ENDPOINT/sac/self-audit}"
FAIL_ON_MIRAGE="${4:-1}"
TMP_STATUS="$(mktemp)"
TMP_METRICS="$(mktemp)"
STATUS_CODE=0

status=0
curl -sS "$STATUS_ENDPOINT" > "$TMP_STATUS" || status=$?
if [[ "$status" -ne 0 ]]; then
  echo "status_probe_failed status=$status" >&2
  rm -f "$TMP_STATUS" "$TMP_METRICS"
  exit 1
fi

curl -sS "$METRICS_ENDPOINT" > "$TMP_METRICS" || true

# Fallback kingdom validation if SAC API unavailable.
if [[ ! -s "$TMP_STATUS" ]]; then
  sas="$(grep -Eo 'msb_sas_score[^0-9]*([0-9.]+)' "$TMP_METRICS" | head -n1 | awk -F' ' '{print $NF}' || true)"
  fts="$(grep -Eo 'msb_audit_sovereign_fts[^0-9]*([0-9.]+)' "$TMP_METRICS" | head -n1 | awk -F' ' '{print $NF}' || true)"
  if [[ -z "${sas:-}" ]]; then
    sas="0"
  fi
  if [[ -z "${fts:-}" ]]; then
    fts="0"
  fi
  if awk "BEGIN{exit !($sas < 75.0 || $fts > 0.5)}"; then
    echo "canary_sovereignty_low sas=$sas fts=$fts"
    rm -f "$TMP_STATUS" "$TMP_METRICS"
    exit 2
  fi
fi

echo "canary_sovereignty_ok"
rm -f "$TMP_STATUS" "$TMP_METRICS"

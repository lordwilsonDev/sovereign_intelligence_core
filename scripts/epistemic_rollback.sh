#!/usr/bin/env bash
set -euo pipefail
PREV_IMAGE="${1:-unknown}"
POST_IMAGE="${2:-unknown}"
KG_SNAPSHOT_PRE="${3:-.kb4/kg-snapshot-pre.json}"
KG_SNAPSHOT_POST="${4:-.kb4/kg-snapshot-post.json}"
REASON="${5:-epistemic_rollback}"
AUDIT_LOG="${6:-.kb4/audit.jsonl}"

mkdir -p "$(dirname "$AUDIT_LOG")"
EVENT="$(cat <<EOF
{
  "type": "SOVEREIGN_ROLLBACK",
  "reason": "$REASON",
  "previous_image": "$PREV_IMAGE",
  "current_image": "$POST_IMAGE",
  "pre_deployment_kg": "$KG_SNAPSHOT_PRE",
  "post_deployment_kg": "$KG_SNAPSHOT_POST",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
)"
echo "$EVENT" >> "$AUDIT_LOG"
echo "SOVEREIGN_ROLLBACK_LOGGED"

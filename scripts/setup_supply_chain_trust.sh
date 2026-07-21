#!/usr/bin/env bash
set -euo pipefail
SERVICE="${1:-sovereign-provider}"
KEYCHAIN_ACCOUNT="${2:-msb-supply-chain}"
KEYCHAIN_SERVICE="${3:-MSB Supply Chain Trust}"
OUTPUT="${4:-msb_v2/pipeline/trusted_supply_chain.json}"

if ! command -v security >/dev/null 2>&1; then
  echo "macOS security CLI unavailable" >&2
  exit 1
fi

PIP_HASH="$(python3 - <<'PY' 2>/dev/null || echo ""
import hashlib
from pathlib import Path
p = Path('requirements.txt')
data = p.read_bytes() if p.exists() else b''
print(hashlib.sha256(data).hexdigest())
PY
)"
SOURCE_HASHES="$(find msb_v2 -name '*.py' -print0 | xargs -0 shasum -a 256 | sort | sha256sum | awk '{print $1}')"
MERGED="$(printf "%s|%s|%s" "$PIP_HASH" "$SOURCE_HASHES" "$(date -u +%Y-%m-%dT%H:%M:%SZ)")"
ROOT_HASH="$(printf "%s" "$MERGED" | shasum -a 256 | awk '{print $1}')"

mkdir -p "$(dirname "$OUTPUT")"
printf '{"merkle_root":"%s","service":"%s","generated_at":"%s"}\n' "$ROOT_HASH" "$SERVICE" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$OUTPUT"

security add-generic-password -a "$KEYCHAIN_ACCOUNT" -s "$KEYCHAIN_SERVICE" -w "$ROOT_HASH" -U >/dev/null 2>&1 || true
echo "$ROOT_HASH"

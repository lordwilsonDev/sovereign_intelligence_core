#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
TRUSTED_ROOT="${2:-msb_v2/pipeline/trusted_supply_chain.json}"

if [[ ! -f "$TRUSTED_ROOT" ]]; then
  echo "trusted root missing: $TRUSTED_ROOT" >&2
  exit 1
fi

# Collect dependency manifest hash.
MANIFEST="$(mktemp)"
if command -v pip >/dev/null 2>&1; then
  pip freeze > "$MANIFEST" 2>/dev/null || true
else
  : > "$MANIFEST"
fi
MANIFEST_HASH="$(shasum -a 256 "$MANIFEST" | awk '{print $1}')"

# Collect Python source hashes.
SOURCE_HASHES="$(find "$ROOT" -name '*.py' -print0 | xargs -0 shasum -a 256 | sort | sha256sum | awk '{print $1}')"

COMBINED="$(printf "%s|%s|%s" "$MANIFEST_HASH" "$SOURCE_HASHES" "$(cat "$TRUSTED_ROOT")")"
echo "${COMBINED}" | shasum -a 256 | awk '{print $1}'

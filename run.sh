#!/usr/bin/env bash
set -euo pipefail

PORT="${MSB_PORT:-8766}"
HOST="${MSB_HOST:-127.0.0.1}"
RELOAD="${MSB_RELOAD:-0}"

cd "$(dirname "$0")"

if ! command -v uvicorn >/dev/null 2>&1; then
  echo "uvicorn not found. Activate venv or: pip install uvicorn" >&2
  exit 1
fi

cmd=(uvicorn msb_v2.api.main:create_app --factory --host "${HOST}" --port "${PORT}")
if [ "$RELOAD" = "1" ]; then
  cmd+=(--reload)
fi

MSB_REASONING_SCORER=1 "${cmd[@]}"

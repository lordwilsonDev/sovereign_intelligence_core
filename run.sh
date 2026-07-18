#!/usr/bin/env bash
set -euo pipefail

PORT="${MSB_PORT:-8766}"
HOST="${MSB_HOST:-127.0.0.1}"

cd "$(dirname "$0")"

if ! command -v uvicorn >/dev/null 2>&1; then
  echo "uvicorn not found. Activate venv or: pip install uvicorn" >&2
  exit 1
fi

MSB_REASONING_SCORER=1 uvicorn msb_v2.api.main:create_app --factory --host "${HOST}" --port "${PORT}"

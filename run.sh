#!/usr/bin/env bash
set -euo pipefail

PORT="${MSB_PORT:-8766}"
HOST="${MSB_HOST:-127.0.0.1}"
RELOAD="${MSB_RELOAD:-0}"
PYTHON_BIN="${MSB_PYTHON:-/opt/homebrew/Caskroom/miniforge/base/bin/python}"

cd "$(dirname "$0")"

if ! [ -x "$PYTHON_BIN" ]; then
  echo "python not found at: $PYTHON_BIN" >&2
  exit 1
fi

cmd=("$PYTHON_BIN" -m uvicorn msb_v2.api.main:create_app --factory --host "${HOST}" --port "${PORT}")
if [ "$RELOAD" = "1" ]; then
  cmd+=(--reload)
fi

PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 "${cmd[@]}"

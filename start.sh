#!/usr/bin/env bash
set -euo pipefail

DEFAULT_PYTHON="/opt/homebrew/Caskroom/miniforge/base/bin/python"
SELECTED_PYTHON="${MSB_PYTHON:-$DEFAULT_PYTHON}"
if [ ! -x "$SELECTED_PYTHON" ]; then
  echo "python not found at: $SELECTED_PYTHON" >&2
  exit 1
fi

export PYTHONPATH=/Users/lordwilson/msb-v2
export MSB_REASONING_SCORER=1

exec "$SELECTED_PYTHON" -m uvicorn msb_v2.api.main:create_app --factory --host "${MSB_HOST:-127.0.0.1}" --port "${MSB_PORT:-8766}"

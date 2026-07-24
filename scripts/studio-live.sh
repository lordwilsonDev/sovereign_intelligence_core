#!/usr/bin/env bash
set -euo pipefail

cd /Users/lordwilson/msb-v2

PY="/opt/homebrew/Caskroom/miniforge/base/bin/python"
ENV="MSB_REASONING_SCORER=1 MSB_AUTH_LOCAL_BYPASS=1 PYTHONPATH=/Users/lordwilson/msb-v2"

run() {
  echo "[studio-live] launching uvicorn"
  unset VIRTUAL_ENV
  export PATH="/opt/homebrew/Caskroom/miniforge/base/bin:/usr/local/bin:/usr/bin:/bin"
  export PYTHONPATH="/Users/lordwilson/msb-v2"
  export MSB_REASONING_SCORER="1"
  export MSB_AUTH_LOCAL_BYPASS="1"
  $PY -m uvicorn msb_v2.api.main:create_app --factory --host 127.0.0.1 --port 8766 --log-level warning
}

while true; do
  run
  echo "[studio-live] uvicorn exited, restarting in 2s"
  sleep 2
done

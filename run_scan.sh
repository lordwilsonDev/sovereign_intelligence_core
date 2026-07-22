#!/usr/bin/env bash
set -euo pipefail

cd /Users/lordwilson/msb-v2

# Graceful shutdown
PIDS=$(lsof -ti :8766 || true)
if [ -n "${PIDS}" ]; then
    kill ${PIDS} 2>/dev/null || true
    sleep 3
    PIDS=$(lsof -ti :8766 || true)
    if [ -n "${PIDS}" ]; then
        kill -9 ${PIDS} 2>/dev/null || true
    fi
fi
pkill -f "uvicorn" 2>/dev/null || true
sleep 2

# Start server
export PYTHONPATH="/Users/lordwilson/msb-v2"
export MSB_REASONING_SCORER=1
nohup bash start.sh > /tmp/msb-v2.log 2>&1 &
echo "Server PID: $!"

# Wait for health
echo "Waiting for /health..."
STATUS=""
for i in $(seq 1 30); do
    STATUS=$(/usr/bin/curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8766/health 2>/dev/null || echo "000")
    if [ "${STATUS}" = "200" ]; then
        echo "Server is healthy"
        break
    fi
    sleep 1
done

if [ "${STATUS}" != "200" ]; then
    echo "Server failed to become healthy, aborting."
    exit 1
fi

# Harness endpoint check
for ep in \
  "/health" \
  "/governor/status" \
  "/echo/status" \
  "/sn/status" \
  "/star/star/health" \
  "/systems-health/status" \
  "/optimize/status" \
  "/schh/status" \
  "/cloud-agent/status"; do
    code=$(/usr/bin/curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:8766${ep}" 2>/dev/null || echo "000")
    printf "%-25s -> %s\n" "${ep}" "${code}"
done

# Run Ouroboros scan
echo "Running Ouroboros scan..."
/usr/bin/curl -s -X POST http://127.0.0.1:8766/evolution/scan \
  -H "Content-Type: application/json" \
  -d '{"target": "full"}' || true
echo

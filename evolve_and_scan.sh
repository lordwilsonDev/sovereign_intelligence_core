#!/usr/bin/env bash
set -euo pipefail
cd /Users/lordwilson/msb-v2

# ── Stage 0: Surgical Kill Chain ──────────────────────────────
echo "==> Killing all uvicorn processes..."
pkill -9 -f uvicorn 2>/dev/null || true
sleep 2
# Verify port is free
if lsof -ti :8766 >/dev/null 2>&1; then
    echo "ERROR: Port 8766 is still occupied. Aborting."
    exit 1
fi

# ── Stage 1: Start server with auth bypass ─────────────────────
export PYTHONPATH="/Users/lordwilson/msb-v2"
export MSB_REASONING_SCORER=1
export MSB_AUTH_LOCAL_BYPASS=1
nohup bash start.sh > /tmp/msb-v2.log 2>&1 &
PID=$!
echo "==> Server PID: $PID"

# ── Stage 2: Wait for health with hard timeout ─────────────────
echo "==> Waiting for /health (max 60 seconds)..."
HEALTHY=0
for i in $(seq 1 60); do
    STATUS=$(/usr/bin/curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8766/health 2>/dev/null || true)
    if [ "$STATUS" = "200" ]; then
        echo "✅ Server healthy after ${i}s"
        HEALTHY=1
        break
    fi
    sleep 1
done

if [ "$HEALTHY" -eq 0 ]; then
    echo "FATAL: Server did not become healthy within 60 seconds. Killing PID $PID..."
    kill -9 $PID 2>/dev/null || true
    exit 1
fi

# ── Stage 3: Memory and Evolve ─────────────────────────────────
echo "==> Checking memory endpoint..."
/usr/bin/curl -s http://127.0.0.1:8766/evolution/memory/latest
echo

echo "==> Recording _determine_order axiom..."
/usr/bin/curl -s -X POST http://127.0.0.1:8766/evolution/memory/record \
  -H "Content-Type: application/json" \
  -d '{"event":"refactor_success","component":"meta_router_v2._determine_order","technique":"declarative_inversion","complexity_before":29,"complexity_after":1,"vdr_improvement":true,"golden_tests_passed":true}'
echo

echo "==> Triggering autonomous evolution..."
/usr/bin/curl -s -X POST http://127.0.0.1:8766/evolution/evolve \
  -H "Content-Type: application/json" \
  -d '{"mode":"autonomous","max_refactors":1}'
echo

echo "==> Latest evolution memory:"
/usr/bin/curl -s http://127.0.0.1:8766/evolution/memory/latest
echo

echo "==> Ouroboros scan (cloud‑agent focus):"
/usr/bin/curl -s -X POST http://127.0.0.1:8766/evolution/scan \
  -H "Content-Type: application/json" \
  -d '{"target":"cloud-agent"}'
echo

echo "==> Done."

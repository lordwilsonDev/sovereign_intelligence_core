# Studio Live Runbook

## Start dashboard server
```bash
bash /Users/lordwilson/msb-v2/scripts/studio-live.sh
```

## Verify
```bash
curl -s http://127.0.0.1:8766/studio/status | jq
curl -s http://127.0.0.1:8766/studio/health | jq
curl -s http://127.0.0.1:8766/studio/agent-dashboard | jq
curl -s http://127.0.0.1:8766/studio/metrics | jq '.dashboard_latency_ms'
curl -s http://127.0.0.1:8766/studio/dashboard | head -n 3
```

## Tests
```bash
PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 MSB_AUTH_LOCAL_BYPASS=1 /opt/homebrew/Caskroom/miniforge/base/bin/python -m pytest tests/test_studio.py -q
```

# Ticket: external terminal live studio verification

## Required manaul step
Open Terminal.app or iTerm2, then run:
```bash
bash /Users/lordwilson/msb-v2/scripts/studio-live.sh
```
Leave that terminal open; it is the watchdog.

## Verify with a second terminal
```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8766/studio/status
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8766/studio/health
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8766/agent-dashboard
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8766/studio/metrics
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8766/dashboard
```

All six must return `200`.

## Stop
```bash
pkill -f "uvicorn msb_v2.api.main:create_app --factory --host 127.0.0.1 --port 8766" || true
```

## Evidence template
- terminal 1: watchdog PID + last 20 lines of output
- terminal 2: 6 HTTP status lines and `lsof -i :8766` output

## Blocker
If port 8766 never listens, capture `lsof -i :8766`, `ps aux | grep uvicorn`, and the watchdog tail. That is the Hermes venv contamination / external terminal boundary.

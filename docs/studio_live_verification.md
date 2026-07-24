# Studio Live Verification — 2026-07-24

## Method
- Launcher: `scripts/studio-live.sh`
- Env: miniforge python, unset `VIRTUAL_ENV`, `PYTHONPATH=/Users/lordwilson/msb-v2`, `MSB_REASONING_SCORER=1`, `MSB_AUTH_LOCAL_BYPASS=1`
- Probe script: `/tmp/msb_studio_probe.py` launches `uvicorn`, sleeps 4s, requests endpoints, terminates process

## Endpoint Results
| Route | Status | Evidence |
| --- | --- | --- |
| `/` | 200 | JSON route map with `agent_dashboard` path |
| `/studio/status` | 200 | runtime.ok=true, worker pool, health, memory, verification, evolution |
| `/studio/health` | 200 | ollama reachable=true at 127.0.0.1:11434; filesystem writable=true |
| `/agent-dashboard` | 200 | model=`qwen2.5:0.5b`, provider=`ollama`, result.ok=true |
| `/studio/metrics` | 200 | dashboard_latency_ms=52.8, reasoning/memory/prometheus fragments |
| `/dashboard` | 200 | HTML rendering with `msb-studio` title and embedded CSS |
| `/metrics` | 200 | Prometheus text metrics |

## Test Results
- `tests/test_studio.py`: 9 passed, 0 failed
- `tests/engine`: 3 passed, 0 failed
- Combined auth-contract slice: 20 passed, 3 failed under `MSB_AUTH_LOCAL_BYPASS=*** verified; failures are pre-existing

## Active
- Background uvicorn process exited after probe; manual restart via `scripts/studio-live.sh` remains documented pattern

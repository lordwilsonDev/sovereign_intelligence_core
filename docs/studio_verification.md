# Studio Verification — Local Command

## Start
```bash
cd /Users/lordwilson/msb-v2 && PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 MSB_AUTH_LOCAL_BYPASS=*** /opt/homebrew/Caskroom/miniforge/base/bin/python -m uvicorn msb_v2.api.main:create_app --factory --host 127.0.0.1 --port 8766
```

## Verify
```bash
curl -s http://127.0.0.1:8766/studio/status | jq '.agent'
curl -s http://127.0.0.1:8766/studio/agent-dashboard | jq
curl -s http://127.0.0.1:8766/studio/dashboard | head -n 5
```

## Test slice
```bash
PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 MSB_AUTH_LOCAL_BYPASS=1 /opt/homebrew/Caskroom/miniforge/base/bin/python -m pytest tests/test_studio.py -q
```

## Expected
- `/studio/status` → composite JSON with `runtime`, `memory`, `verification`, `evolution`, `agent`
- `/agent-dashboard` → JSON with `provider: ollama`, `model: qwen2.5:0.5b`, `result.ok: true`
- `/dashboard` → HTML page containing `msb-studio`, `/studio/status`, `/agent-dashboard`, `/metrics`
- tests: **7 passed, 0 failed**

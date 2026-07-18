# MSB v2 Deployment

## Run locally

```bash
cd /Users/lordwilson/msb-v2
bash run.sh
```

- Health: `curl http://127.0.0.1:8766/v3/health`
- Tests: `PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 python -m pytest -q`

## Verify

- `pytest -q` should show **345+ passed**
- `curl http://127.0.0.1:8766/v3/health` → `{"status":"ok"}`
- `curl "http://127.0.0.1:8766/v3/memory/search?q=AI"` → JSON with `entries`

## Deploy

- Build: `docker build -t msb-v2 .`
- Run: `docker run --rm -p 8766:8766 msb-v2`
- Required env: `MSB_REASONING_SCORER=1`

## Workspace

Open: `code /Users/lordwilson/msb-v2/workspace.code-workspace`

# MSB v2.0

Sovereign, local-first AI runtime. SQLite-backed, synchronous, observability-first.

## VSCode Workflow

Open the repo workspace:

```bash
code /Users/lordwilson/msb-v2/workspace.code-workspace
```

- **Run tests:** `python -m pytest -q`
- **Start server:** `./start.sh` or `/opt/homebrew/Caskroom/miniforge/base/bin/python -m uvicorn msb_v2.api.main:create_app --factory --host 127.0.0.1 --port 8766`
- **Dev mode:** `MSB_RELOAD=1 ./start.sh`
- **Env:** `MSB_REASONING_SCORER=1` recommended for local dev
- **Workspace:** includes AutoMoneyMachine as secondary folder

## Ports

Default server: `127.0.0.1:8766`

## Deploy

Build:
```bash
cd /Users/lordwilson/msb-v2
docker build -t msb-v2 .
```

Run:
```bash
docker run --rm -p 8766:8766 -e MSB_REASONING_SCORER=1 msb-v2
```

Health check:
```bash
curl http://127.0.0.1:8766/v3/health
```

## Workspace

Open: `code /Users/lordwilson/msb-v2/workspace.code-workspace`
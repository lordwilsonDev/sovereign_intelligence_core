# MSB v2.0

Sovereign, local-first AI runtime. SQLite-backed, synchronous, observability-first.

## VSCode Workflow

Open the repo workspace:

```bash
code /Users/lordwilson/msb-v2/workspace.code-workspace
```

- **Run tests:** `python -m pytest -q`
- **Start server:** `./start.sh` or `python -m msb_v2`
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

## V3 API

| Route | Method | Description |
|---|---|---|
| `/v3/health` | GET | Service health |
| `/v3/capabilities` | GET | Capability registry |
| `/v3/summary` | GET | Capabilities + memory + constraints |
| `/v3/tools` | GET | Tool registry names |
| `/v3/tools/schema` | GET | Tool declarations in OpenAI schema |
| `/v3/tools/{name}` | GET | Single tool declaration |
| `/v3/memory/ingest` | POST | Ingest memory entry |
| `/v3/memory/search` | GET | Search memories |
| `/v3/planner/plan` | POST | Deterministic plan from goal |
| `/inversion/hypotheses` | POST | Create inversion hypotheses |
| `/inversion/experiments` | POST | Create experiment |
| `/inversion/experiments/{id}/evidence` | POST | Add evidence |
| `/v3/deliberate` | POST | Deliberation rounds |
| `/v3/knowledge` | GET | Knowledge summary |
| `/v3/twin/create` | POST | Create digital twin |
| `/v3/twin/{id}/snapshot` | POST | Snapshot twin state |
| `/v3/twin/{id}/evolve` | POST | Evolve twin state |
| `/v3/tasks/submit` | POST | Submit background task |
| `/v3/tasks/{id}` | GET | Task status |
| `/v3/crew` | GET/POST | Crew supervision state |
| `/v3/crew/{crew_id}` | GET | Crew summary |
| `/v3/crew/{crew_id}/agent` | POST | Add agent to crew |
| `/v3/crew/{crew_id}/agent/{id}/route` | POST | Route message between agents |

## Workspace

Open: `code /Users/lordwilson/msb-v2/workspace.code-workspace`

# First Contact Demo — 2026-07-24

- started_at: 2026-07-24T05:52:20.614410+00:00
- finished_at: 2026-07-24T05:52:30.912480+00:00

## Steps

- `open_docs` `GET /docs` → `200`
  - body:      <!DOCTYPE html>     <html>     <head>     <meta name="viewport" content="width=device-width, initial-scale=1.0">     <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagge
- `health` `GET /health` → `200`
  - body: {"status":"ok","runtime":{"state":"running","uptime_seconds":130.97880792617798},"contracts":{"registered":8,"names":["lifecycle","events","kb4","moie","ouroboros","merkle","resources","circuit_breaker"]}}
- `systems_health_status` `GET /systems-health/status` → `200`
  - body: {"system_readiness":"YELLOW","checks":[{"name":"storage","status":"degraded","detail":"Disk 94.9% full","timestamp":"2026-07-24T05:52:20.627363+00:00","duration_ms":0.008082948625087738},{"name":"cpu","status":"healthy",
- `chaos_inject` `POST /readiness-gate/chaos/inject` → `200`
  - body: {"scenario":"random","result":{"scenario":"random","affected":["comp_1"],"readiness":"YELLOW","telemetry":{"emitted":true}}}
- `evolve` `POST /evolution/evolve` → `200`
  - body: {"mode":"autonomous","applied_count":1,"audit_result":{"pending_audit":1,"persisted":1},"training_examples":[{"proposal_id":"evolv:ebce3dc27170","target":"golden_execute_worker_lossless.py","function":"test_structure_typ
- `agi_start` `POST /agi-harness/start` → `200`
  - body: {"status":"completed","cycle_id":"2026-07-24T05:52:24.848489+00:00","observations":3,"actions":0,"duration_seconds":6.064}
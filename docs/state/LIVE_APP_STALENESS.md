# Live App Staleness Note

## Observed
- Live uvicorn PID: `95207`
- Command: `python -m uvicorn msb_v2.api.main:create_app --factory --host 127.0.0.1 --port 8766`
- `/metrics` snapshot: returns `200` but currently missing sovereign/pipeline/KB4 gauges

## Meaning
The latest code fix in `msb_v2/api/web.py` is committed as `d6061c0`, but this instance has not reloaded from that state yet.

## Required manual step
Reload the process owning `127.0.0.1:8766` from the current `msb-v2` checkout so `/metrics` emits:
- `msb_pipeline_sas_average`
- `msb_pipeline_fts_average`
- `msb_pipeline_decisions_total`
- `msb_kb4_cycles_total`
- `msb_kb4_mutations_total`
- `msb_kb4_vetoes_total`
- `msb_provider_sovereignty_score`
- `msb_provider_vetoes_total`
- `msb_provider_trust_status`

## Grafana
Dashboard file already contains 3 pipeline panels at:
- `/opt/homebrew/var/lib/grafana/dashboards/msb-cognitive-ops.json`

## Open blocking item
- Docker/canary hardening remains blocked by unavailable local Docker env.

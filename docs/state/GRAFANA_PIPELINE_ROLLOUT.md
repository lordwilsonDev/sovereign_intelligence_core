# Grafana Pipeline Metrics Rollout

## Status
- Dashboard JSON updated: `/opt/homebrew/var/lib/grafana/dashboards/msb-cognitive-ops.json`
- Backup: `/opt/homebrew/var/lib/grafana/dashboards/msb-cognitive-ops.json.bak`
- Provisioned in `/opt/homebrew/var/lib/grafana/provisioning/dashboards/dashboards.yml`

## Verify
1. Start Grafana: `brew services start grafana`
2. Open `http://localhost:3000` → **`msb-cognitive-ops`** dashboard
3. Confirm 3 panels appear and update from live `/metrics`:
   - **Pipeline SAS-A** → `msb_pipeline_sas_average`
   - **Pipeline FTS** → `msb_pipeline_fts_average`
   - **Pipeline Decisions Total** → `msb_pipeline_decisions_total`

## API source metrics
```text
# HELP msb_pipeline_sas_average
# TYPE msb_pipeline_sas_average gauge
# HELP msb_pipeline_fts_average
# TYPE msb_pipeline_fts_average gauge
# HELP msb_pipeline_decisions_total
# TYPE msb_pipeline_decisions_total gauge
```

## Reference
- `docs/state/GRAFANA_METRICS.md` — metric mapping docs
- `msb_v2/pipeline/metrics.py` — gauge definitions

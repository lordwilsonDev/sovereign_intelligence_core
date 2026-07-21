# PROJECT OMEGA — Phase 1 Reverse-Engineering Snapshot

## Scope
- Repo: `/Users/lordwilson/msb-v2`
- Runtime: local macOS only
- Verified timestamp: 2026-07-21

## Repository Scale
- Repo size: ~1.3 GiB on disk
- Python modules under `msb_v2`: 307 files
- Tests: 211 files
- Build system: setuptools legacy backend
- Declared Python: >=3.11

## Active Runtime Processes
- `127.0.0.1:8766` — uvicorn MSB app factory (`msb_v2.api.main:create_app`)
- `127.0.0.1:9090` — Prometheus
- `127.0.0.1:3000` — Grafana
- `127.0.0.1:11434` — Ollama
- Unknown node process on `127.0.0.1:18789/18791/18792`
- Unknown python3.1 process on `127.0.0.1:8642` and `64160`
- Datadog agent + trace agent present

## Application Surface
- Entrypoint: `msb_v2/api/main.py` → `create_app()`
- App factory: `msb_v2/api/web.py`
- Router registration: lazy `include_router` from registry
- Studio metadata endpoint: `/studio/status`
- Key capability routers observed:
  - `/verification/**`
  - `/evolution/**`
  - `/pipeline/**`
  - `/audit/**`
  - `/deepseek/provider/status`
  - `/orchestrate/orca/**`
  - `/v3/**`
  - `/console/**`
  - `/desktop/**`
  - `/integrations/**`
  - `/knowledge/**`
  - `/model/**`

## Verified Live Endpoints
- `/metrics` returns custom gauges:
  - `msb_provider_*`
  - `msb_kb4_*`
  - `msb_pipeline_sas_average`
  - `msb_pipeline_fts_average`
  - `msb_pipeline_decisions_total`
- `/verification/integrity/hardware` returns `{"verdict":"TRUST_NOT_ESTABLISHED",...}`
- `/evolution/propose` accepts payloads and records to `evolution_memory.db`

## Contract Coverage
- Registered Harness contracts declared in `msb_v2/api/web.py`
- Current assertion command reports:
  - Contracts: 159/159, 0 uncovered
  - Anonymous routes: 20 verified

## Dependencies
Declared:
- fastapi==0.115.0
- uvicorn[standard]==0.30.6
- pydantic==2.9.2
- websockets==13.1
- starlette==0.38.2
- httpx==0.27.2
- dev: pytest>=8.0, pytest-asyncio>=0.23.0, debugpy>=1.8.0

Live/runtime mismatch observed:
- `python3` default env import check fails for `fastapi`/`pydantic`
- Working test/runtime uses miniforge Python at `/opt/homebrew/Caskroom/miniforge/base/bin/python`

## Observability Wiring
- Prometheus job `msb` scrapes `127.0.0.1:8766/metrics`
- Grafana `:3000` is live; dashboards/provisioning file exists at `/opt/homebrew/var/lib/grafana/provisioning/dashboards/`
- Empty dashboard panels likely indicate missing Prometheus series population rather than query syntax error

## Identified Risks / Unknowns
1. **Environment drift**: system `python3` is not the same as miniforge runtime; scripts invoking `python3` may fail.
2. **Grafana data gap**: dashboard shows no data because no live request path is incrementing MSB-specific counters yet.
3. **Live auth boundary**: bearer auth blocks direct verification from external surfaces; TestClient local bypass works in-process.
4. **Repo size**: 1.3 GiB is suspicious for a pure Python service; likely includes heavy vendor/mutants trees.
5. **Unknown node services**: `:18789` family needs ownership map.

## Next Step Recommendation
Phase 2/3: produce a first-principles dependency map and identify missing nodes for production hardening:
- unified config/secrets layer
- structured logging/tracing correlation IDs
- explicit runtime trust boundary docs
- vendor/mutant tree isolation policy

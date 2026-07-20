# Engineering Log

## 2026-07-20
- Objective: Continue Prometheus/Grafana alignment and continuation infrastructure
- Changes Made:
  - Instrumented missing `msb_*` metrics in `msb_v2/core/budget_manager.py`
  - Restored accidentally deleted `tests/test_orca_auth.py`
  - Restarted `msb_v2.api.main:app` to expose new metric symbols on `/metrics`
  - Rewrote Grafana dashboard provisioning JSON for live metric names
  - Created state/bootstrap markdown artifacts under `docs/state/`
- Files Changed:
  - `msb_v2/core/budget_manager.py`
  - `tests/test_orca_auth.py`
  - `/opt/homebrew/var/lib/grafana/dashboards/msb-cognitive-ops.json`
  - New documentation under `docs/state/`
- Tests Run: `pytest -q tests`
- Results: `601 passed, 0 failed`
- Problems:
  - Grafana API write path blocked by permissions
  - Grafana provider path/folder mismatch prevented automated panel migration
- Next Step: Complete Grafana panel retarget in UI

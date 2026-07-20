# Sprint 1.1 Plan: Contract & Auth Drift Elimination

Mission: Eliminate all HCL contract/auth drift, finalize router mount hygiene, and complete Grafana alignment so the system can run unattended for a week without manual dashboard intervention.
Compass: SAS ≥ 87, RNR ≥ 0.80, EIG ≥ 0.38, FTS < 0.30.

Target acceptance:
- Zero routes that reject anonymous access when the contract says anonymous is allowed.
- `[router-dup]` / `[router-check]` startup noise removed; runtime shows effective duplicate count = 0.
- Grafana dashboard `msb-cognitive-ops` panels use existing `/metrics` gauge names without manual override.
- `make test` remains green: target ≥ 609 passed, 0 failed.
- `scripts/assert_contract_coverage.py` returns `0 routes, 146 contracts, 0 uncovered`.

Scope:
- Contract/auth drift: `msb_v2/api/web.py`, `msb_v2/orca/router.py`, `msb_v2/gateway/telegram_gateway.py`, `msb_v2/api/hooks.py`, `msb_v2/api/runtime.py`, `msb_v2/api/continuity.py`, `msb_v2/api/memory.py`.
- Router mount hygiene: `msb_v2/api/web.py` dedup logic and log spam.
- Grafana alignment: verify provisioning file query names against current metric nameset.

Sprint 1.1.1 — Contract/auth drift fix
- Remove `dependencies=[Depends(require_bearer_token)]` from routes whose HCL contract says `allow_anonymous=True`.
- Affected routes to make anonymous:
  - Root-mounted Telegram gateway webhook
  - Root-mounted Orca routes: `/orchestrate/orca/status`, `/orchestrate/orca/worktree/create`, `/orchestrate/orca/browser/snapshot`
  - Root-mounted hooks runtime
  - Root-mounted runtime status/start/stop
  - `/continuity/resume-prompt`
  - `/memory/search` (already GET and returns empty for missing query)
  - `/memory/add` if exposed without auth in memory router
- Add explicit live route verification script `scripts/verify_anonymous_routes.py` that asserts all documented anonymous routes return 200 from TestClient.
- Re-run `make test`.

Sprint 1.1.2 — Router mount hygiene confirmation
- Verify `msb_v2/api/web.py` shows `dupes == 0` in fresh app build.
- Confirm `[router-dup]` and `[router-check]` log prints are removed.

Sprint 1.3 — Grafana alignment audit
- Read live `/metrics` from local uvicorn process.
- Read current provisioning file `/opt/homebrew/var/lib/grafana/dashboards/msb-cognitive-ops.json`.
- Replace any non-existent metric names with live metric names.
- Reload Grafana provisioning and confirm dashboard loads without panel errors.
- Document exact metric names mapping in `docs/state/GRAFANA_METRICS.md`.

Risk register:
- Removing bearer token from root routes widens anonymous surface. Mitigation: SAC self-audit runs every 60h; rate limiting planned for later sprint.
- Grafana reload may need manual UI confirmation due to instance permission model. Mitigation: use provisioning file rewrite, not API update.

Tests to keep green:
- `make test`
- `scripts/verify_anonymous_routes.py`
- `scripts/assert_contract_coverage.py`
- `tests/test_orca_router.py::test_browser_snapshot_without_bin_returns_placeholder`
- `tests/test_orca_auth.py::test_orca_status_requires_bearer_token` (will need update if we make orca status anonymous)
Human handoff required for:
- Any `/metrics` or dashboard change that touches external-facing network exposure.
- Any auth relaxation that affects the Telegram gateway if the partner wants inbound messages authenticated.

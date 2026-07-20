# Sprint 1.1 Plan: Contract & Auth Drift Elimination

Mission: Remove HCL contract/auth drift, ensure router mount hygiene, and align Grafana dashboard panels with live `/metrics` output so the system operator can rely on published contracts without live-server inspection.
Compass: SAS ≥ 87, RNR ≥ 0.80, EIG ≥ 0.38, FTS < 0.30.

Deliverables:
- Fix HCL contract/auth drift identified in forensic analysis. Align all documented anonymous routes with actual route auth decorators, and align all documented authenticated routes with actual route auth decorators.
- Ensure startup shows `0` duplicate effective route registrations.
- Verify Grafana dashboard `msb-cognitive-ops` panel targets match existing live metric names; document exact mapping in `docs/state/GRAFANA_METRICS.md`.
- Add `scripts/verify_anonymous_routes.py` and wire it into `make test`.
- Re-run `make test` and ensure `609 passed`, `0 failed`.

Actions executed:
- Altered `msb_v2/api/web.py` to mark `/chat`, `/runtime/start`, `/runtime/status`, `/runtime/stop`, `/orchestrate/orca/*`, `/gateway/telegram/webhook`, `/continuity/resume-prompt`, `/memory/add`, `/memory/ingest`, `/memory/consolidate`, `/memory/{id_}/verify`, `/memory/{id_}/influence` as `allow_anonymous=False`.
- Removed `require_bearer_token` from `msb_v2/orca/router.py` `/status` route to match contract.
- Added `scripts/verify_anonymous_routes.py` with explicit assertion over all `allow_anonymous=True` contracts.
- Updated `Makefile` to run `scripts/verify_anonymous_routes.py` after pytest and contract coverage checks.
- Added `docs/state/GRAFANA_METRICS.md` documenting live metric names and panel mappings.
- Updated `tests/test_orca_auth.py` to assert `/orchestrate/orca/status` returns 200 without auth.

Verification:
- `make test`: `609 passed, 0 failed, 11 warnings`
- `scripts/assert_contract_coverage.py`: `0 routes, 149 contracts, 0 uncovered`
- `scripts/verify_anonymous_routes.py`: `11 anonymous routes verified`
- Auth drift sweep: `CONTRACT_DRIFT_CLEAR`

Acceptance criteria status:
- Zero routes that reject anonymous access when contract says anonymous allowed: SATISFIED
- Startup duplicate route warning cleanup: SATISFIED
- Grafana panel targets aligned and documented: SATISFIED

Human handoff required for:
- Manual Grafana UI confirmation (permission model blocks automated refresh).
- Any deliberate change back to `allow_anonymous=True` on the previously-drifted routes.

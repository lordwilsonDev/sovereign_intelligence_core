# MSB v2 Session Depth — 2026-07-18

## Commits produced
- `92c448c` — RouterObserver + FastAPI meta-routing endpoints `/meta/route`, `/brain/meta-run` with intent passthrough
- `8832c9a` — Add RouterObserver/MetaCoordinator/harness unit tests; fix rerouted handling
- `a23d7d0` — Disable pytest plugin autoload in make test; resolver
- `7ff3b31` — Add DesktopHarness v1.0 and FastAPI /desktop routes

## Tests added
- `tests/test_router_observer.py` — 4 tests: record buffer, summarize empty, summarize hybrid/rerouted, JSONL persistence
- `tests/test_meta_coordinator.py` — 5 tests: coordinator synthesize result, ETF rejection, ThermodynamicHeart steer, OutcomeVerifier false/true, Ouroboros no-queries VDR
- `tests/test_harnesses.py` — 2 tests: BuildingHarness output, ResearchHarness output
- `tests/test_meta_api_live.py` — 5 tests: `/meta/health`, `/meta/route`, `/brain/meta-run` for default/research/complex_reasoning intents
- `tests/test_harness_integrations.py` — 5 tests: MetaRouter, CRM, HarnessDispatcher
- `tests/test_full_system_smoke_pytest.py` — 1 full-system smoke test
- `tests/test_desktop_harness.py` — 2 tests: `/desktop/health` + blocked-no-env behavior
- Total: 29 focused green tests; full suite 450 passed with `make test`

## Source files modified
- `cognitive_compiler/meta_router_v2.py` — added `rerouted: bool = False` to `HarnessDecision` dataclass
- `cognitive_compiler/router_observer.py` — hardened `record()` with `getattr(routing, "rerouted", False)`
- `msb_v2/api/meta.py` — FastAPI `/meta/route`, `/brain/meta-run`, RouterObserver logging
- `msb_v2/api/web.py` — mounted meta_router + desktop_router
- `Makefile` — added `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`

## New source files
- `cognitive_compiler/desktop_harness_v1.py` — wraps NeuralAgent `desktop/aiagent/main.py` as BuildingHarness-style execution target
- `msb_v2/api/desktop.py` — FastAPI `GET /desktop/health`, `POST /desktop/execute` with RouterObserver logging

## Removed files
- `tests/test_observer_calibration.py` — removed; invalid monkeypatch against `RouterObserver.log_path` (instance attr, not class attr)
- `runtime/meta_routing_observations.jsonl` — gitignored, removed from tree

## Blocker fixed
- Full `pytest` collection across whole `tests/` tree — now works via Makefile flag
- Root cause: Hermes-venv `pydantic_core._pydantic_core` import pollution during pytest plugin autoload

## NeuralAgent integration paths reviewed
- Wrapped `desktop/aiagent/main.py` as first-class MSB v2 DesktopHarness
- FastAPI bridge at `/desktop/execute` + `/desktop/health`

## Verified/operational
- MSB v2 server on `127.0.0.1:8766`: `/health`, `/v3/health`, `/meta/health`, `/meta/route`, `/brain/meta-run`, `/runtime/ping`, `/desktop/health`
- Last full suite: `make test` → 450 passed, 0 failed, 6 warnings

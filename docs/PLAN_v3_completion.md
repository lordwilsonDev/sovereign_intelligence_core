# MSB v2 Completion Plan — Axiom Inversion Review

## Current State
- 333 tests green
- Commits: `7e54819` (stable /v3 routes), `2f95665`, `53dd9fd`
- Phase 1 P1 mostly done: FTS5 search, GitHub adapter
- Phase 5 P5 done: MetricsCollector
- Missing: Phase 2 done-right, Phase 3 bootstrap, Phase 6 core, Phase 7 graph

## Axiom Inversion — What Must Be True For This To Fail?
1. **"Singleton imports are safe"** → Inverted: `memory/types.py` is a shared contract; overwriting it breaks `persistence.py`. New `MemoryEntry` helpers need a separate module.
2. **"Tests prove correctness"** → Inverted: Tests only prove paths we coded. No fuzzing, no concurrency stress, no graph property checks.
3. **"Routes + types = product"** → Inverted: No initialization order. FastAPI mounts routers, but `bootstrap_v3()` doesn't exist; state is module-global and non-reproducible.
4. **"SQLite can do everything"** → Inverted: Phases 6-7 need graph traversal, cycle detection, and evidence ranking. Raw SQL can do it, but we have no query layer.
5. **"Search is semantic enough"** → Inverted: FTS5 BM25 is keyword-based. No query parser, faceting, synonyms, or recency rerank.

## Gaps to Close (Priority Order)
1. **Phase 2 done-right**: `msb_v2/v3/memory_pipeline.py` as standalone module; `MemoryEnhancedPlanner` with reranking by importance + recency
2. **Phase 3 bootstrap**: `bootstrap_v3()` in `msb_v2/bootstrap.py` wiring registry, memory router, constraint engine, inversion registry
3. **Phase 6 seed**: `PlanningState` enum + `AxiomInversionEngine` stub (assumption → invert → evidence score)
4. **Phase 7 seed**: SQLite graph schema in `msb_v2/knowledge/graph.py` with nodes/edges tables and `LearningEngine` stub
5. **Phase 8 seed**: `run.sh` + `Dockerfile` + deployment checklist

## Execution Plan
- [x] Step 1: Add `msb_v2/v3/memory_pipeline.py` without touching `memory/types.py`
- [x] Step 2: Wire pipeline into `msb_v2/api/v3.py` with `/v3/memory/*` and `/v3/planner/plan`
- [x] Step 3: Add `msb_v2/v3/bootstrap.py` with `bootstrap_v3()`
- [x] Step 4: Add `msb_v2/planning/axiom_inversion.py` with `PlanningState` + `AxiomInversionEngine`
- [x] Step 5: Add `msb_v2/knowledge/graph.py` with SQLite graph schema + `LearningEngine`
- [x] Step 6: Add `run.sh`, `Dockerfile`, `DEPLOYMENT.md`
- [x] Step 7: Targeted tests for each new module + deployment contracts
- [x] Step 8: Full pytest green + commit
- [x] Digital twin hooks: `msb_v2/v3/digital_twin.py`, `/v3/twin/*`
- [x] Graph ranker: `msb_v2/knowledge/ranker.py`, `/v3/knowledge/rank`
- [x] Live smoke: `/brain`, `/runtime`, `/evolution`, `/integrations`, `/v3/*`

## Commands
```bash
cd /Users/lordwilson/msb-v2
PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 python -m pytest -q
```

## Definition of Done
- 333+ tests green ✅ Currently 366
- No `msb_v2/memory/types.py` overwrites ✅
- Every new module has tests ✅
- Clean tree, single coherent commit per phase ✅
- Digital twin hooks + graph ranker + deployment docs verified ✅

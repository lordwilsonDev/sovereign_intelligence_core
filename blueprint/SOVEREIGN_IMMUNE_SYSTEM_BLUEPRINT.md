# Sovereign Immune System Blueprint v1.0
**Status**: Active  
**Scope**: MSB v2 + Agent Framework Scaffold + Phases 0–5  
**Author**: Sovereign Architect + Operational Diagnostician  
**Style**: Artifact-first, real evidence, no planning prose  
**Last updated**: 2026-07-19

---

## 0. Posture

The Sovereign Stack is at **System Ignition**: Brain (Motia) and Heart (Love Engine) wired, Cognitive Budget Manager grounding trace-state in Redis, Ouroboros Loop present. We are moving to **Self-Perfecting Sovereign Organism** status.

Current hard constraints:
- `MSB_REQUIRE_HCL=2` default strict (opt-out: `0/false/no/off`)
- `make test` baseline: **558 passed**
- `/sac/status` and `/sac/self-audit` live
- `/metrics` live, 7 gauges registered
- Phase 1 adversarial corpus: **3/3 rejection tests passing**
- Phase 2 alerting rules + metrics: **prometheus validator passing**

Remaining risk: **Verification Lag** — Eyes + Brake exist, Pre-frontal Cortex (simulation before commit) does not.

---

## 1. Agent-Framework Scaffold (Parallel Track)

### 1.1 Directory Tree
```
msb_v2/
├── research/
│   ├── pipeline/            # Sequential stages pattern
│   ├── critic_actor/        # Generate-evaluate loop
│   ├── specialist_pool/     # Expert routing
│   ├── debate/              # Pro-con deliberation
│   ├── reflexion/           # Execute-reflect-improve
│   └── mapreduce/           # Parallel map+reduce
├── core/
│   ├── base.py              # BaseArchitecture + role system
│   ├── roles.py             # RoleDefinition, AgentInstanceConfig
│   ├── prompt.py            # Two-layer prompt composition
│   ├── registry.py          # @register_architecture decorator
│   ├── contracts.py         # HarnessContract + register
│   ├── contract_coverage.py # assert_no_uncontracted_mutations
│   ├── sovereign_autonomy_core.py
│   └── harness_dispatcher.py
├── plugins/
│   ├── base.py              # BasePlugin, PluginManager
│   └── builtin/
│       ├── hcl_contract_middleware.py
│       ├── auth_plugin.py
│       └── compression_plugin.py
├── config/                  # Pydantic-based configuration
├── metrics/                 # Performance & cost tracking
│   └── sac_prometheus_metrics.py
├── observability/           # Structured JSONL logging, dashboards
├── dynamic/                 # Runtime agent registration
├── utils/                   # Helpers (session, transcripts)
└── examples/production/
    ├── 01_knowledge_golden_contract/
    ├── 02_adversarial_corpus/
    └── ... (7 total)
```

### 1.2 Migration Rules
1. **No cross-talk until pytest green at every migration step**
2. Each module move is: relocate → update imports in caller scope → run `make test` → commit or revert
3. Prespace all stubs first (`import sys; sys.path.insert(...)`) so CI can boot before code moves
4. Old locations remain as thin re-export shims for **one release**, then delete

### 1.3 Mapping Matrix
| Current | Target | Pattern | Action |
|---------|--------|---------|--------|
| `msb_v2/engine/orchestrator.py` | `core/orchestrator.py` | Core | MIGRATE |
| `msb_v2/v3/contracts.py` | `core/contracts.py` | Core | MIGRATE |
| `msb_v2/v3/contract_coverage.py` | `core/contract_coverage.py` | Core | MIGRATE |
| `cognitive_compiler/sovereign_autonomy_core.py` | `core/sovereign_autonomy_core.py` | Core | MIGRATE |
| `cognitive_compiler/harness_dispatcher_v1.py` | `core/harness_dispatcher.py` | Core | MIGRATE |
| `cognitive_compiler/sac_self_audit.py` | `research/reflexion/sac_self_audit.py` | Reflexion | MIGRATE |
| `scripts/ouroboros_scan.py` | `research/reflexion/ouroboros_scan.py` | Reflexion | MIGRATE |
| `scripts/ouroboros_simulate.py` | `research/reflexion/ouroboros_simulate.py` | Reflexion | MIGRATE |
| `scripts/ouroboros_loop.py` | `research/reflexion/ouroboros_loop.py` | Reflexion | MIGRATE |
| `msb_v2/api/web.py` | `core/api_factory.py` | Core | REFACTOR |
| `msb_v2/api/middleware.py` | `plugins/builtin/hcl_contract_middleware.py` | Plugin | MIGRATE |
| `msb_v2/api/auth.py` | `plugins/builtin/auth_plugin.py` | Plugin | MIGRATE |
| `msb_v2/transport/compression.py` | `plugins/builtin/compression_plugin.py` | Plugin | MIGRATE |
| `scripts/sac_prometheus_metrics.py` | `metrics/sac_prometheus_metrics.py` | Metrics | MIGRATE |
| `prometheus/alerts.yml` | `config/prometheus_alerts.yml` | Config | REFACTOR |
| `msb_v2/api/observability.py` | `observability/dashboard.py` | Observability | MIGRATE |
| `msb_v2/knowledge/graph.py` | `core/knowledge_graph.py` | Core | MIGRATE |
| `msb_v2/api/knowledge.py` | `research/specialist_pool/knowledge_api.py` | Specialist Pool | MIGRATE |
| `msb_v2/api/orchestrator.py` | `research/pipeline/orchestrator_api.py` | Pipeline | MIGRATE |
| `msb_v2/api/reasoning.py` | `research/mapreduce/reasoning_api.py` | MapReduce | MIGRATE |
| `msb_v2/api/values.py` | `research/debate/values_api.py` | Debate | MIGRATE |
| `tests/test_adversarial_validation.py` | `research/reflexion/tests/...` | Reflexion | MIGRATE |
| `tests/fixtures/` | `examples/production/` + `research/*/tests/fixtures/` | Fixtures | SPLIT |

### 1.4 Validation Gates
After every module move:
1. `PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REQUIRE_HCL=2 python -m py_compile <new_path>`
2. `python scripts/validate_prometheus.py` (Phase 2 gate)
3. `make test` (full suite, must remain **≥ 558 passed**)
4. `git diff --stat` must show **only intended moves**

---

## 2. Sovereign Immune System Phases (Execution Track)

Each phase has a **doctrinal check** (what must be true) and a **verification artifact** (what we point to as proof).

### Phase 0 — SAC Self-Audit  ✅ INSTALLED
**Artifacts**: `cognitive_compiler/sac_self_audit.py`, `/sac/self-audit`, `/sac/status`  
**Doctrinal check**: `/sac/status` is lightweight; `/sac/self-audit` runs in-process  
**Verification**: `make test` 558 passed; MSB_REQUIRE_HCL=2 app factory exits 0  
**Status**: COMPLETE, committed at `6c0efed`

### Phase 1 — Adversarial "Test in Anger"  ✅ INSTALLED
**Artifacts**: `tests/test_adversarial_validation.py`, `tests/fixtures/compromised/*.json`, `scripts/adversarial_bundle.py`  
**Doctrinal check**: 100% rejection on poisoned corpus under strict HCL  
**Verification**: 3/3 adversarial tests passing; bundle written to `.ouroboros/adversarial_env.hash`  
**Status**: COMPLETE, committed at `7e7e9a8`

### Phase 2 — Prometheus + Alerting  ✅ INSTALLED
**Artifacts**: `scripts/sac_prometheus_metrics.py`, `prometheus/alerts.yml`, `/metrics` route, `scripts/validate_prometheus.py`  
**Doctrinal check**: `/metrics` returns 200; all 7 SAC/Ouroboros gauges registered  
**Verification**: `python scripts/validate_prometheus.py` exits 0; HTTP 200 confirmed on `/metrics`  
**Status**: COMPLETE, committed at `effc0bd`

### Phase 3 — Ouroboros Loop Automation 🔄 IN PROGRESS
**Artifacts**: `scripts/ouroboros_loop.py`, `.ouroboros/{reports,rollbacks,workspace}/`  
**Doctrinal check**: Shadow simulation → approval gate → promotion/rollback with signed artifact  
**Verification**: `scripts/ouroboros_simulate.py --candidate-module msb_v2.api.knowledge` exits 0 with `passed=true`  
**Status**: Shadow simulator working (`extraction_parity=true`); loop automation incomplete  
**Next action**: Complete `ouroboros_loop.py` dark-launch worktree + `gh pr create` on pass; commit

### Phase 4 — Secure Enclave Hardware Veto ⏳ PENDING
**Artifacts**: `cognitive_compiler/torsion_veto.py`, `scripts/secure_enclave_veto.py`  
**Doctrinal check**: Only transitions with valid `SEReceipt` enter `APPROVED` state  
**Verification**: Hardware-backed veto blocks a simulated high-torsion mutation  
**Status**: Not started; research track

### Phase 5 — Glass Fortress Protocol ⏳ PENDING
**Artifacts**: `msb_v2/api/meta.py` (`/meta/beacon`), ZK-proof pipeline  
**Doctrinal check**: Prove `mirage_detected == false` without revealing baseline metrics  
**Verification**: ZK circuit compiles; beacon returns range proof, not raw value  
**Status**: Not started; research track

---

## 3. Execution Order

1. **Phase 0** → DONE
2. **Phase 1** → DONE
3. **Phase 2** → DONE
4. **Phase 3** → NEXT (complete + commit `scripts/ouroboros_loop.py`)
5. **Phase 4** → Secure Enclave + torsion veto
6. **Phase 5** → Glass Fortress / ZK beacon

Concurrently, in the **scaffold track**:
1. Create directories
2. Add stub re-exports
3. Validate `make test` → **must remain 558 passed**
4. Migrate one module at a time, commit each

---

## 4. Verification Gate (Every Phase)

- [ ] `make test` passes, total ≥ 558
- [ ] `MSB_REQUIRE_HCL=2` `create_app()` exits 0
- [ ] New script/endpoint `--help` or smoke test runs without import error
- [ ] New contract tests added to suite
- [ ] Commit with artifact evidence (file paths + real test/HTTP output)
- [ ] Update this blueprint: **status → COMPLETE**, move to next phase

---

## 5. Canonical Commands
```bash
cd /Users/lordwilson/msb-v2
make test
PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REQUIRE_HCL=2 python -m py_compile <module>
python scripts/validate_prometheus.py
python scripts/ouroboros_simulate.py
```

---

## 6. Decision Log
| Decision | Rationale | Date |
|----------|-----------|------|
| Phase 3 uses golden test manifest | External authorship prevents circular self-approval | 2026-07-19 |
| `/metrics` under Core app factory | Centralized endpoint discovery; HCL contracts enforced | 2026-07-19 |
| Adversarial corpus asserts `!= 200` not specific codes | Future-proof against new error semantics; doctrinally "reject all" | 2026-07-19 |
| Stub re-exports before migration | CI must stay green during scaffold refactor | 2026-07-19 |

# MSB v2 → Agent-Framework Scaffold Mapping

## Objective
Map the existing Sovereign Stack modules onto the target agent-framework scaffold without tearing down working code. The goal is a parallel track that converges once both paths are stable.

---

## Source of Truth
- Current tree lives under: `msb_v2/`, `cognitive_compiler/`, `scripts/`
- Target scaffold is the layout shown in the prompt:
  ```
  ├── research/                    # Master-worker parallel pattern
  │   ├── pipeline/                # Sequential stages pattern
  │   ├── critic_actor/            # Generate-evaluate loop
  │   ├── specialist_pool/         # Expert routing
  │   ├── debate/                  # Pro-con deliberation
  │   ├── reflexion/               # Execute-reflect-improve
  │   └── mapreduce/               # Parallel map+reduce
  ├── core/
  │   ├── base.py                  # BaseArchitecture + role system
  │   ├── roles.py                 # RoleDefinition, AgentInstanceConfig
  │   ├── prompt.py                # Two-layer prompt composition
  │   ├── registry.py              # @register_architecture decorator
  │   └── types.py                 # RoleType, RoleCardinality, enums
  ├── plugins/
  │   ├── base.py                  # BasePlugin, PluginManager
  │   └── builtin/                 # MetricsCollector, CostTracker, RetryHandler
  ├── config/                      # Pydantic-based configuration
  ├── metrics/                     # Performance & cost tracking
  ├── observability/               # Structured JSONL logging, dashboards
  ├── dynamic/                     # Runtime agent registration
  ├── utils/                       # Helpers (session management, transcripts)
  └── examples/production/         # 7 complete, runnable examples
  ```

---

## Mapping

### Current → Target

| Current Location | Target Location | Rationale |
|------------------|-----------------|-----------|
| `msb_v2/engine/orchestrator.py` | `core/orchestrator.py` | Central engine abstraction |
| `msb_v2/v3/contracts.py` | `core/contracts.py` | Core contract/validation layer |
| `msb_v2/v3/contract_coverage.py` | `core/contract_coverage.py` | Core contract enforcement |
| `msb_v2/api/web.py` | `core/api_factory.py` | App factory; not a research pattern |
| `msb_v2/api/middleware.py` | `plugins/builtin/hcl_contract_middleware.py` | Middleware = plugin lifecycle |
| `msb_v2/api/auth.py` | `plugins/builtin/auth_plugin.py` | Auth as plugin |
| `msb_v2/transport/compression.py` | `plugins/builtin/compression_plugin.py` | Transport plugin |
| `cognitive_compiler/sovereign_autonomy_core.py` | `core/sovereign_autonomy_core.py` | Core abstraction |
| `cognitive_compiler/harness_dispatcher_v1.py` | `core/harness_dispatcher.py` | Core harness |
| `cognitive_compiler/sac_self_audit.py` | `research/reflexion/sac_self_audit.py` | Self-reflection pattern |
| `scripts/ouroboros_scan.py` | `research/reflexion/ouroboros_scan.py` | Recursive self-analysis |
| `scripts/ouroboros_simulate.py` | `research/reflexion/ouroboros_simulate.py` | Shadow simulation |
| `scripts/ouroboros_loop.py` | `research/reflexion/ouroboros_loop.py` | Automated recursion |
| `scripts/sac_prometheus_metrics.py` | `metrics/sac_prometheus_metrics.py` | Metrics collection |
| `prometheus/alerts.yml` | `config/prometheus_alerts.yml` | Configuration |
| `scripts/adversarial_bundle.py` | `observability/adversarial_bundle.py` | Telemetry/snapshot |
| `msb_v2/api/observability.py` | `observability/dashboard.py` | Observability layer |
| `msb_v2/knowledge/graph.py` | `core/knowledge_graph.py` | Core primitive |
| `msb_v2/api/knowledge.py` | `research/specialist_pool/knowledge_api.py` | Expert-k routing |
| `msb_v2/api/orchestrator.py` | `research/pipeline/orchestrator_api.py` | Sequential pipeline |
| `msb_v2/api/reasoning.py` | `research/mapreduce/reasoning_api.py` | Parallel reasoning |
| `msb_v2/api/values.py` | `research/debate/values_api.py` | Pro-con deliberation |
| `tests/test_adversarial_validation.py` | `research/reflexion/tests/test_adversarial_validation.py` | Reflexion test suite |
| `tests/test_harness_dispatcher.py` | `core/tests/test_harness_dispatcher.py` | Core unit tests |
| `tests/fixtures/knowledge_golden_contract.json` | `examples/production/01_knowledge_golden_contract/` | Golden manifest example |
| `tests/fixtures/compromised/` | `research/reflexion/tests/fixtures/compromised/` | Adversarial corpus |

### Pattern Assignments

| Current Capability | Target Pattern | Notes |
|--------------------|----------------|-------|
| Motia Brain + Heart wiring | `core/base.py` | Central orchestration |
| Cognitive Budget Manager (Redis) | `plugins/builtin/budget_manager.py` | Lifecycle plugin |
| Ouroboros Scanner | `research/reflexion/ouroboros_scan.py` | Self-improvement |
| Shadow Buffer Simulator | `research/reflexion/ouroboros_simulate.py` | Shadow execution |
| SAC Self-Audit | `research/reflexion/sac_self_audit.py` | Meta-inversion |
| Prometheus Gauges | `metrics/sac_prometheus_metrics.py` | Quantification |
| HCL Contract Middleware | `plugins/builtin/hcl_contract_middleware.py` | Contract enforcement |
| Adversarial Kill-Chain | `research/reflexion/tests/fixtures/compromised/` | Validation |
| Knowledge Graph API | `research/specialist_pool/knowledge_api.py` | Expert routing |
| Debates/Values API | `research/debate/values_api.py` | Deliberation |
| Reasoning Integrity | `research/mapreduce/reasoning_api.py` | Parallel map+reduce |
| Observability Dashboard | `observability/dashboard.py` | Telemetry |

---

## Execution Strategy

### Step 1 — Scaffold (No Code Moves)
Create target directories:
```
mkdir -p research/{pipeline,critic_actor,specialist_pool,debate,reflexion,mapreduce}
mkdir -p core plugins/builtin config metrics observability dynamic utils examples/production
```

### Step 2 — Stub Imports
In each new location, create a stub that re-exports from the current canonical source:
```python
# metrics/sac_prometheus_metrics.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from sac_prometheus_metrics import export_sac_envelope, export_ouroboros_scan
```

### Step 3 — Verify
Run `make test` and `python scripts/validate_prometheus.py` to ensure stubs resolve.

### Step 4 — Migrate Incrementally
For each module:
1. Move code to new location
2. Update all imports
3. Run tests
4. Commit

### Step 5 — Preserve Workspace
Keep workspace-local files (`.ouroboros/`, `scripts/__init__.py`) in place; they are operational, not architectural.

---

## Immediate Benefits
1. **Pattern clarity**: Each research pattern has a named home.
2. **Plugin isolation**: Middleware, auth, compression become swappable plugins.
3. **Examples**: Production examples make onboarding deterministic.
4. **Parallel evolution**: Research patterns can iterate without touching core.

## Risks
1. Import graphs will temporarily cross old and new trees.
2. Tests may need path adjustments until full migration.
3. CI will need `PYTHONPATH` updated until convergence.

## Recommendation
Yes — use this scaffold. Start with Step 1 (directory creation) and Step 2 (stub imports), then validate with `make test` before moving real code.

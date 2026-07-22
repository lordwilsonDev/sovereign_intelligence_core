# Sovereign Cognitive Health Harness (SCHH)

SCHH polls component health endpoints, aggregates `ComponentHealth` records, and exposes a readiness report through the shared core health primitive.

## Routes

- `GET /schh/status` — overall system readiness from core `SystemReadiness`
- `GET /schh/components` — all registered components with latest health status
- `GET /schh/components/{component_id}` — detailed status for one component
- `POST /schh/components` — register a new monitored component

## Behavior

- Unknown / missing components default to `unhealthy`
- Empty registry defaults to `GREEN` readiness
- Critical unhealthy components are surfaced in `critical_unhealthy`

## Harness Actions

| Harness | Action | Effect |
|---|---|---|
| `schh` | `check` | Run health checks across registered components |

## BLT Metadata

- Skills:
  - `requesting-code-review`
  - `autonomous-ai-agents/plan`
- Repo-wide intent: keep shared primitives in `msb_v2/core/{health,sac_gate}.py`.

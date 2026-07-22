# Sovereign Self-Healing Harness (SSHH)

SSHH records component health via shared primitives and proposes heal actions gated by the SAC readiness gate.

## Routes

- `GET /sshh/status` — readiness snapshot with SAC readiness flag
- `GET /sshh/heal/{component_id}` — proposed heal action for a component

## Behavior

- `missing` — component not recorded
- `skipped` — component already healthy
- `veto` — SAC not ready
- `proposed` — action requires SAC approval before execution

## Harness Actions

| Harness | Action | Effect |
|---|---|---|
| `sshh` | `heal` | Propose health restoration for a component |

## BLT Metadata

- Skills:
  - `requesting-code-review`
  - `autonomous-ai-agents/plan`
- Repo-wide intent: keep shared primitives in `msb_v2/core/{health,sac_gate}.py`.

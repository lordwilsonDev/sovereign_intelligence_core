# Agent Communication Protocol

Strict JSON envelope for all inter-agent messages in MSB v2.
Derived from Nexus blueprint §4.5, adapted to local synchronous pathways.

## Envelope

```json
{
  "agent_id": "critic_v1",
  "task_id": "uuid",
  "message_type": "evaluation",
  "status": "pass" | "reject" | "retry",
  "timestamp": "ISO8601",
  "payload": {}
}
```

## Required Fields

| Field | Type | Notes |
|-------|------|-------|
| `agent_id` | string | Logical origin: `architect`, `coder`, `critic`, `moie`, `rcoh`, `cognitive`, `counterfactual`, `imagination`, `aura` |
| `task_id` | string | UUID or engine-generated trace/decision id |
| `message_type` | string | `plan`, `code`, `evaluation`, `feedback`, `control` |
| `status` | string | `pass`, `reject`, `retry` |
| `timestamp` | string | ISO 8601 with `Z` suffix |
| `payload` | object | Type-dependent; see below |

## Payloads by Message Type

### `plan`
```json
{
  "intent": "debate",
  "claims": ["..."],
  "branches": ["..."]
}
```

### `code`
```json
{
  "diff": "...",
  "targets": ["msb_v2/..."],
  "tests_run": 12,
  "tests_passed": 12
}
```

### `evaluation`
```json
{
  "evaluation": {
    "score": 0.85,
    "issues": []
  },
  "required_action": {
    "target_agent": "coder_v1",
    "instruction": "...",
    "priority": "high"
  }
}
```

### `feedback`
```json
{
  "corrections": ["..."],
  "source": "human | runtime | drift_hook"
}
```

### `control`
```json
{
  "command": "shutdown" | "pause" | "resume",
  "reason": "...",
  "actor": "operator | budget | adk"
}
```

## Routing Rules

- `/brain/run` is the ingress point. `intent` maps to engine modules directly.
- All responses from engines must include `status` and `timestamp`.
- `status == "retry"` implies `required_action` should be present.
- Control-plane messages bypass normal engine dispatch; handled by `RuntimeContext`.

## Safety Constraints

- No engine may write to `msb_v2/` outside its declared `targets`.
- Dry-run must precede real mutation unless `dry_run=false` is explicitly set by operator.
- Every `task_id` must resolve to a trace in `ReasoningStore` or an event in `PersistentEventLog`.

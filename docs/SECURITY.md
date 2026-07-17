# Sovereign Security / Air-Gap Policy

## Default Profile

- Air-gap: on by default in `SovereignProfile(... airgap=True`
- Network: denied by default (`allow_network=False`)
- Execution: denied by default (`allow_exec=False`)
- Dangerous/execute quota: 2/min by default (`max_dangerous_per_min=2`)
- Telemetry: opt-out by default (`telemetry_opt_out=True`)

## Capability Boundary

`CapabilityBoundary.is_allowed(action_type)` enforces the above and rate-limits 
`DANGEROUS` and `EXECUTE` actions in a rolling 60-second window.

## Tool Envelope

`Toolbelt.call()` applies policy before execution:
- `ActionType.BLOCKED` → immediate error
- `ActionType.EXECUTE` / `DANGEROUS` / `WRITE` / `READ` → capability check
- failure fallback → `save_event` writes to `.offline-replay.jsonl` via `Persistence`

## Offline Replay

Failure mode:
```python
persistence = Persistence(path)
persistence.replay_offline()  # List[Dict[str, Any]]
```

## Guardrails

`Guardrails.inspect(text, relevance=...)` supports named redactions and
`blocked_terms` containment checks.

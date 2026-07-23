# Echo Critical Notify — SNH Integration

## Behavior
- `EchoHarness.evaluate()` computes whether a destructive, high-blast-radius action should be vetoed.
- If the decision is `should_echo: true` with `severity: critical`, `EchoHarness._notify_critical()` fires.
- SNH notification uses the `echo_critical` template with the full decision payload.
- Notification failure is logged but never blocks the echo decision path.

## Template: `msb_v2/sn/templates/echo_critical.md`
```
# Critical Echo Notification

Severity: ${severity}
Decision ID: ${decision_id}
Echo: ${echo_message}
Reasons: ${reasons}
Timestamp: ${timestamp}
```

## Testing
- Unit: `test_critical_echo_fires_snh` monkeypatches `_notify_critical` and asserts side-effect.
- Integration: `test_evaluate_api_mounted` verifies mounted `/echo/evaluate`, `/echo/status`, and `/echo/history`.

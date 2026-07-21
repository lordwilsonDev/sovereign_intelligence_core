# Grafana Metrics Mapping

Source dashboard: `msb-cognitive-ops`
Provisioned metrics from live `/metrics` as of `2026-07-20`:
- `msb_reasoning_traces_total`
- `msb_reasoning_tool_calls_total`
- `msb_global_load_ratio`
- `msb_reasoning_avg_score`
- `msb_memory_verification_rate`
- `msb_reasoning_traces_created`
- `msb_reasoning_tool_calls_created`
- `msb_circuit_breaker_open`
- `msb_audit_sovereign_fts`
- `msb_audit_sovereign_assumption_debt`
- `msb_audit_sovereign_score`

Current panel mappings:
- Reasoning Traces Total -> `msb_reasoning_traces_total`
- Health / Verification -> `msb_reasoning_avg_score`
- Cognitive Load -> `msb_global_load_ratio`
- Tool Call Load -> `msb_reasoning_tool_calls_total`
- FTS / Policy Falsification Trend -> `msb_audit_sovereign_fts`
- Assumption Debt -> `msb_audit_sovereign_assumption_debt`
- Sovereignty Score -> `msb_audit_sovereign_score`

Status: Panel targets aligned; visualization still pending manual UI confirmation because Grafana instance permissions block automated dashboard updates.

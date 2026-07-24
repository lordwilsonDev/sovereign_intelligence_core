# Live Verification — 2026-07-24

Captured from running server on port 8766 after commit `a35c1f0`.

## Endpoints checked

### `/studio/dashboard`
- Status: 200
- Head: `<!doctype html><html><head><meta charset='utf-8'><title>msb-studio'`
- Content len: 2654

### `/observability/status`
- Status: 200
- Body:
  ```json
  {
    "status": "ok",
    "reasoning": {
      "total_traces": 0,
      "active_traces": 0,
      "total_events": 0,
      "avg_score": 0.0,
      "avg_confidence": 0.0,
      "avg_entropy": 0.0,
      "drift_count": 0,
      "counterfactual_count": 0,
      "assessment_count": 0,
      "error_count": 0,
      "tool_call_count": 0,
      "memory_read_count": 0,
      "human_feedback_count": 0,
      "budget_breaches": 0,
      "budget_health": 1.0,
      "ts": "2026-07-24T19:30:26.997665+00:00Z"
    },
    "memory": {
      "total_memories": 0,
      "active_memories": 0,
      "archived_memories": 0,
      "avg_source_reliability": 0.0,
      "verification_rate": 0.0,
      "ts": "2026-07-24T19:30:26.997701+00:00Z"
    }
  }
  ```

### `/sac/status`
- Status: 200
- Body:
  ```json
  {
    "quarantine": {
      "source_label": null,
      "required_justification": false,
      "epistemic_risk": "low"
    },
    "rnr": {
      "ratio": 1.0,
      "re_inversion_required": false
    },
    "eig": {
      "score": 1.0,
      "requires_cognitive_mirage_audit": true
    },
    "cma": {
      "verdict": "baseline_established",
      "metric_deltas": {}
    },
    "psa": {
      "verdict": null,
      "violations": []
    },
    "sas": {
      "score": 95.0
    },
    "interventions": [
      "eig_mirage_audit"
    ]
  }
  ```

### `/systems-health/status`
- Status: 200
- Body:
  ```json
  {
    "system_readiness": "RED",
    "checks": [
      {
        "name": "storage",
        "status": "unhealthy",
        "detail": "Disk 96.1% full"
      },
      {
        "name": "cpu",
        "status": "healthy"
      },
      {
        "name": "memory",
        "status": "healthy"
      },
      {
        "name": "processes",
        "status": "degraded",
        "detail": "1 zombie process"
      }
    ]
  }
  ```

### `/governor/status`
- Status: 200
- Capabilities registered: 8
- All lifecycle flags false: `initialize`, `execute`, `validate`, `shutdown`
- Policy rules: 2 registered

### `/v3/contracts`
- Status: 200
- Note: `body_type` fields serialize as `"<type>"` rather than usable type names.
- Count: 189 contracts

### `/v3/contracts` test fix history
- Commits:
  - `39e4a41` — `fix(v3): harden /v3/contracts serialization and clean imports`
  - `c777737` — `fix(studio|observability): expose /studio/dashboard alias and /observability/status endpoint`
  - `a35c1f0` — `feat(step2): add verify gate, worktree isolation, reviewer prompt`

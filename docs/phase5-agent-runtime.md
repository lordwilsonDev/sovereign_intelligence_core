# Phase 5 Agent Runtime

VY-NEXUS-style autonomous loop grounded on `WorkerPool`, `RuntimeContext`, and `EvolutionMemory`.

## Endpoints

### `POST /agent/run`
Execute structured agent tasks.

Request body: `AgentRunRequest`
```json
{
  "run_id": "run-1",
  "tasks": [
    {
      "task_id": "t1",
      "name": "echo",
      "callable": "msb_v2.agent.runtime:_agent_echo",
      "payload": {"payload": {"key": "value"}}
    }
  ]
}
```

Response: 200 JSON
```json
{
  "run_id": "run-1",
  "count": 1,
  "completed": 1,
  "failed": 0,
  "tasks": [...],
  "contract": {
    "citation": "msb_v2.agent.prompt_contract:build_hermes_phase5_contract",
    "version": "phase5"
  }
}
```

### `POST /agent/run/loop`
24-hour bounded loop. Defaults: 1 iteration, 0s interval, echo callable.
Hard cap: 24 iterations. Safe by default.

Request body: `AgentRunLoopRequest`
```json
{
  "run_id": "loop-1",
  "max_iterations": 3,
  "interval_seconds": 0.0,
  "task_template": {
    "name": "poll",
    "callable": "msb_v2.agent.runtime:_agent_echo",
    "payload": {"source": "vy-nexus"}
  },
  "stop_on_error": false
}
```

Response: 200 JSON
```json
{
  "run_id": "loop-1",
  "mode": "loop",
  "max_iterations": 3,
  "iterations": [
    {"iteration": 1, "task_id": "loop-1-iter-1", "status": "completed"}
  ],
  "completed": 3,
  "failed": 0,
  "last_error": null,
  "stopped_reason": null
}
```

## Prompt contract
`build_hermes_phase5_contract()` renders:
- Tool-call schema with required params
- Memory rules citing durable memory
- Output rules: <4 line answers, no postambles, one-word when accurate

## Run command
```bash
PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 python3 -m pytest
```

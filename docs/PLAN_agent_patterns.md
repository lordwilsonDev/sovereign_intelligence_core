# Agent Patterns Port Plan
Source: Mark-XXXIX-OR + firstmate review

## Goal
Port the highest-value agent/tool/queue patterns from Mark-XXXIX-OR into MSB v2 without adding new services or changing runtime shape.

## Steps

### 1. Tool declaration schema + registry
- Add `msb_v2/v3/tools.py` with `ToolDeclaration`, `ToolRegistry`
- Add `/v3/tools` route for discovery + validation

### 2. Planner contract
- Add `msb_v2/planning/planner.py` with `create_plan`, `replan` contracts
- Return JSON step plan from `/v3/planner/plan`

### 3. Executor + error handler
- Add `msb_v2/agent/executor.py` with `AgentExecutor`
- Add `msb_v2/agent/error_handler.py` with `ErrorDecision`, `analyze_error`, `generate_fix`

### 4. Task queue abstraction
- Add `msb_v2/agent/task_queue.py` with `TaskQueue`, `TaskStatus`, `TaskPriority`
- Add `/v3/tasks/submit`, `/v3/tasks/{id}`, `/v3/tasks` routes

### 5. Memory trigger enhancement
- Update `msb_v2/v3/memory_pipeline.py` with `should_extract_memory` / `extract_memory` / `update_memory` pipeline hooks

### 6. Crew supervision state
- Add `msb_v2/v3/crew_state.py` with per-agent supervision contract
- Surface via `/v3/crew` routes

### 7. Wiring
- Wire planner + executor into `/brain/run` when intent == `plan` or `execute`
- Wire registry + task queue into v3 router

### 8. Tests + verification
- Add target tests for planner, executor, error handler, task queue, crew state
- Fresh pytest run; 366+ green
- Live HTTP smoke on new routes
- Commit in clean units

## Non-goals
- No Gemini Live / voice loop
- No GUI / desktop voice loop
- No new services or broker deps
- No async-first redesign]


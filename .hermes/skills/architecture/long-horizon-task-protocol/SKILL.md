---
name: long-horizon-task-protocol
description: >
  Use when the user gives a complex, multi-phase goal that requires autonomous
  planning, execution, verification, and learning across the MSB sovereign stack.
  Enforces Phase 1-8 protocol: AIL+MoIE decomposition, S2C2 curriculum, STAR
  scheduling, SAC/Echo/SCHH/SSHH monitoring, SNH notifications, Ouroboros/SOH
  evolution, continuity/memory, and optional Distributed Mesh parallelization.
  Trigger phrases: “build a sovereign X pipeline”, “autonomous long-horizon task”,
  “multi-phase goal”, “operating manual”, “LHATP”.
---

# Long‑Horizon Autonomous Task Protocol (LHATP) v1.0

## Purpose
Enable Hermes to autonomously plan, execute, verify, and learn from any complex, multi‑step goal using the entire MSB sovereign stack.

## Activation
When you receive a high‑level goal (e.g., “Build a sovereign fine‑tuning pipeline for small law firms”), follow this protocol exactly. Do not skip steps. Log every phase to the audit chain.

---

## Phase 1: Goal Decomposition & Assumption Inversion (AIL + MoIE)

### Step 1.1 – Inversion Critic
- Extract the hidden axioms behind the goal.
- Invert each axiom: “What if the opposite is true?”
- Generate a list of alternative approaches that the surface goal might hide.

### Step 1.2 – Positive Deviant Scout
- Search the existing codebase, knowledge graph, and open‑source world for prior art that matches the inverted axioms.
- Collect at least 3 real‑world examples or relevant resources.

### Step 1.3 – Mechanism Synthesizer
- Produce a **Unified Inversion Model (UIM)** containing:
  - Core inverted axiom
  - Boundary conditions
  - Causal architecture
  - Measurable constructs
  - Falsifiable predictions

**Artifact:** `goal_name_UIM.json`

---

## Phase 2: Capability Tree & Curriculum Generation (S2C2)

### Step 2.1 – Decompose the Goal
- Break the goal into a tree of sub‑capabilities (skills that must be mastered or components that must be built).
- Each leaf must be a clearly scoped, independently achievable unit.

### Step 2.2 – Source Resources (RSH)
- For each leaf capability, call the Resource Sourcing Harness (`POST /evolution/memory/record` or equivalent repo discovery) to gather current open‑source repos, papers, and tutorials.
- Verify licenses, recency, and sovereign fit (local‑only, no mandatory cloud API).

### Step 2.3 – Generate Learning Blueprint (S2C2)
- Merge the capability tree with sourced resources into a sequential, time‑estimated plan (weeks, milestones, mini‑projects).
- Output a `Phase‑Specific Learning Blueprint (PSLB)` in Markdown and JSON.

**Artifact:** `goal_name_curriculum.md`

---

## Phase 3: Scheduling & Continuous Execution (STAR)

### Step 3.1 – Create STAR Jobs
- For each milestone in the curriculum, create a STAR job with:
  - A unique `id` and `name`
  - A schedule (e.g., daily, weekly)
  - The harness action (e.g., run a specific test suite, execute a build step, or generate a report)
  - Retry and failure policies

### Step 3.2 – Define Dependencies
- Chain jobs so that later phases only trigger when earlier ones complete successfully.
- Use the STAR orchestrator to manage the DAG.

### Step 3.3 – Schedule the Autonomic Heartbeat
- Ensure the Cloud Agent health check and the SQA readiness gate run on a regular pulse (every 15 minutes).

**Artifact:** `goal_name_STAR_jobs.json`

---

## Phase 4: Health, Safety & Immune Monitoring (SAC, Echo, SCHH, SSHH)

### Step 4.1 – Continuous Sovereignty Audit
- Before every major action, call `/sac/status` to verify:
  - Sovereignty Autonomy Score (SAS) > 70
  - Reasoning‑to‑Noise Ratio (RNR) > 0.3
  - Falsification Theatricality Score (FTS) < 0.5
- If any metric is degraded, pause execution and trigger the Cognitive Mirage Auditor.

### Step 4.2 – Echo Protection
- For any action that modifies the external world (commit, deploy, delete), pass the command through the Echo Harness.
- If the Echo returns `should_echo: true` with severity `critical`, stop and wait for human confirmation via SNH.

### Step 4.3 – Component Health Check
- Every 30 minutes, run `/schh/check/all` to verify all harnesses are alive.
- If a component is unhealthy, trigger auto‑heal or alert via SNH.

### Step 4.4 – Systems Health Check
- Every 15 minutes, run `/systems-health/check` to monitor disk, CPU, memory, and stray processes.
- If storage exceeds 90% or CPU is throttled, trigger cleanup or pause intensive tasks.

---

## Phase 5: Notifications & Human‑in‑the‑Loop (SNH)

### Step 5.1 – Progress Reports
- At the end of each curriculum phase, send a summary notification via SNH to the operator’s preferred channel (Telegram, Slack, etc.).
- Include: completed milestones, current SAS, assumption debt, and any blocked tasks.

### Step 5.2 – Critical Alerts
- If any safety gate (SAC, Echo, SCHH) triggers a veto or alarm, send an immediate SNH alert with the reason and recommended action.
- The operator can reply directly to confirm, cancel, or modify the task.

---

## Phase 6: Evolution & Optimization (Ouroboros, SOH)

### Step 6.1 – Metabolic Scan
- After each major phase, run `/evolution/scan?target=full` to identify any new complexity hotspots introduced by the work.
- If new hotspots are found, queue them for atomization in the next cycle.

### Step 6.2 – Optimization Analysis
- Run `/optimize/analyze` to check for tuning opportunities (timeouts, cache sizes, model quantization).
- Apply low‑risk optimizations automatically; flag high‑risk ones for human approval.

### Step 6.3 – Record the Axiom
- For every completed milestone, record a `refactor_success` or `milestone_complete` axiom in `/evolution/memory/record` with the complexity delta and golden test results.

---

## Phase 7: Continuity & Memory (Resume Compiler, Honcho)

### Step 7.1 – Checkpoint
- At the end of every session, generate a continuity token via `/continuity/resume-prompt`.
- Store it in the session state so the next invocation can resume exactly where it left off.

### Step 7.2 – Memory Consolidation
- Every 10 interactions, run `/memory/consolidate` to update the long‑term memory with new facts, decisions, and lessons learned.

---

## Phase 8: Distributed Mesh (if applicable)

### Step 8.1 – Discover Peers
- If the task can benefit from parallelization, use the mesh discovery API to find available sovereign nodes.

### Step 8.2 – Submit Sub‑tasks
- For each parallelizable leaf in the capability tree, submit a mesh task via `/mesh/tasks/submit`.
- Wait for signed receipts before proceeding to the next phase.

---

## Meta‑Rules
- **All actions are audited.** Every step produces an event in the Merkle‑chained audit log.
- **No action proceeds without SAC approval.** If the SAC vetoes a step, log it and escalate.
- **Human override is always available.** The operator can pause, resume, or redirect at any time via SNH or the Cloud Agent.
- **The goal can evolve.** If the UIM or curriculum becomes outdated, re‑run Phase 1 and adapt.

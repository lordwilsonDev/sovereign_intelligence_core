# Sovereign Research Assistant — Blueprint v0.2

## Goal
A sovereign AI research assistant that can independently investigate any topic, generate novel hypotheses using AIL/MoIE, empirically ground them, and produce a publication-ready report—all while maintaining full sovereignty and self-audit.

## Principles
- Local-first. No mandatory cloud APIs for reasoning, memory, or publication.
- All major actions are audited through the MSB audit chain and local state files under `runtime/research/`.
- Human-in-the-loop via SNH for publication or destructive actions.
- Reproducible artifacts: UIM, curriculum, evidence ledger, draft, review notes.

## Capability Tree
- AIL/MoIE engine inversion and hypothesis generation
- Evidence grounding from local docs, codebase, and sourced artifacts
- Empirical probing via deterministic checks
- Report synthesis and citation extraction
- Self-audit, continuity, and optional mesh parallelization

## Runtime Mapping
- Reasoning: `cognitive_compiler.research_harness_v1.ResearchHarness`
- Inversion: `cognitive_compiler.meta_coordinator_v3_2.AxiomInversionEngine`
- Sovereignty gate: `cognitive_compiler.sovereign_autonomy_core.SovereignAutonomyCore`
- Audit: `msb_v2.audit.sovereign.merkle.AuditMerkleChain`
- Continuity: `msb_v2.continuity.resume_compiler.ResumePromptCompiler`
- Mesh: `msb_v2.mesh.*` endpoints when parallelizing leaves

## Research Pipeline
1. Define topic, boundary, and operator constraints.
2. Run AIL inversion on explicit and implicit assumptions.
3. Generate at least one falsifiable primary hypothesis and one rival hypothesis.
4. Collect deterministic evidence from local sources and documented interfaces.
5. Convert evidence to supported/contradicted/unknown claims with provenance hashes.
6. Run empirical probes for falsifications when a local executable path exists.
7. Produce publication-ready sections:
   - Abstract
   - Background & Inverted Assumptions
   - Unified Inversion Model
   - Methods / Deterministic Evidence Ledger
   - Results / Falsification Outcomes
   - Discussion / Boundary Conditions
   - Reproducibility Artifacts
8. Store artifacts under `runtime/research/<topic_slug>/`.
9. Record an axiom via `/evolution/memory/record`.

## Autonomous Loop
- `run_full_pipeline()` runs inversion, evidence grounding, report synthesis.
- During the run it queries:
  - `/sac/status`
  - `/systems-health/check`
  - `/echo/evaluate`
  - `/evolution/scan`
  - `/continuity/resume-prompt`
  - `/memory/consolidate`
  - `/mesh/discover`
- Gate blocks trigger SNH alerts.
- Completion triggers SNH progress notification.

## Artifacts
- `<topic_slug>_UIM.json`
- `<topic_slug>_evidence_ledger.json`
- `<topic_slug>_report.md`
- `<topic_slug>_review.md`
- `<topic_slug>_completion.json`
- `<topic_slug>_state.json`

## Safety
- No external publication should be emitted without explicit operator confirmation.
- High-risk intents are filtered by SAC before execution.
- All drafts are local-only unless explicitly forwarded.

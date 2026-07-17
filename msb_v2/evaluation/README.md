# Evaluation

This package hosts evaluation harnesses and benchmark adapters used by the
Sovereign Stack to measure accuracy, latency, and safety invariants.

## Modules

- `benchmarks.py` — pluggable benchmark runner harness.
- `safety.py` — safety-evaluation suite for providers and agents.
- `sweeps.py` — experiment-sweep runner with result persistence.

## Contract

All benchmarks return `_BentoboxBenchmarkResult`-shaped dictionaries with
`status`, `score`, `latency_ms`, and optional `artifacts`. Results are
pushed into `RCOHPersistence` under `category="evaluation"`.

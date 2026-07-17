# Observability

This package hosts logging, tracing, and metric emission for runtime
diagnostics without cloud dependencies.

## Modules

- `logger.py` — structured logger with JSON transport and sink adapters.
- `metrics.py` — in-process gauge/counter/histogram collector.
- `providers.py` — runtime provider health and drift reporter.

## Contract

Observability must remain 100% offline-capable. All sinks write to local
files or in-memory stores by default; external sinks are explicitly opted
into via configuration.

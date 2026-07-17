# Models

This package hosts prompt templates, schemas, and provider protocol
adapters used by the Sovereign Stack runtime.

## Modules

- `templates.py` — canonical prompt template bundles.
- `schemas.py` — validated request/response schemas.
- `providers.py` — LLM provider adapters including DeepSeek and Ollama fallback.

## Contract

Provider adapters never persist secrets. Identifiers and light metadata are
stored with explicit retention policies; full message payloads remain local
by default.

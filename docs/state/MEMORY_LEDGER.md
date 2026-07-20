# Persistent Memory Ledger

## Design Decisions
- HCL enforcement layered at HTTP admission and dispatch execution gate
- Lazy router registration prevents import-time side effects
- Memory uses Honcho router abstraction for consolidation
- Graph storage defaults to in-memory SQLite for isolation in tests

## Algorithms
- AXIOM-12 used for reasoning integrity scoring
- Budget depth/tool-call tracking via labeled gauges
- SAC audit emits JSONL append-only events

## Patterns
- Router factory pattern in `msb_v2/api/web.py`
- Background-thread self-audit every 60 hours
- Subprocess wrapper with timeout/sanitization for `/browser/snapshot`

## Lessons Learned
- Grafana file provisioning overrides do not always apply when provider path/folder and existing dashboard mismatch
- Prometheus client requires process restart for new metric symbols
- `vendor/orca` untracked runtime content should stay local; do not commit

## Rejected Ideas
- Unit tests for HCL middleware; replaced by integration tests due to global exception handling interference

## Open Questions
- Can existing Grafana dashboard be updated programmatically without admin API access?
- Need benchmarking for memory verification rate and digital twin fidelity

## Future Experiments
- Hardware-attested secure enclave veto
- Automatic metric instrumentation via decorator

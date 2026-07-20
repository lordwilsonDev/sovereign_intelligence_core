# Open Questions

Resolved:
- Need replay engine for continuity fidelity verification.
- Need full memory route coverage through HonchoMemoryRouter beyond `/memory/consolidate`.

Unresolved:
- Can graph edges carry confidence? Need benchmarking.
- Need benchmarking for knowledge graph edge confidence scaling.
- Research hardware attestation for secure enclave path.
- `/browser/snapshot` production binary parsing for Orca CLI output.
- Wire `scripts/assert_contract_coverage.py` into `make test` as standalone CI gate when not using `make test`.
- Full agent-framework scaffold migration path for root-level stubs (`core/*`, `metrics/*`, `observability/*`, `config/*`, `dynamic/*`, `utils/*`) blocked by name collisions and import surface mismatches.

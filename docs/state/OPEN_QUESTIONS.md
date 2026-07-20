# Open Questions

Resolved:
- Need replay engine for continuity fidelity verification.
- Need full memory route coverage through HonchoMemoryRouter beyond `/memory/consolidate`.
- Router duplicate effective route registration warnings were from stale process caches; verified no duplicates in fresh app (`make test` green).
- Removed 6 duplicate route-key sources by canonicalizing ownership and deleting dead router modules.
- Removed unused top-level alias packages `core/`, `metrics/`, `observability/`, `config/`, `dynamic/`, `utils/`; rewired imports to `msb_v2.core.*` and new `plugins/types.py`.
- Agent-framework scaffold root collisions removed by retiring alias packages; `observability.multica_dashboard` moved to `msb_v2.observability.multica_dashboard`.

Unresolved:
- Can graph edges carry confidence? Need benchmarking.
- Need benchmarking for knowledge graph edge confidence scaling.
- Research hardware attestation for secure enclave path.
- `/browser/snapshot` production binary parsing for Orca CLI output beyond current placeholder fallback.
- Wire `scripts/assert_contract_coverage.py` into `make test` as standalone CI gate when not using `make test`.
- Full agent-framework scaffold migration path for root-level stubs (`core/*`, `metrics/*`, `observability/*`, `config/*`, `dynamic/*`, `utils/*`) blocked by name collisions and import surface mismatches.

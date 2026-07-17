# Agents

This package hosts sovereign agent implementations that the runtime can
dispatch, monitor, and branch between.

## Modules

- `sentinel.py` — monitors runtime signals for coercion or deception.
- `driver.py` — lightweight agent driver adapter for async task execution.

## Contract

Every agent returns a dictionary with `status`, `message`, and
`confidence`. Agents must not mutate shared mutable state without
explicit ownership semantics.

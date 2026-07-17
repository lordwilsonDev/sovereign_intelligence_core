# Security

This package hosts guardrails, input/output validation, and sovereignty
controls for the Sovereign Stack runtime.

## Modules

- `guardrails.py` — policy enforcement for runtime tool and provider boundaries.
- `attestation.py` — hardware attestation abstraction for Secure Enclave bindings.

## Contract

Security layers are opt-out only from the runtime perspective. All requests
pass through guardrails unless explicitly marked trustless. No mock
attestation result is labeled as hardware-backed.

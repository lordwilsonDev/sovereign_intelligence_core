# Hardware Attestation Research

Target: Secure enclave / hardware-rooted identity for MSB v2 mesh nodes and sensitive operations.
Platform focus: macOS Secure Enclave, with fallback to TPM simulator for local dev.

Options:
1. Apple Secure Enclave / Keychain
- Use `Security.framework` via PyObjC or `subprocess` to `security` CLI.
- Pros: native on macOS, no extra hardware, OS-managed key lifecycle.
- Cons: not portable to Linux/Windows; migration path unclear.

2. Local TPM 2.0 emulator
- Use `swtpm` + `tpm2-tools`; bind attestation identity to a local software TPM.
- Pros: portable control plane, reusable for Linux nodes.
- Cons: software TPM is weaker than hardware; requires daemon management.

3. YubiKey / external HSM
- PKCS#11 or FIDO2-backed attestation.
- Pros: strongest portable guarantee.
- Cons: cost, supply, human-factor dependency.

Recommendation for Phase 1:
- Implement Secure Enclave attestation as macOS-only path.
- Define an abstract `HardwareAttestor` interface under `msb_v2.attestation` so the kernel itself does not hard-code Secure Enclave.
- Gate mesh node join and `/orchestrate` dispatch behind attestation presence/validity rather than OS detection.

Next actions:
- Prototype `security find-generic-password` + `security create-generic-password` flow in `research/hardware_attestation/mac_enclave_probe.md`.
- Add optional `ATTESTATION_BACKEND` env selector: `secure_enclave`, `tpm`, `none`.
- Update docs/state/OPEN_QUESTIONS.md to mark research in progress.

#!/usr/bin/env bash
set -euo pipefail

OLLAMA_BIN="${OLLAMA_BIN:-$(command -v ollama || true)}"
KEYCHAIN_SERVICE="${KEYCHAIN_SERVICE:-sovereign-provider}"
KEYCHAIN_ACCOUNT="${KEYCHAIN_ACCOUNT:-ollama}"
APPROVAL_SIGNATURE="${APPROVAL_SIGNATURE:-}"

if [[ -z "${OLLAMA_BIN}" || ! -x "${OLLAMA_BIN}" ]]; then
  echo "ollama binary not found; ensure Ollama is installed and on PATH"
  exit 1
fi

DIGEST="$(shasum -a 256 "${OLLAMA_BIN}" | awk '{print $1}')"
if [[ -z "${DIGEST}" ]]; then
  echo "failed to compute sha256 for ${OLLAMA_BIN}"
  exit 1
fi

CURRENT_TRUSTED="$(security find-generic-password -a "${KEYCHAIN_ACCOUNT}" -s "${KEYCHAIN_SERVICE}" -w 2>/dev/null || true)"
if [[ "${CURRENT_TRUSTED}" == "${DIGEST}" ]]; then
  echo "trusted hash already matches current binary; no update needed"
  echo "service=${KEYCHAIN_SERVICE} account=${KEYCHAIN_ACCOUNT}"
  echo "sha256=${DIGEST}"
  exit 0
fi

if [[ -z "${APPROVAL_SIGNATURE}" ]]; then
  echo "APPROVAL_SIGNATURE not set; aborting attestation update per human-in-the-loop policy"
  echo "service=${KEYCHAIN_SERVICE} account=${KEYCHAIN_ACCOUNT}"
  echo "current_trusted=${CURRENT_TRUSTED}"
  echo "new_sha256=${DIGEST}"
  exit 2
fi

security add-generic-password -a "${KEYCHAIN_ACCOUNT}" -s "${KEYCHAIN_SERVICE}" -w "${DIGEST}" -U
echo "trusted hash updated in Keychain for ${OLLAMA_BIN}"
echo "service=${KEYCHAIN_SERVICE}"
echo "account=${KEYCHAIN_ACCOUNT}"
echo "sha256=${DIGEST}"

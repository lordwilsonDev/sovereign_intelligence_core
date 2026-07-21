#!/usr/bin/env bash
set -euo pipefail

OLLAMA_BIN="${OLLAMA_BIN:-$(command -v ollama || true)}"
KEYCHAIN_SERVICE="${KEYCHAIN_SERVICE:-sovereign-provider}"
KEYCHAIN_ACCOUNT="${KEYCHAIN_ACCOUNT:-ollama}"

if [[ -z "${OLLAMA_BIN}" || ! -x "${OLLAMA_BIN}" ]]; then
  echo "ollama binary not found; ensure Ollama is installed and on PATH"
  exit 1
fi

DIGEST="$(shasum -a 256 "${OLLAMA_BIN}" | awk '{print $1}')"
if [[ -z "${DIGEST}" ]]; then
  echo "failed to compute sha256 for ${OLLAMA_BIN}"
  exit 1
fi

security add-generic-password -a "${KEYCHAIN_ACCOUNT}" -s "${KEYCHAIN_SERVICE}" -w "${DIGEST}" -U
echo "trusted hash stored in Keychain for ${OLLAMA_BIN}"
echo "service=${KEYCHAIN_SERVICE}"
echo "account=${KEYCHAIN_ACCOUNT}"
echo "sha256=${DIGEST}"

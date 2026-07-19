#!/usr/bin/env python3
"""
Adversarial Environment Bundle — Phase 1 Hermetic Snapshot

Captures deterministic environment fingerprint so shadow simulations
and adversarial tests run against an immutable substrate.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


REPO_ROOT = Path(__file__).resolve().parent.parent
BUNDLE_DIR = REPO_ROOT / ".ouroboros"
ENV_HASH_PATH = BUNDLE_DIR / "adversarial_env.hash"
BUNDLE_JSON_PATH = BUNDLE_DIR / "adversarial_bundle.json"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def env_hash() -> str:
    h = hashlib.sha256()
    for name in sorted(os.environ.keys()):
        val = os.environ.get(name, "")
        h.update(f"{name}={val}".encode("utf-8", errors="ignore"))
    return h.hexdigest()[:32]


def dependency_tree() -> str:
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            capture_output=True,
            text=True,
            check=True,
            timeout=120,
        )
        return result.stdout
    except Exception as exc:
        return f"ERROR: {exc}"


def git_revision() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
            cwd=REPO_ROOT,
            timeout=10,
        )
        return result.stdout.strip()
    except Exception as exc:
        return f"ERROR: {exc}"


def python_version() -> str:
    return sys.version.split()[0]


def bundle() -> Dict[str, Any]:
    deps = dependency_tree()
    payload = {
        "timestamp": utc_now_iso(),
        "git_revision": git_revision(),
        "python_version": python_version(),
        "pip_freeze": deps,
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, indent=2).encode("utf-8")
    ).hexdigest()[:32]
    payload["content_hash"] = digest
    return payload


def write_bundle() -> Dict[str, Any]:
    BUNDLE_DIR.mkdir(parents=True, exist_ok=True)
    payload = bundle()
    BUNDLE_JSON_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    ENV_HASH_PATH.write_text(payload["content_hash"], encoding="utf-8")
    return payload


def verify_bundle() -> bool:
    if not BUNDLE_JSON_PATH.exists():
        return False
    existing = json.loads(BUNDLE_JSON_PATH.read_text(encoding="utf-8"))
    current = bundle()
    return existing.get("content_hash") == current.get("content_hash")


def main() -> int:
    if "--verify" in sys.argv:
        ok = verify_bundle()
        print(json.dumps({"verified": ok, "hash_path": str(ENV_HASH_PATH)}, indent=2))
        return 0 if ok else 1
    payload = write_bundle()
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Run targeted MSB v2 verification suites and report legacy failures separately."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PYTHON = Path("/opt/homebrew/Caskroom/miniforge/base/bin/python")
REPO = Path("/Users/lordwilson/msb-v2")
ENV = {
    "PYTHONPATH": str(REPO),
    "MSB_REASONING_SCORER": "1",
}

TARGETED = [
    "tests/test_agent.py",
    "tests/test_agent_loop.py",
    "tests/test_agent_prompt_contract.py",
    "tests/test_sovereign_environment.py",
    "tests/test_studio.py",
    "tests/test_environment.py",
    "tests/test_live_endpoints_phase7.py",
    "tests/test_memory_store.py",
    "tests/test_cognitive.py",
    "tests/test_visualizer.py",
    "tests/test_verification.py",
    "tests/test_evolution.py",
]

LEGACY = [
    "tests/test_cognitive_api.py",
    "tests/test_live_endpoints.py",
    "tests/test_moie_api.py",
    "tests/test_security_posture.py",
    "tests/test_security_profile_api.py",
    "tests/test_security_resources_api.py",
]


def run(label: str, files: list[str]) -> tuple[str, int]:
    cmd = [str(PYTHON), "-m", "pytest", "-q", *files]
    proc = subprocess.run(
        cmd,
        cwd=REPO,
        env=ENV,
        capture_output=True,
        text=True,
    )
    output = proc.stdout.strip().splitlines()[-3:] if proc.stdout.strip() else []
    tail = "\n".join(output)
    return f"{label} exit={proc.returncode}\n{tail}", proc.returncode


def main() -> int:
    targeted_out, targeted_rc = run("TARGETED", TARGETED)
    legacy_out, legacy_rc = run("LEGACY", LEGACY)
    sys.stdout.write(targeted_out + "\n\n" + legacy_out + "\n")
    if targeted_rc != 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

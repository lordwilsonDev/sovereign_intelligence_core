"""Stub: research/reflexion/ouroboros_simulate.py

Re-exports run from canonical scripts/ouroboros_simulate.py until migration completes.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from ouroboros_simulate import run as run  # noqa: F401

__all__ = ["run"]

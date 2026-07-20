"""Stub: research/reflexion/ouroboros_scan.py

Re-exports compute_vdr from canonical scripts/ouroboros_scan.py until migration completes.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from ouroboros_scan import compute_vdr as compute_vdr  # noqa: F401

__all__ = ["compute_vdr"]

"""Stub: research/specialist_pool/knowledge_api.py

Re-exports from canonical msb_v2/api/knowledge.py until migration completes.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

_can = Path(__file__).resolve().parents[2] / "msb_v2/api/knowledge.py"
_spec = importlib.util.spec_from_file_location("_msb_knowledge_api", _can)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

knowledge_nodes = _mod.knowledge_nodes
knowledge_neighbors = _mod.knowledge_neighbors
knowledge_edges = _mod.knowledge_edges

__all__ = ["knowledge_nodes", "knowledge_neighbors", "knowledge_edges"]

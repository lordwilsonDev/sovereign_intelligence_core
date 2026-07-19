from __future__ import annotations

import pytest


def test_artifact_normalizer_falls_back_without_swift_or_treesitter():
    from cognitive_compiler.codebrain_artifact import ArtifactNormalizer
    n = ArtifactNormalizer()
    assert n.swift_available is False
    assert n.tree_sitter_available is False
    assert n.fallback_reason is not None


def test_normalize_outputs_codebrain_artifact():
    from cognitive_compiler.codebrain_artifact import ArtifactNormalizer
    n = ArtifactNormalizer()
    out = n.normalize({"goal": "Build API", "metrics": {"x": 1}}, kind="design")
    assert out.kind == "design"
    assert out.title == "Build API"
    assert out.metrics["normalizer_backend"] == "generic"
    assert "artifact_id" in out.to_dict()
    assert out.normalized()["normalized"] is True


def test_best_backend_selection_generic_only():
    from cognitive_compiler.codebrain_artifact import ArtifactNormalizer
    n = ArtifactNormalizer()
    assert n.best_backend("// swift foo") == "generic"
    assert n.best_backend("python hello") == "generic"

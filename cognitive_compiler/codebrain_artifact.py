from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict
from typing import Any
from datetime import datetime, timezone


@dataclass
class CodeBrainArtifact:
    """Normalized representation of a code/design artifact for MSB v2."""
    artifact_id: str
    kind: str  # design | build | test | docs
    title: str
    body: str
    tags: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    relations: list[dict[str, str]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source: str = "building_harness"

    @staticmethod
    def from_dict(data: dict[str, Any]) -> CodeBrainArtifact:
        return CodeBrainArtifact(**data)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def normalized(self) -> dict[str, Any]:
        data = self.to_dict()
        data.setdefault("normalized", True)
        return data


class ArtifactNormalizer:
    """Converts raw build/design outputs into CodeBrainArtifact records.

    Backends inspected in order:
      1. SwiftSyntax parser if `swift` payload detected.
      2. Generic AST normalization fallback.
    """

    def __init__(self):
        self.swift_available = False
        self.tree_sitter_available = False
        self.fallback_reason: str | None = None
        self._detect_backends()

    def _detect_backends(self):
        # Swift and tree-sitter backends may be absent; normalize to generic fallback.
        try:
            import swiftlint  # noqa: F401
            self.swift_available = True
        except Exception:
            self.fallback_reason = self.fallback_reason or "swift backend unavailable"

        try:
            import tree_sitter  # noqa: F401
            self.tree_sitter_available = True
        except Exception:
            self.fallback_reason = self.fallback_reason or "tree-sitter backend unavailable"

    def best_backend(self, payload: str) -> str:
        if self.swift_available and payload.strip().startswith("// swift"):
            return "swift"
        if self.tree_sitter_available:
            return "tree-sitter"
        return "generic"

    def normalize(self, payload: dict[str, Any], kind: str = "design") -> CodeBrainArtifact:
        raw = payload.get("body") or payload.get("raw") or json.dumps(payload, default=str)
        title = payload.get("title") or payload.get("goal") or "Untitled artifact"
        tags = list(payload.get("tags") or [])
        metrics = dict(payload.get("metrics") or {})

        digest = hashlib.sha1(raw.encode("utf-8", errors="replace")).hexdigest()[:10]
        artifact_id = payload.get("artifact_id") or f"cb-{kind}-{digest}"

        relations = list(payload.get("relations") or [])
        backend = self.best_backend(raw)
        if backend == "generic":
            metrics["normalizer_backend"] = "generic"
            metrics["normalizer_fallback_reason"] = self.fallback_reason
        else:
            metrics["normalizer_backend"] = backend

        return CodeBrainArtifact(
            artifact_id=artifact_id,
            kind=kind,
            title=title,
            body=raw,
            tags=tags,
            metrics=metrics,
            relations=relations,
            source="artifact_normalizer",
        )


__all__ = ["CodeBrainArtifact", "ArtifactNormalizer"]

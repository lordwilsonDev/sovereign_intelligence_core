from __future__ import annotations

import importlib.util
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from cognitive_compiler.harness_abc import BaseHarness, HarnessResult, HarnessTelemetry


DEFAULT_ARTIFACT_DIR = Path.home() / ".hermes" / "artifacts"


@dataclass
class ArtifactManifest:
    id: str
    title: str
    kind: Optional[str]
    html_path: Optional[Path]
    bytes: Optional[int]
    created: Optional[str]


class TelegramArtifactHarness(BaseHarness):
    def __init__(self, artifact_dir: Optional[Path] = None, *, max_failures: int = 3) -> None:
        self.artifact_dir = (artifact_dir or DEFAULT_ARTIFACT_DIR).expanduser().resolve()
        self._max_failures = max_failures
        self._failures: Dict[str, int] = {}
        self._index: Dict[str, ArtifactManifest] = {}
        self._current_error: Optional[str] = None
        self.ready = False
        self._ensure_ready()

    def initialize(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self._ensure_ready()
        return {"ok": bool(self._index), "artifact_dir": str(self.artifact_dir)}

    def evaluate(self, query: str, context: Dict[str, Any]) -> HarnessResult:
        html = context.get("artifact_html")
        title = context.get("artifact_title") or "Artifact"
        kind = context.get("artifact_kind") or "html"
        if not html:
            return HarnessResult(ok=False, event="blocked", error="artifact_html is required", telemetry=HarnessTelemetry(error_class="input"))
        key = f"{kind}:{title}"
        if self._failures.get(key, 0) >= self._max_failures:
            return HarnessResult(ok=False, event="blocked", error=f"artifact kind={kind} too many failures; check token/host", telemetry=HarnessTelemetry(error_class="risk"))
        try:
            saved = self._save(html, title, kind)
            payload = {
                "id": saved.id,
                "title": saved.title,
                "kind": saved.kind,
                "html_path": str(saved.html_path) if saved.html_path else None,
                "bytes": saved.bytes,
                "created": saved.created,
                "status": "delivered",
            }
            self._index[saved.id] = saved
            telemetry = HarnessTelemetry(tags=["telegram", "artifact", kind])
            return HarnessResult(ok=True, event="delivered", payload=payload, telemetry=telemetry)
        except Exception as e:
            self._failures[key] = self._failures.get(key, 0) + 1
            return HarnessResult(ok=False, event="failed", error=str(e), telemetry=HarnessTelemetry(error_class="external"))

    def execute(self, query: str, *args: Any, context: Optional[Dict[str, Any]] = None, **kwargs: Any) -> HarnessResult:
        if context is None:
            context = {}
        if not self.ready:
            return HarnessResult(ok=False, event="blocked", error="artifact local storage unavailable", telemetry=HarnessTelemetry(error_class="prerequisite"))
        return self.evaluate(query, context)

    def observe(self, result: HarnessResult) -> Dict[str, Any]:
        return {
            "event": result.event,
            "id": result.payload.get("id"),
            "bytes": result.payload.get("bytes"),
            "error_class": result.telemetry.error_class,
        }

    def repair(self, result: HarnessResult) -> Optional[HarnessResult]:
        if result.ok:
            return None
        if result.telemetry.error_class in ("input", "prerequisite"):
            return None
        repaired = HarnessResult(ok=True, event="repair:queued", payload={"previous": result.event, "queued": True}, error=None, telemetry=HarnessTelemetry(tags=["telegram", "repair"]))
        return repaired

    def shutdown(self) -> Dict[str, Any]:
        return {"ok": True, "event": "shutdown", "index": len(self._index)}

    def _ensure_ready(self) -> None:
        self.ready = self.artifact_dir.exists()
        self._current_error = None if self.ready else "artifact dir missing"
        if self.ready:
            self._load_index()

    def _load_index(self) -> None:
        idx_path = self.artifact_dir / "index.json"
        if not idx_path.exists():
            self._index = {}
            return
        try:
            data = idx_path.read_text(encoding="utf-8")
            loaded = {}
            for entry in __import__("json").loads(data).get("artifacts", []):
                aid = entry.get("id")
                ts = entry.get("timestamp")
                rel = self.artifact_dir / f"{aid}.html" if aid else None
                loaded[aid] = ArtifactManifest(
                    id=str(aid),
                    title=str(entry.get("title", "")),
                    kind=str(entry.get("type")) if entry.get("type") else None,
                    html_path=rel if rel and rel.exists() else None,
                    bytes=rel.stat().st_size if rel and rel.exists() else None,
                    created=ts,
                )
            self._index = loaded
        except Exception:
            self._index = {}

    def _save(self, html: str, title: str, kind: str) -> ArtifactManifest:
        self.artifact_dir.mkdir(parents=True, exist_ok=True)
        ts = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat()
        source = f"{ts}{title}"
        aid = __import__("hashlib").sha256(source.encode()).hexdigest()[:12]
        html_path = self.artifact_dir / f"{aid}.html"
        html_path.write_text(html, encoding="utf-8")
        entry = {"id": aid, "title": title, "type": kind, "timestamp": ts}
        idx_path = self.artifact_dir / "index.json"
        idx = {}
        if idx_path.exists():
            try:
                idx = __import__("json").loads(idx_path.read_text(encoding="utf-8"))
            except Exception:
                idx = {"artifacts": []}
        idx["artifacts"] = [e for e in idx.get("artifacts", []) if e.get("id") != aid]
        idx["artifacts"].insert(0, entry)
        idx["artifacts"] = idx["artifacts"][:50]
        idx_path.write_text(__import__("json").dumps(idx, indent=2), encoding="utf-8")
        return ArtifactManifest(
            id=aid,
            title=title,
            kind=kind,
            html_path=html_path,
            bytes=html_path.stat().st_size if html_path.exists() else None,
            created=ts,
        )

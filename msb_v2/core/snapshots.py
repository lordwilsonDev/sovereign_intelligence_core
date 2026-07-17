from __future__ import annotations

import hashlib
import json
import shutil
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


class SnapshotManager:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def snapshot(self, tag: str, source: Path | str) -> str:
        src = Path(source).resolve()
        root = self.root.resolve()
        if not src.exists():
            raise FileNotFoundError(f"snapshot source missing: {src}")
        if root in src.parents or src == root:
            raise ValueError("cannot snapshot the snapshot root into itself")
        ts = datetime.now(timezone.utc).isoformat() + "Z"
        name = f"{tag}__{ts}".replace(":", "-")
        dest = root / name
        if dest.exists():
            raise FileExistsError(f"snapshot already exists: {dest}")
        with self._lock:
            if src.is_dir():
                shutil.copytree(src, dest, dirs_exist_ok=False)
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
            if dest.exists():
                meta = _meta_path(dest)
                meta.write_text(
                    json.dumps({"tag": tag, "source": str(src), "created": ts}),
                    encoding="utf-8",
                )
        return tag

    def rollback(self, tag: str, dest: Path | str) -> None:
        target = Path(dest)
        candidates = sorted(self.root.glob(f"{tag}__*"), reverse=True)
        if not candidates:
            raise FileNotFoundError(f"no snapshot for tag={tag}")
        src = candidates[0]
        _strip_meta(src)
        with self._lock:
            if target.exists():
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()
            if src.is_dir():
                shutil.copytree(src, target)
            else:
                shutil.copy2(src, target)

    def list_snapshots(self, tag: str) -> list[dict[str, str]]:
        out: list[dict[str, str]] = []
        for path in sorted(self.root.glob(f"{tag}__*")):
            meta = _read_meta(path)
            meta["path"] = str(path)
            out.append(meta)
        return out


def _meta_path(snapshot: Path) -> Path:
    return snapshot / ".snapshot_meta.json" if snapshot.is_dir() else snapshot.with_suffix(snapshot.suffix + ".snapshot_meta.json")


def _write_meta(snapshot: Path, *, tag: str, source: str, created: str) -> None:
    meta = _meta_path(snapshot)
    meta.write_text(json.dumps({"tag": tag, "source": source, "created": created}), encoding="utf-8")


def _read_meta(snapshot: Path) -> dict[str, str]:
    meta = _meta_path(snapshot)
    if not meta.exists():
        return {}
    try:
        return json.loads(meta.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _strip_meta(snapshot: Path) -> None:
    meta = _meta_path(snapshot)
    if meta.exists():
        meta.unlink()
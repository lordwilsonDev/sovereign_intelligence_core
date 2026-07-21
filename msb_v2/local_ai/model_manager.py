from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
import subprocess
import time


@dataclass(frozen=True)
class LocalModel:
    id: str
    source: str  # "ollama" | "hf"
    size_bytes: Optional[int] = None
    modified_at: Optional[str] = None
    last_used_at: Optional[str] = None
    license: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ModelManager:
    def __init__(self, cache_dir: Optional[Path] = None) -> None:
        self.cache_dir = Path(cache_dir or Path.home() / ".cache" / "msb" / "models")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._manifest_path = self.cache_dir / "manifest.json"
        self._manifest: Dict[str, Dict[str, Any]] = self._load_manifest()

    def _load_manifest(self) -> Dict[str, Dict[str, Any]]:
        if self._manifest_path.exists():
            return json.loads(self._manifest_path.read_text())
        return {}

    def _save_manifest(self) -> None:
        self._manifest_path.write_text(json.dumps(self._manifest, indent=2))

    def list_models(self) -> List[LocalModel]:
        models: List[LocalModel] = []
        models.extend(self._list_ollama())
        models.extend(self._list_hf())
        return models

    def _list_ollama(self) -> List[LocalModel]:
        try:
            out = subprocess.check_output(["ollama", "list"], text=True)
        except Exception:
            return []
        models: List[LocalModel] = []
        for line in out.splitlines()[1:]:
            parts = line.split()
            if not parts:
                continue
            name = parts[0]
            size_str = parts[1] if len(parts) > 1 else None
            size_bytes = self._parse_size(size_str)
            modified = parts[2] + " " + parts[3] if len(parts) >= 4 else None
            meta = self._manifest.get(name, {})
            models.append(LocalModel(
                id=name,
                source="ollama",
                size_bytes=size_bytes,
                modified_at=modified,
                last_used_at=meta.get("last_used_at"),
                license=meta.get("license"),
                metadata=meta,
            ))
        return models

    def _list_hf(self) -> List[LocalModel]:
        hf_cache = Path.home() / ".cache" / "huggingface" / "hub"
        models: List[LocalModel] = []
        if not hf_cache.exists():
            return models
        for repo_dir in hf_cache.iterdir():
            config = repo_dir / "config.json"
            if not config.exists():
                continue
            name = repo_dir.name.replace("models--", "").replace("--", "/")
            models.append(LocalModel(id=name, source="hf", modified_at=None, last_used_at=None))
        return models

    @staticmethod
    def _parse_size(value: Optional[str]) -> Optional[int]:
        if not value:
            return None
        value = value.strip()
        if value.endswith("GB"):
            return int(float(value[:-2]) * 1_073_741_824)
        if value.endswith("MB"):
            return int(float(value[:-2]) * 1_048_576)
        if value.endswith("KB"):
            return int(float(value[:-2]) * 1024)
        try:
            return int(value)
        except ValueError:
            return None

    def record_use(self, model_id: str) -> None:
        self._manifest.setdefault(model_id, {})["last_used_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self._save_manifest()

    def pull_model(self, source: str, model_id: str, license_: Optional[str] = None) -> LocalModel:
        if source == "ollama":
            subprocess.check_call(["ollama", "pull", model_id])
        else:
            from huggingface_hub import snapshot_download
            snapshot_download(repo_id=model_id, local_dir=str(self.cache_dir / model_id.replace("/", "--")))
        self._manifest.setdefault(model_id, {})["license"] = license_
        self._save_manifest()
        self.record_use(model_id)
        return next((m for m in self.list_models() if m.id == model_id), LocalModel(id=model_id, source=source, license=license_))

    def remove_model(self, model_id: str) -> None:
        source = self._manifest.get(model_id, {}).get("source") or "ollama"
        if source == "ollama":
            subprocess.check_call(["ollama", "rm", model_id])
        else:
            target = self.cache_dir / model_id.replace("/", "--")
            if target.exists():
                for child in target.iterdir():
                    child.unlink()
                target.rmdir()
        self._manifest.pop(model_id, None)
        self._save_manifest()

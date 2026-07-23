"""Sovereign Snapshot Engine — encrypted local zip backups."""
import os
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import pyzipper

SNAPSHOT_PASSWORD = os.getenv("MSB_SNAPSHOT_PASSWORD", "msb-sovereign-backup")


class SnapshotEngine:
    """Captures sovereign state into an encrypted local zip archive."""

    def __init__(self, repo_path: Path | None = None) -> None:
        self.repo_path = repo_path or Path(__file__).resolve().parent.parent.parent
        self.backup_dir = Path.home() / "msb-backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def capture(self) -> Dict[str, Any]:
        """Take a full snapshot and save as encrypted zip."""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        snapshot_id = timestamp.replace(":", "-")
        temp_dir = self.backup_dir / f"temp_{snapshot_id}"
        temp_dir.mkdir(parents=True, exist_ok=True)

        memory_src = self.repo_path / "data" / "evolution_memory.jsonl"
        if memory_src.exists():
            shutil.copy2(memory_src, temp_dir / "evolution_memory.jsonl")

        audit_dir = self.repo_path / "runtime" / "audit"
        if audit_dir.exists():
            shutil.copytree(audit_dir, temp_dir / "audit", dirs_exist_ok=True)

        research_dir = self.repo_path / "runtime" / "research"
        if research_dir.exists():
            shutil.copytree(research_dir, temp_dir / "research", dirs_exist_ok=True)

        voiceprint_file = self.repo_path / "msb_v2" / "cloud_agent" / "voiceprint_baseline.json"
        if voiceprint_file.exists():
            shutil.copy2(voiceprint_file, temp_dir / "voiceprint_baseline.json")

        env_file = self.repo_path / ".env"
        if env_file.exists():
            shutil.copy2(env_file, temp_dir / "dot_env")

        try:
            import requests
            sac = requests.get("http://127.0.0.1:8766/sac/status", timeout=5).json()
            with open(temp_dir / "sac_status.json", "w") as f:
                json.dump(sac, f, indent=2)
        except Exception:
            pass

        try:
            import requests
            jobs = requests.get("http://127.0.0.1:8766/star/jobs", timeout=5).json()
            with open(temp_dir / "star_jobs.json", "w") as f:
                json.dump(jobs, f, indent=2)
        except Exception:
            pass

        meta = {"snapshot_id": snapshot_id, "timestamp": timestamp}
        with open(temp_dir / "metadata.json", "w") as f:
            json.dump(meta, f, indent=2)

        zip_path = self.backup_dir / f"{snapshot_id}.zip"
        with pyzipper.AESZipFile(
            zip_path,
            "w",
            compression=pyzipper.ZIP_DEFLATED,
            encryption=pyzipper.WZ_AES,
        ) as zf:
            zf.setpassword(SNAPSHOT_PASSWORD.encode())
            for root, _dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(temp_dir)
                    zf.write(file_path, arcname)

        shutil.rmtree(temp_dir)

        return {"snapshot_id": snapshot_id, "path": str(zip_path), "status": "captured"}

    def list_snapshots(self) -> list:
        """Return available local snapshots, newest first."""
        if not self.backup_dir.exists():
            return []
        zips = sorted(self.backup_dir.glob("*.zip"), key=os.path.getmtime, reverse=True)
        return [z.name for z in zips[:10]]

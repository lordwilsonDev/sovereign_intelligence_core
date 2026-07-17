from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from msb_v2.eve.discovery import discover
from msb_v2.eve.manifest import compile_manifest


AGENT_ROOT = "/Users/lordwilson/msb-v2"


def refresh_manifest(root: str = AGENT_ROOT, **_: Dict[str, Any]) -> Dict[str, Any]:
    result = discover(Path(root))
    manifest = compile_manifest(result)
    payload = {
        "kind": manifest.kind,
        "version": manifest.version,
        "tools": [t.name for t in manifest.tools],
        "skills": [s.name for s in manifest.skills],
        "schedules": [s.name for s in manifest.schedules],
        "tool_count": len(manifest.tools),
        "skill_count": len(manifest.skills),
        "schedule_count": len(manifest.schedules),
    }
    return {"status": "ok", "message": "manifest refreshed", "manifest": payload, "confidence": 1.0}

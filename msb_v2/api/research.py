from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter

from msb_v2.research.assistant import SovereignResearchAssistant

router = APIRouter()
_RUNTIME_ROOT = Path("runtime/research")


def _probe(path: str, expected_key: str = "system_readiness") -> Dict[str, Any]:
    import requests
    try:
        r = requests.get(f"http://127.0.0.1:8766{path}", timeout=3)
        if r.ok:
            data = r.json()
            return {"path": path, "ok": True, "value": data.get(expected_key) or data.get("status") or data.get("readiness")}
    except Exception as exc:
        return {"path": path, "ok": False, "error": str(exc)}
    return {"path": path, "ok": False}


@router.get("/assistant/preflight")
def research_preflight() -> Dict[str, Any]:
    checks = {
        "health": _probe("/health", "status"),
        "schh": _probe("/schh/status"),
        "sshh": _probe("/systems-health/status"),
        "sac": _probe("/sac/status"),
    }
    failed = [name for name, result in checks.items() if not result.get("ok")]
    return {"checks": checks, "passed": len(failed) == 0, "failed": failed}


@router.post("/assistant/run")
def run_research_assistant(payload: Dict[str, Any]) -> Dict[str, Any]:
    phase_hint = payload.get("phase") if isinstance(payload, dict) else None
    topic = str(payload.get("topic") if isinstance(payload, dict) else None) or "sovereign-local-llm-economics"
    from msb_v2.research.assistant import _slugify as _topic_slugify
    slug = _topic_slugify(topic)
    root = _RUNTIME_ROOT / slug
    try:
        assistant = SovereignResearchAssistant(topic=topic, root=root)
        if phase_hint == "literature_scan":
            return assistant.run_inversion()
        if phase_hint == "hypothesis_generation":
            return assistant.run_full_pipeline()
        if phase_hint == "report_synthesis":
            return {"status": "ok", "topic": topic, "phase": "completed", "path": str(assistant.draft_report())}
        return assistant.run_full_pipeline()
    except Exception as exc:
        return {
            "status": "error",
            "phase": phase_hint,
            "topic": topic,
            "error": str(exc),
        }


@router.get("/assistant/status")
def research_assistant_status() -> Dict[str, Any]:
    if not _RUNTIME_ROOT.exists():
        return {"status": "ok", "artifacts": []}
    artifacts = [p.name for p in _RUNTIME_ROOT.glob("*") if p.is_file()]
    return {"status": "ok", "artifacts": sorted(artifacts)}


@router.get("/assistant/latest")
def latest_research_artifact() -> Dict[str, Any]:
    latest = None
    latest_mtime = 0.0
    if _RUNTIME_ROOT.exists():
        for path in _RUNTIME_ROOT.glob("*_completion.json"):
            try:
                mtime = path.stat().st_mtime
            except FileNotFoundError:
                continue
            if mtime > latest_mtime:
                latest_mtime = mtime
                latest = path
    if not latest:
        return {"status": "not_found"}
    try:
        data = json.loads(latest.read_text(encoding="utf-8"))
    except Exception:
        return {"status": "error", "path": str(latest)}
    return {"status": "ok", "path": str(latest), "data": data}

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from msb_v2.eve.discovery import discover
from msb_v2.eve.manifest import compile_manifest

router = APIRouter()
_AGENT_ROOT = Path(__file__).resolve().parent.parent.parent


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class ScheduleResponse(BaseModel):
    name: str
    path: str
    sha256: str
    raw: Dict[str, Any]


@router.get("/schedules", response_model=List[ScheduleResponse])
def eve_schedules(root: Optional[str] = None) -> List[Dict[str, Any]]:
    agent_root = Path(root).resolve() if root else _AGENT_ROOT
    result = discover(agent_root)
    schedules = result.schedules
    manifest = compile_manifest(result)
    schedule_map: Dict[str, Any] = {s.name: s for s in manifest.schedules}
    payload: List[Dict[str, Any]] = []
    for schedule in schedules:
        compiled = schedule_map.get(schedule.name)
        payload.append(
            {
                "name": schedule.name,
                "path": schedule.path,
                "sha256": compiled.sha256 if compiled else "",
                "raw": schedule.raw or {},
            }
        )
    return payload

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from msb_v2.eve.discovery import discover
from msb_v2.eve.manifest import compile_manifest, manifest_to_dict

router = APIRouter()


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class ManifestResponse(BaseModel):
    kind: str
    version: int
    tools: list[Dict[str, Any]]
    skills: list[Dict[str, Any]]
    schedules: list[Dict[str, Any]]


@router.get("/manifest", response_model=ManifestResponse)
def eve_manifest(root: Optional[str] = None) -> Dict[str, Any]:
    agent_root = Path(root).resolve() if root else Path(__file__).resolve().parent.parent.parent
    result = discover(agent_root)
    manifest = compile_manifest(result)
    return manifest_to_dict(manifest)

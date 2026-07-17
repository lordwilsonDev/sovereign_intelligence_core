from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from msb_v2.eve.discovery import DiscoveryResult


@dataclass(frozen=True)
class CompiledToolDef:
    name: str
    path: str
    kind: str
    docstring: Optional[str]


@dataclass(frozen=True)
class CompiledSkillDef:
    name: str
    path: str
    sha256: str
    frontmatter: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CompiledScheduleDef:
    name: str
    path: str
    raw: Dict[str, Any]
    sha256: str


@dataclass(frozen=True)
class CompiledManifest:
    kind: str = "msb-eve-compiled-manifest"
    version: int = 1
    tools: List[CompiledToolDef] = field(default_factory=list)
    skills: List[CompiledSkillDef] = field(default_factory=list)
    schedules: List[CompiledScheduleDef] = field(default_factory=list)


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _extract_frontmatter(raw: str) -> Dict[str, Any]:
    if not raw.startswith("---"):
        return {}
    end = raw.find("---", 3)
    if end == -1:
        return {}
    block = raw[3:end].strip()
    out: Dict[str, Any] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip()
    return out


def compile_manifest(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def manifest_to_dict(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "tools": [
            {"name": t.name, "path": t.path, "kind": t.kind, "docstring": t.docstring}
            for t in manifest.tools
        ],
        "skills": [
            {"name": s.name, "path": s.path, "sha256": s.sha256, "frontmatter": s.frontmatter}
            for s in manifest.skills
        ],
        "schedules": [
            {"name": s.name, "path": s.path, "sha256": s.sha256, "raw": s.raw}
            for s in manifest.schedules
        ],
    }

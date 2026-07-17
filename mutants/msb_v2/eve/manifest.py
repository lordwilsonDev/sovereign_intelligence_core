from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from msb_v2.eve.discovery import DiscoveryResult


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


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
mutants_x__sha256__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__sha256__mutmut)
def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def x__sha256__mutmut_orig(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def x__sha256__mutmut_1(text: str) -> str:
    return hashlib.sha256(None).hexdigest()


def x__sha256__mutmut_2(text: str) -> str:
    return hashlib.sha256(text.encode(None)).hexdigest()


def x__sha256__mutmut_3(text: str) -> str:
    return hashlib.sha256(text.encode("XXutf-8XX")).hexdigest()


def x__sha256__mutmut_4(text: str) -> str:
    return hashlib.sha256(text.encode("UTF-8")).hexdigest()

mutants_x__sha256__mutmut['_mutmut_orig'] = x__sha256__mutmut_orig # type: ignore # mutmut generated
mutants_x__sha256__mutmut['x__sha256__mutmut_1'] = x__sha256__mutmut_1 # type: ignore # mutmut generated
mutants_x__sha256__mutmut['x__sha256__mutmut_2'] = x__sha256__mutmut_2 # type: ignore # mutmut generated
mutants_x__sha256__mutmut['x__sha256__mutmut_3'] = x__sha256__mutmut_3 # type: ignore # mutmut generated
mutants_x__sha256__mutmut['x__sha256__mutmut_4'] = x__sha256__mutmut_4 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__extract_frontmatter__mutmut)
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


def x__extract_frontmatter__mutmut_orig(raw: str) -> Dict[str, Any]:
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


def x__extract_frontmatter__mutmut_1(raw: str) -> Dict[str, Any]:
    if raw.startswith("---"):
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


def x__extract_frontmatter__mutmut_2(raw: str) -> Dict[str, Any]:
    if not raw.startswith(None):
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


def x__extract_frontmatter__mutmut_3(raw: str) -> Dict[str, Any]:
    if not raw.startswith("XX---XX"):
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


def x__extract_frontmatter__mutmut_4(raw: str) -> Dict[str, Any]:
    if not raw.startswith("---"):
        return {}
    end = None
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


def x__extract_frontmatter__mutmut_5(raw: str) -> Dict[str, Any]:
    if not raw.startswith("---"):
        return {}
    end = raw.find(None, 3)
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


def x__extract_frontmatter__mutmut_6(raw: str) -> Dict[str, Any]:
    if not raw.startswith("---"):
        return {}
    end = raw.find("---", None)
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


def x__extract_frontmatter__mutmut_7(raw: str) -> Dict[str, Any]:
    if not raw.startswith("---"):
        return {}
    end = raw.find(3)
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


def x__extract_frontmatter__mutmut_8(raw: str) -> Dict[str, Any]:
    if not raw.startswith("---"):
        return {}
    end = raw.find("---", )
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


def x__extract_frontmatter__mutmut_9(raw: str) -> Dict[str, Any]:
    if not raw.startswith("---"):
        return {}
    end = raw.rfind("---", 3)
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


def x__extract_frontmatter__mutmut_10(raw: str) -> Dict[str, Any]:
    if not raw.startswith("---"):
        return {}
    end = raw.find("XX---XX", 3)
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


def x__extract_frontmatter__mutmut_11(raw: str) -> Dict[str, Any]:
    if not raw.startswith("---"):
        return {}
    end = raw.find("---", 4)
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


def x__extract_frontmatter__mutmut_12(raw: str) -> Dict[str, Any]:
    if not raw.startswith("---"):
        return {}
    end = raw.find("---", 3)
    if end != -1:
        return {}
    block = raw[3:end].strip()
    out: Dict[str, Any] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip()
    return out


def x__extract_frontmatter__mutmut_13(raw: str) -> Dict[str, Any]:
    if not raw.startswith("---"):
        return {}
    end = raw.find("---", 3)
    if end == +1:
        return {}
    block = raw[3:end].strip()
    out: Dict[str, Any] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip()
    return out


def x__extract_frontmatter__mutmut_14(raw: str) -> Dict[str, Any]:
    if not raw.startswith("---"):
        return {}
    end = raw.find("---", 3)
    if end == -2:
        return {}
    block = raw[3:end].strip()
    out: Dict[str, Any] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip()
    return out


def x__extract_frontmatter__mutmut_15(raw: str) -> Dict[str, Any]:
    if not raw.startswith("---"):
        return {}
    end = raw.find("---", 3)
    if end == -1:
        return {}
    block = None
    out: Dict[str, Any] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip()
    return out


def x__extract_frontmatter__mutmut_16(raw: str) -> Dict[str, Any]:
    if not raw.startswith("---"):
        return {}
    end = raw.find("---", 3)
    if end == -1:
        return {}
    block = raw[4:end].strip()
    out: Dict[str, Any] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip()
    return out


def x__extract_frontmatter__mutmut_17(raw: str) -> Dict[str, Any]:
    if not raw.startswith("---"):
        return {}
    end = raw.find("---", 3)
    if end == -1:
        return {}
    block = raw[3:end].strip()
    out: Dict[str, Any] = None
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip()
    return out


def x__extract_frontmatter__mutmut_18(raw: str) -> Dict[str, Any]:
    if not raw.startswith("---"):
        return {}
    end = raw.find("---", 3)
    if end == -1:
        return {}
    block = raw[3:end].strip()
    out: Dict[str, Any] = {}
    for line in block.splitlines():
        if "XX:XX" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip()
    return out


def x__extract_frontmatter__mutmut_19(raw: str) -> Dict[str, Any]:
    if not raw.startswith("---"):
        return {}
    end = raw.find("---", 3)
    if end == -1:
        return {}
    block = raw[3:end].strip()
    out: Dict[str, Any] = {}
    for line in block.splitlines():
        if ":" in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip()
    return out


def x__extract_frontmatter__mutmut_20(raw: str) -> Dict[str, Any]:
    if not raw.startswith("---"):
        return {}
    end = raw.find("---", 3)
    if end == -1:
        return {}
    block = raw[3:end].strip()
    out: Dict[str, Any] = {}
    for line in block.splitlines():
        if ":" not in line:
            break
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip()
    return out


def x__extract_frontmatter__mutmut_21(raw: str) -> Dict[str, Any]:
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
        key, value = None
        out[key.strip()] = value.strip()
    return out


def x__extract_frontmatter__mutmut_22(raw: str) -> Dict[str, Any]:
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
        key, value = line.split(None, 1)
        out[key.strip()] = value.strip()
    return out


def x__extract_frontmatter__mutmut_23(raw: str) -> Dict[str, Any]:
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
        key, value = line.split(":", None)
        out[key.strip()] = value.strip()
    return out


def x__extract_frontmatter__mutmut_24(raw: str) -> Dict[str, Any]:
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
        key, value = line.split(1)
        out[key.strip()] = value.strip()
    return out


def x__extract_frontmatter__mutmut_25(raw: str) -> Dict[str, Any]:
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
        key, value = line.split(":", )
        out[key.strip()] = value.strip()
    return out


def x__extract_frontmatter__mutmut_26(raw: str) -> Dict[str, Any]:
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
        key, value = line.rsplit(":", 1)
        out[key.strip()] = value.strip()
    return out


def x__extract_frontmatter__mutmut_27(raw: str) -> Dict[str, Any]:
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
        key, value = line.split("XX:XX", 1)
        out[key.strip()] = value.strip()
    return out


def x__extract_frontmatter__mutmut_28(raw: str) -> Dict[str, Any]:
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
        key, value = line.split(":", 2)
        out[key.strip()] = value.strip()
    return out


def x__extract_frontmatter__mutmut_29(raw: str) -> Dict[str, Any]:
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
        out[key.strip()] = None
    return out

mutants_x__extract_frontmatter__mutmut['_mutmut_orig'] = x__extract_frontmatter__mutmut_orig # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_1'] = x__extract_frontmatter__mutmut_1 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_2'] = x__extract_frontmatter__mutmut_2 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_3'] = x__extract_frontmatter__mutmut_3 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_4'] = x__extract_frontmatter__mutmut_4 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_5'] = x__extract_frontmatter__mutmut_5 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_6'] = x__extract_frontmatter__mutmut_6 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_7'] = x__extract_frontmatter__mutmut_7 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_8'] = x__extract_frontmatter__mutmut_8 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_9'] = x__extract_frontmatter__mutmut_9 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_10'] = x__extract_frontmatter__mutmut_10 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_11'] = x__extract_frontmatter__mutmut_11 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_12'] = x__extract_frontmatter__mutmut_12 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_13'] = x__extract_frontmatter__mutmut_13 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_14'] = x__extract_frontmatter__mutmut_14 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_15'] = x__extract_frontmatter__mutmut_15 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_16'] = x__extract_frontmatter__mutmut_16 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_17'] = x__extract_frontmatter__mutmut_17 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_18'] = x__extract_frontmatter__mutmut_18 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_19'] = x__extract_frontmatter__mutmut_19 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_20'] = x__extract_frontmatter__mutmut_20 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_21'] = x__extract_frontmatter__mutmut_21 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_22'] = x__extract_frontmatter__mutmut_22 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_23'] = x__extract_frontmatter__mutmut_23 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_24'] = x__extract_frontmatter__mutmut_24 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_25'] = x__extract_frontmatter__mutmut_25 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_26'] = x__extract_frontmatter__mutmut_26 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_27'] = x__extract_frontmatter__mutmut_27 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_28'] = x__extract_frontmatter__mutmut_28 # type: ignore # mutmut generated
mutants_x__extract_frontmatter__mutmut['x__extract_frontmatter__mutmut_29'] = x__extract_frontmatter__mutmut_29 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_compile_manifest__mutmut)
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


def x_compile_manifest__mutmut_orig(result: DiscoveryResult) -> CompiledManifest:
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


def x_compile_manifest__mutmut_1(result: DiscoveryResult) -> CompiledManifest:
    tools = None
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_2(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=None, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_3(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=None, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_4(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=None, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_5(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=None) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_6(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_7(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_8(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_9(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, ) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_10(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = None
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_11(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = None
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_12(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(None)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_13(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(None)
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_14(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=None, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_15(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=None, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_16(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=None, frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_17(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=None))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_18(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_19(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_20(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_21(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), ))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_22(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(None), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_23(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = None
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_24(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=None, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_25(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=None, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_26(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=None, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_27(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=None)
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_28(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_29(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_30(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_31(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, )
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_32(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw and {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_33(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(None))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_34(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(None, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_35(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=None)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_36(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_37(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, )))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_38(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw and {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_39(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=False)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_40(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=None, skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_41(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=None, schedules=schedules)


def x_compile_manifest__mutmut_42(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, schedules=None)


def x_compile_manifest__mutmut_43(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(skills=skills, schedules=schedules)


def x_compile_manifest__mutmut_44(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, schedules=schedules)


def x_compile_manifest__mutmut_45(result: DiscoveryResult) -> CompiledManifest:
    tools = [CompiledToolDef(name=t.name, path=t.path, kind=t.kind, docstring=t.docstring) for t in result.tools]
    skills = []
    for s in result.skills:
        frontmatter = _extract_frontmatter(s.raw)
        skills.append(CompiledSkillDef(name=s.name, path=s.path, sha256=_sha256(s.raw), frontmatter=frontmatter))
    schedules = [
        CompiledScheduleDef(name=s.name, path=s.path, raw=s.raw or {}, sha256=_sha256(json.dumps(s.raw or {}, sort_keys=True)))
        for s in result.schedules
    ]
    return CompiledManifest(tools=tools, skills=skills, )

mutants_x_compile_manifest__mutmut['_mutmut_orig'] = x_compile_manifest__mutmut_orig # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_1'] = x_compile_manifest__mutmut_1 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_2'] = x_compile_manifest__mutmut_2 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_3'] = x_compile_manifest__mutmut_3 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_4'] = x_compile_manifest__mutmut_4 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_5'] = x_compile_manifest__mutmut_5 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_6'] = x_compile_manifest__mutmut_6 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_7'] = x_compile_manifest__mutmut_7 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_8'] = x_compile_manifest__mutmut_8 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_9'] = x_compile_manifest__mutmut_9 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_10'] = x_compile_manifest__mutmut_10 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_11'] = x_compile_manifest__mutmut_11 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_12'] = x_compile_manifest__mutmut_12 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_13'] = x_compile_manifest__mutmut_13 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_14'] = x_compile_manifest__mutmut_14 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_15'] = x_compile_manifest__mutmut_15 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_16'] = x_compile_manifest__mutmut_16 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_17'] = x_compile_manifest__mutmut_17 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_18'] = x_compile_manifest__mutmut_18 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_19'] = x_compile_manifest__mutmut_19 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_20'] = x_compile_manifest__mutmut_20 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_21'] = x_compile_manifest__mutmut_21 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_22'] = x_compile_manifest__mutmut_22 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_23'] = x_compile_manifest__mutmut_23 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_24'] = x_compile_manifest__mutmut_24 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_25'] = x_compile_manifest__mutmut_25 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_26'] = x_compile_manifest__mutmut_26 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_27'] = x_compile_manifest__mutmut_27 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_28'] = x_compile_manifest__mutmut_28 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_29'] = x_compile_manifest__mutmut_29 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_30'] = x_compile_manifest__mutmut_30 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_31'] = x_compile_manifest__mutmut_31 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_32'] = x_compile_manifest__mutmut_32 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_33'] = x_compile_manifest__mutmut_33 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_34'] = x_compile_manifest__mutmut_34 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_35'] = x_compile_manifest__mutmut_35 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_36'] = x_compile_manifest__mutmut_36 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_37'] = x_compile_manifest__mutmut_37 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_38'] = x_compile_manifest__mutmut_38 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_39'] = x_compile_manifest__mutmut_39 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_40'] = x_compile_manifest__mutmut_40 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_41'] = x_compile_manifest__mutmut_41 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_42'] = x_compile_manifest__mutmut_42 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_43'] = x_compile_manifest__mutmut_43 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_44'] = x_compile_manifest__mutmut_44 # type: ignore # mutmut generated
mutants_x_compile_manifest__mutmut['x_compile_manifest__mutmut_45'] = x_compile_manifest__mutmut_45 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_manifest_to_dict__mutmut)
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


def x_manifest_to_dict__mutmut_orig(manifest: CompiledManifest) -> Dict[str, Any]:
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


def x_manifest_to_dict__mutmut_1(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "XXkindXX": manifest.kind,
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


def x_manifest_to_dict__mutmut_2(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "KIND": manifest.kind,
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


def x_manifest_to_dict__mutmut_3(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "XXversionXX": manifest.version,
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


def x_manifest_to_dict__mutmut_4(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "VERSION": manifest.version,
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


def x_manifest_to_dict__mutmut_5(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "XXtoolsXX": [
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


def x_manifest_to_dict__mutmut_6(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "TOOLS": [
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


def x_manifest_to_dict__mutmut_7(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "tools": [
            {"XXnameXX": t.name, "path": t.path, "kind": t.kind, "docstring": t.docstring}
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


def x_manifest_to_dict__mutmut_8(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "tools": [
            {"NAME": t.name, "path": t.path, "kind": t.kind, "docstring": t.docstring}
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


def x_manifest_to_dict__mutmut_9(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "tools": [
            {"name": t.name, "XXpathXX": t.path, "kind": t.kind, "docstring": t.docstring}
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


def x_manifest_to_dict__mutmut_10(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "tools": [
            {"name": t.name, "PATH": t.path, "kind": t.kind, "docstring": t.docstring}
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


def x_manifest_to_dict__mutmut_11(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "tools": [
            {"name": t.name, "path": t.path, "XXkindXX": t.kind, "docstring": t.docstring}
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


def x_manifest_to_dict__mutmut_12(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "tools": [
            {"name": t.name, "path": t.path, "KIND": t.kind, "docstring": t.docstring}
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


def x_manifest_to_dict__mutmut_13(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "tools": [
            {"name": t.name, "path": t.path, "kind": t.kind, "XXdocstringXX": t.docstring}
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


def x_manifest_to_dict__mutmut_14(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "tools": [
            {"name": t.name, "path": t.path, "kind": t.kind, "DOCSTRING": t.docstring}
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


def x_manifest_to_dict__mutmut_15(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "tools": [
            {"name": t.name, "path": t.path, "kind": t.kind, "docstring": t.docstring}
            for t in manifest.tools
        ],
        "XXskillsXX": [
            {"name": s.name, "path": s.path, "sha256": s.sha256, "frontmatter": s.frontmatter}
            for s in manifest.skills
        ],
        "schedules": [
            {"name": s.name, "path": s.path, "sha256": s.sha256, "raw": s.raw}
            for s in manifest.schedules
        ],
    }


def x_manifest_to_dict__mutmut_16(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "tools": [
            {"name": t.name, "path": t.path, "kind": t.kind, "docstring": t.docstring}
            for t in manifest.tools
        ],
        "SKILLS": [
            {"name": s.name, "path": s.path, "sha256": s.sha256, "frontmatter": s.frontmatter}
            for s in manifest.skills
        ],
        "schedules": [
            {"name": s.name, "path": s.path, "sha256": s.sha256, "raw": s.raw}
            for s in manifest.schedules
        ],
    }


def x_manifest_to_dict__mutmut_17(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "tools": [
            {"name": t.name, "path": t.path, "kind": t.kind, "docstring": t.docstring}
            for t in manifest.tools
        ],
        "skills": [
            {"XXnameXX": s.name, "path": s.path, "sha256": s.sha256, "frontmatter": s.frontmatter}
            for s in manifest.skills
        ],
        "schedules": [
            {"name": s.name, "path": s.path, "sha256": s.sha256, "raw": s.raw}
            for s in manifest.schedules
        ],
    }


def x_manifest_to_dict__mutmut_18(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "tools": [
            {"name": t.name, "path": t.path, "kind": t.kind, "docstring": t.docstring}
            for t in manifest.tools
        ],
        "skills": [
            {"NAME": s.name, "path": s.path, "sha256": s.sha256, "frontmatter": s.frontmatter}
            for s in manifest.skills
        ],
        "schedules": [
            {"name": s.name, "path": s.path, "sha256": s.sha256, "raw": s.raw}
            for s in manifest.schedules
        ],
    }


def x_manifest_to_dict__mutmut_19(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "tools": [
            {"name": t.name, "path": t.path, "kind": t.kind, "docstring": t.docstring}
            for t in manifest.tools
        ],
        "skills": [
            {"name": s.name, "XXpathXX": s.path, "sha256": s.sha256, "frontmatter": s.frontmatter}
            for s in manifest.skills
        ],
        "schedules": [
            {"name": s.name, "path": s.path, "sha256": s.sha256, "raw": s.raw}
            for s in manifest.schedules
        ],
    }


def x_manifest_to_dict__mutmut_20(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "tools": [
            {"name": t.name, "path": t.path, "kind": t.kind, "docstring": t.docstring}
            for t in manifest.tools
        ],
        "skills": [
            {"name": s.name, "PATH": s.path, "sha256": s.sha256, "frontmatter": s.frontmatter}
            for s in manifest.skills
        ],
        "schedules": [
            {"name": s.name, "path": s.path, "sha256": s.sha256, "raw": s.raw}
            for s in manifest.schedules
        ],
    }


def x_manifest_to_dict__mutmut_21(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "tools": [
            {"name": t.name, "path": t.path, "kind": t.kind, "docstring": t.docstring}
            for t in manifest.tools
        ],
        "skills": [
            {"name": s.name, "path": s.path, "XXsha256XX": s.sha256, "frontmatter": s.frontmatter}
            for s in manifest.skills
        ],
        "schedules": [
            {"name": s.name, "path": s.path, "sha256": s.sha256, "raw": s.raw}
            for s in manifest.schedules
        ],
    }


def x_manifest_to_dict__mutmut_22(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "tools": [
            {"name": t.name, "path": t.path, "kind": t.kind, "docstring": t.docstring}
            for t in manifest.tools
        ],
        "skills": [
            {"name": s.name, "path": s.path, "SHA256": s.sha256, "frontmatter": s.frontmatter}
            for s in manifest.skills
        ],
        "schedules": [
            {"name": s.name, "path": s.path, "sha256": s.sha256, "raw": s.raw}
            for s in manifest.schedules
        ],
    }


def x_manifest_to_dict__mutmut_23(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "tools": [
            {"name": t.name, "path": t.path, "kind": t.kind, "docstring": t.docstring}
            for t in manifest.tools
        ],
        "skills": [
            {"name": s.name, "path": s.path, "sha256": s.sha256, "XXfrontmatterXX": s.frontmatter}
            for s in manifest.skills
        ],
        "schedules": [
            {"name": s.name, "path": s.path, "sha256": s.sha256, "raw": s.raw}
            for s in manifest.schedules
        ],
    }


def x_manifest_to_dict__mutmut_24(manifest: CompiledManifest) -> Dict[str, Any]:
    return {
        "kind": manifest.kind,
        "version": manifest.version,
        "tools": [
            {"name": t.name, "path": t.path, "kind": t.kind, "docstring": t.docstring}
            for t in manifest.tools
        ],
        "skills": [
            {"name": s.name, "path": s.path, "sha256": s.sha256, "FRONTMATTER": s.frontmatter}
            for s in manifest.skills
        ],
        "schedules": [
            {"name": s.name, "path": s.path, "sha256": s.sha256, "raw": s.raw}
            for s in manifest.schedules
        ],
    }


def x_manifest_to_dict__mutmut_25(manifest: CompiledManifest) -> Dict[str, Any]:
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
        "XXschedulesXX": [
            {"name": s.name, "path": s.path, "sha256": s.sha256, "raw": s.raw}
            for s in manifest.schedules
        ],
    }


def x_manifest_to_dict__mutmut_26(manifest: CompiledManifest) -> Dict[str, Any]:
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
        "SCHEDULES": [
            {"name": s.name, "path": s.path, "sha256": s.sha256, "raw": s.raw}
            for s in manifest.schedules
        ],
    }


def x_manifest_to_dict__mutmut_27(manifest: CompiledManifest) -> Dict[str, Any]:
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
            {"XXnameXX": s.name, "path": s.path, "sha256": s.sha256, "raw": s.raw}
            for s in manifest.schedules
        ],
    }


def x_manifest_to_dict__mutmut_28(manifest: CompiledManifest) -> Dict[str, Any]:
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
            {"NAME": s.name, "path": s.path, "sha256": s.sha256, "raw": s.raw}
            for s in manifest.schedules
        ],
    }


def x_manifest_to_dict__mutmut_29(manifest: CompiledManifest) -> Dict[str, Any]:
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
            {"name": s.name, "XXpathXX": s.path, "sha256": s.sha256, "raw": s.raw}
            for s in manifest.schedules
        ],
    }


def x_manifest_to_dict__mutmut_30(manifest: CompiledManifest) -> Dict[str, Any]:
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
            {"name": s.name, "PATH": s.path, "sha256": s.sha256, "raw": s.raw}
            for s in manifest.schedules
        ],
    }


def x_manifest_to_dict__mutmut_31(manifest: CompiledManifest) -> Dict[str, Any]:
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
            {"name": s.name, "path": s.path, "XXsha256XX": s.sha256, "raw": s.raw}
            for s in manifest.schedules
        ],
    }


def x_manifest_to_dict__mutmut_32(manifest: CompiledManifest) -> Dict[str, Any]:
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
            {"name": s.name, "path": s.path, "SHA256": s.sha256, "raw": s.raw}
            for s in manifest.schedules
        ],
    }


def x_manifest_to_dict__mutmut_33(manifest: CompiledManifest) -> Dict[str, Any]:
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
            {"name": s.name, "path": s.path, "sha256": s.sha256, "XXrawXX": s.raw}
            for s in manifest.schedules
        ],
    }


def x_manifest_to_dict__mutmut_34(manifest: CompiledManifest) -> Dict[str, Any]:
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
            {"name": s.name, "path": s.path, "sha256": s.sha256, "RAW": s.raw}
            for s in manifest.schedules
        ],
    }

mutants_x_manifest_to_dict__mutmut['_mutmut_orig'] = x_manifest_to_dict__mutmut_orig # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_1'] = x_manifest_to_dict__mutmut_1 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_2'] = x_manifest_to_dict__mutmut_2 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_3'] = x_manifest_to_dict__mutmut_3 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_4'] = x_manifest_to_dict__mutmut_4 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_5'] = x_manifest_to_dict__mutmut_5 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_6'] = x_manifest_to_dict__mutmut_6 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_7'] = x_manifest_to_dict__mutmut_7 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_8'] = x_manifest_to_dict__mutmut_8 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_9'] = x_manifest_to_dict__mutmut_9 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_10'] = x_manifest_to_dict__mutmut_10 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_11'] = x_manifest_to_dict__mutmut_11 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_12'] = x_manifest_to_dict__mutmut_12 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_13'] = x_manifest_to_dict__mutmut_13 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_14'] = x_manifest_to_dict__mutmut_14 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_15'] = x_manifest_to_dict__mutmut_15 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_16'] = x_manifest_to_dict__mutmut_16 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_17'] = x_manifest_to_dict__mutmut_17 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_18'] = x_manifest_to_dict__mutmut_18 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_19'] = x_manifest_to_dict__mutmut_19 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_20'] = x_manifest_to_dict__mutmut_20 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_21'] = x_manifest_to_dict__mutmut_21 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_22'] = x_manifest_to_dict__mutmut_22 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_23'] = x_manifest_to_dict__mutmut_23 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_24'] = x_manifest_to_dict__mutmut_24 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_25'] = x_manifest_to_dict__mutmut_25 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_26'] = x_manifest_to_dict__mutmut_26 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_27'] = x_manifest_to_dict__mutmut_27 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_28'] = x_manifest_to_dict__mutmut_28 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_29'] = x_manifest_to_dict__mutmut_29 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_30'] = x_manifest_to_dict__mutmut_30 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_31'] = x_manifest_to_dict__mutmut_31 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_32'] = x_manifest_to_dict__mutmut_32 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_33'] = x_manifest_to_dict__mutmut_33 # type: ignore # mutmut generated
mutants_x_manifest_to_dict__mutmut['x_manifest_to_dict__mutmut_34'] = x_manifest_to_dict__mutmut_34 # type: ignore # mutmut generated

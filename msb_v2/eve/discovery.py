from __future__ import annotations

import ast
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


SUPPORTED_MODULE_EXTENSIONS = {".py"}
SUPPORTED_SKILL_EXTENSIONS = {".md"}

IGNORED_DIRS = {"node_modules", ".next", ".output", ".vercel", "__pycache__"}


@dataclass(frozen=True)
class ToolDef:
    name: str
    path: str
    kind: str = "python"
    docstring: Optional[str] = None


@dataclass(frozen=True)
class SkillDef:
    name: str
    path: str
    raw: str


@dataclass(frozen=True)
class ScheduleDef:
    name: str
    path: str
    raw: Any


@dataclass(frozen=True)
class DiscoveryResult:
    tools: List[ToolDef] = field(default_factory=list)
    skills: List[SkillDef] = field(default_factory=list)
    schedules: List[ScheduleDef] = field(default_factory=list)
    diagnostics: List[Dict[str, Any]] = field(default_factory=list)


def _is_ignored(entry: os.DirEntry[str]) -> bool:
    return entry.is_dir() and entry.name in IGNORED_DIRS


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _safe_name(path: Path, root: Path) -> str:
    rel = path.relative_to(root)
    stem = rel.stem
    suffix = rel.suffix.lower()
    if suffix == ".py" and stem == "__init__":
        return rel.parent.name
    return stem


def _extract_function_docstring(source: str, func_name: str) -> Optional[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            doc = ast.get_docstring(node)
            return doc.strip() if doc else None
    return None


def discover_tools(root: str | Path) -> List[ToolDef]:
    tools: List[ToolDef] = []
    root = Path(root)
    tools_dir = root / "tools"
    if not tools_dir.is_dir():
        return tools
    for entry in sorted(tools_dir.iterdir()):
        if entry.is_dir():
            continue
        if entry.suffix.lower() not in SUPPORTED_MODULE_EXTENSIONS:
            continue
        source = _read_text(entry)
        name = _safe_name(entry, tools_dir)
        doc = _extract_function_docstring(source, name)
        tools.append(ToolDef(name=name, path=str(entry), docstring=doc))
    return tools


def discover_skills(root: str | Path) -> List[SkillDef]:
    skills: List[SkillDef] = []
    root = Path(root)
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return skills
    for entry in sorted(skills_dir.iterdir()):
        if entry.is_dir():
            continue
        if entry.suffix.lower() not in SUPPORTED_SKILL_EXTENSIONS:
            continue
        raw = _read_text(entry)
        skills.append(SkillDef(name=entry.stem, path=str(entry), raw=raw))
    return skills


def discover_schedules(root: str | Path) -> List[ScheduleDef]:
    schedules: List[ScheduleDef] = []
    root = Path(root)
    schedules_dir = root / "schedules"
    if not schedules_dir.is_dir():
        return schedules
    for entry in sorted(schedules_dir.iterdir()):
        if entry.is_dir():
            continue
        if entry.suffix.lower() not in {".yaml", ".yml"}:
            continue
        import yaml

        raw = yaml.safe_load(_read_text(entry))
        schedules.append(ScheduleDef(name=entry.stem, path=str(entry), raw=raw))
    return schedules


def discover(root: str | Path) -> DiscoveryResult:
    root = Path(root)
    diagnostics: List[Dict[str, Any]] = []
    tools = discover_tools(root)
    skills = discover_skills(root)
    schedules = discover_schedules(root)
    return DiscoveryResult(tools=tools, skills=skills, schedules=schedules, diagnostics=diagnostics)

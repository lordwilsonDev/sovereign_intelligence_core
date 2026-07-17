from __future__ import annotations

import ast
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


SUPPORTED_MODULE_EXTENSIONS = {".py"}
SUPPORTED_SKILL_EXTENSIONS = {".md"}

IGNORED_DIRS = {"node_modules", ".next", ".output", ".vercel", "__pycache__"}


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


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
mutants_x__is_ignored__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_ignored__mutmut)
def _is_ignored(entry: os.DirEntry[str]) -> bool:
    return entry.is_dir() and entry.name in IGNORED_DIRS


def x__is_ignored__mutmut_orig(entry: os.DirEntry[str]) -> bool:
    return entry.is_dir() and entry.name in IGNORED_DIRS


def x__is_ignored__mutmut_1(entry: os.DirEntry[str]) -> bool:
    return entry.is_dir() or entry.name in IGNORED_DIRS


def x__is_ignored__mutmut_2(entry: os.DirEntry[str]) -> bool:
    return entry.is_dir() and entry.name not in IGNORED_DIRS

mutants_x__is_ignored__mutmut['_mutmut_orig'] = x__is_ignored__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_ignored__mutmut['x__is_ignored__mutmut_1'] = x__is_ignored__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_ignored__mutmut['x__is_ignored__mutmut_2'] = x__is_ignored__mutmut_2 # type: ignore # mutmut generated
mutants_x__read_text__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__read_text__mutmut)
def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def x__read_text__mutmut_orig(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def x__read_text__mutmut_1(path: Path) -> str:
    return path.read_text(encoding=None)


def x__read_text__mutmut_2(path: Path) -> str:
    return path.read_text(encoding="XXutf-8XX")


def x__read_text__mutmut_3(path: Path) -> str:
    return path.read_text(encoding="UTF-8")

mutants_x__read_text__mutmut['_mutmut_orig'] = x__read_text__mutmut_orig # type: ignore # mutmut generated
mutants_x__read_text__mutmut['x__read_text__mutmut_1'] = x__read_text__mutmut_1 # type: ignore # mutmut generated
mutants_x__read_text__mutmut['x__read_text__mutmut_2'] = x__read_text__mutmut_2 # type: ignore # mutmut generated
mutants_x__read_text__mutmut['x__read_text__mutmut_3'] = x__read_text__mutmut_3 # type: ignore # mutmut generated
mutants_x__safe_name__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__safe_name__mutmut)
def _safe_name(path: Path, root: Path) -> str:
    rel = path.relative_to(root)
    stem = rel.stem
    suffix = rel.suffix.lower()
    if suffix == ".py" and stem == "__init__":
        return rel.parent.name
    return stem


def x__safe_name__mutmut_orig(path: Path, root: Path) -> str:
    rel = path.relative_to(root)
    stem = rel.stem
    suffix = rel.suffix.lower()
    if suffix == ".py" and stem == "__init__":
        return rel.parent.name
    return stem


def x__safe_name__mutmut_1(path: Path, root: Path) -> str:
    rel = None
    stem = rel.stem
    suffix = rel.suffix.lower()
    if suffix == ".py" and stem == "__init__":
        return rel.parent.name
    return stem


def x__safe_name__mutmut_2(path: Path, root: Path) -> str:
    rel = path.relative_to(None)
    stem = rel.stem
    suffix = rel.suffix.lower()
    if suffix == ".py" and stem == "__init__":
        return rel.parent.name
    return stem


def x__safe_name__mutmut_3(path: Path, root: Path) -> str:
    rel = path.relative_to(root)
    stem = None
    suffix = rel.suffix.lower()
    if suffix == ".py" and stem == "__init__":
        return rel.parent.name
    return stem


def x__safe_name__mutmut_4(path: Path, root: Path) -> str:
    rel = path.relative_to(root)
    stem = rel.stem
    suffix = None
    if suffix == ".py" and stem == "__init__":
        return rel.parent.name
    return stem


def x__safe_name__mutmut_5(path: Path, root: Path) -> str:
    rel = path.relative_to(root)
    stem = rel.stem
    suffix = rel.suffix.upper()
    if suffix == ".py" and stem == "__init__":
        return rel.parent.name
    return stem


def x__safe_name__mutmut_6(path: Path, root: Path) -> str:
    rel = path.relative_to(root)
    stem = rel.stem
    suffix = rel.suffix.lower()
    if suffix == ".py" or stem == "__init__":
        return rel.parent.name
    return stem


def x__safe_name__mutmut_7(path: Path, root: Path) -> str:
    rel = path.relative_to(root)
    stem = rel.stem
    suffix = rel.suffix.lower()
    if suffix != ".py" and stem == "__init__":
        return rel.parent.name
    return stem


def x__safe_name__mutmut_8(path: Path, root: Path) -> str:
    rel = path.relative_to(root)
    stem = rel.stem
    suffix = rel.suffix.lower()
    if suffix == "XX.pyXX" and stem == "__init__":
        return rel.parent.name
    return stem


def x__safe_name__mutmut_9(path: Path, root: Path) -> str:
    rel = path.relative_to(root)
    stem = rel.stem
    suffix = rel.suffix.lower()
    if suffix == ".PY" and stem == "__init__":
        return rel.parent.name
    return stem


def x__safe_name__mutmut_10(path: Path, root: Path) -> str:
    rel = path.relative_to(root)
    stem = rel.stem
    suffix = rel.suffix.lower()
    if suffix == ".py" and stem != "__init__":
        return rel.parent.name
    return stem


def x__safe_name__mutmut_11(path: Path, root: Path) -> str:
    rel = path.relative_to(root)
    stem = rel.stem
    suffix = rel.suffix.lower()
    if suffix == ".py" and stem == "XX__init__XX":
        return rel.parent.name
    return stem


def x__safe_name__mutmut_12(path: Path, root: Path) -> str:
    rel = path.relative_to(root)
    stem = rel.stem
    suffix = rel.suffix.lower()
    if suffix == ".py" and stem == "__INIT__":
        return rel.parent.name
    return stem

mutants_x__safe_name__mutmut['_mutmut_orig'] = x__safe_name__mutmut_orig # type: ignore # mutmut generated
mutants_x__safe_name__mutmut['x__safe_name__mutmut_1'] = x__safe_name__mutmut_1 # type: ignore # mutmut generated
mutants_x__safe_name__mutmut['x__safe_name__mutmut_2'] = x__safe_name__mutmut_2 # type: ignore # mutmut generated
mutants_x__safe_name__mutmut['x__safe_name__mutmut_3'] = x__safe_name__mutmut_3 # type: ignore # mutmut generated
mutants_x__safe_name__mutmut['x__safe_name__mutmut_4'] = x__safe_name__mutmut_4 # type: ignore # mutmut generated
mutants_x__safe_name__mutmut['x__safe_name__mutmut_5'] = x__safe_name__mutmut_5 # type: ignore # mutmut generated
mutants_x__safe_name__mutmut['x__safe_name__mutmut_6'] = x__safe_name__mutmut_6 # type: ignore # mutmut generated
mutants_x__safe_name__mutmut['x__safe_name__mutmut_7'] = x__safe_name__mutmut_7 # type: ignore # mutmut generated
mutants_x__safe_name__mutmut['x__safe_name__mutmut_8'] = x__safe_name__mutmut_8 # type: ignore # mutmut generated
mutants_x__safe_name__mutmut['x__safe_name__mutmut_9'] = x__safe_name__mutmut_9 # type: ignore # mutmut generated
mutants_x__safe_name__mutmut['x__safe_name__mutmut_10'] = x__safe_name__mutmut_10 # type: ignore # mutmut generated
mutants_x__safe_name__mutmut['x__safe_name__mutmut_11'] = x__safe_name__mutmut_11 # type: ignore # mutmut generated
mutants_x__safe_name__mutmut['x__safe_name__mutmut_12'] = x__safe_name__mutmut_12 # type: ignore # mutmut generated
mutants_x__extract_function_docstring__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__extract_function_docstring__mutmut)
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


def x__extract_function_docstring__mutmut_orig(source: str, func_name: str) -> Optional[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            doc = ast.get_docstring(node)
            return doc.strip() if doc else None
    return None


def x__extract_function_docstring__mutmut_1(source: str, func_name: str) -> Optional[str]:
    try:
        tree = None
    except SyntaxError:
        return None
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            doc = ast.get_docstring(node)
            return doc.strip() if doc else None
    return None


def x__extract_function_docstring__mutmut_2(source: str, func_name: str) -> Optional[str]:
    try:
        tree = ast.parse(None)
    except SyntaxError:
        return None
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            doc = ast.get_docstring(node)
            return doc.strip() if doc else None
    return None


def x__extract_function_docstring__mutmut_3(source: str, func_name: str) -> Optional[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    for node in ast.iter_child_nodes(None):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            doc = ast.get_docstring(node)
            return doc.strip() if doc else None
    return None


def x__extract_function_docstring__mutmut_4(source: str, func_name: str) -> Optional[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef) or node.name == func_name:
            doc = ast.get_docstring(node)
            return doc.strip() if doc else None
    return None


def x__extract_function_docstring__mutmut_5(source: str, func_name: str) -> Optional[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef) and node.name != func_name:
            doc = ast.get_docstring(node)
            return doc.strip() if doc else None
    return None


def x__extract_function_docstring__mutmut_6(source: str, func_name: str) -> Optional[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            doc = None
            return doc.strip() if doc else None
    return None


def x__extract_function_docstring__mutmut_7(source: str, func_name: str) -> Optional[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            doc = ast.get_docstring(None)
            return doc.strip() if doc else None
    return None

mutants_x__extract_function_docstring__mutmut['_mutmut_orig'] = x__extract_function_docstring__mutmut_orig # type: ignore # mutmut generated
mutants_x__extract_function_docstring__mutmut['x__extract_function_docstring__mutmut_1'] = x__extract_function_docstring__mutmut_1 # type: ignore # mutmut generated
mutants_x__extract_function_docstring__mutmut['x__extract_function_docstring__mutmut_2'] = x__extract_function_docstring__mutmut_2 # type: ignore # mutmut generated
mutants_x__extract_function_docstring__mutmut['x__extract_function_docstring__mutmut_3'] = x__extract_function_docstring__mutmut_3 # type: ignore # mutmut generated
mutants_x__extract_function_docstring__mutmut['x__extract_function_docstring__mutmut_4'] = x__extract_function_docstring__mutmut_4 # type: ignore # mutmut generated
mutants_x__extract_function_docstring__mutmut['x__extract_function_docstring__mutmut_5'] = x__extract_function_docstring__mutmut_5 # type: ignore # mutmut generated
mutants_x__extract_function_docstring__mutmut['x__extract_function_docstring__mutmut_6'] = x__extract_function_docstring__mutmut_6 # type: ignore # mutmut generated
mutants_x__extract_function_docstring__mutmut['x__extract_function_docstring__mutmut_7'] = x__extract_function_docstring__mutmut_7 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_discover_tools__mutmut)
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


def x_discover_tools__mutmut_orig(root: str | Path) -> List[ToolDef]:
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


def x_discover_tools__mutmut_1(root: str | Path) -> List[ToolDef]:
    tools: List[ToolDef] = None
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


def x_discover_tools__mutmut_2(root: str | Path) -> List[ToolDef]:
    tools: List[ToolDef] = []
    root = None
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


def x_discover_tools__mutmut_3(root: str | Path) -> List[ToolDef]:
    tools: List[ToolDef] = []
    root = Path(None)
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


def x_discover_tools__mutmut_4(root: str | Path) -> List[ToolDef]:
    tools: List[ToolDef] = []
    root = Path(root)
    tools_dir = None
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


def x_discover_tools__mutmut_5(root: str | Path) -> List[ToolDef]:
    tools: List[ToolDef] = []
    root = Path(root)
    tools_dir = root * "tools"
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


def x_discover_tools__mutmut_6(root: str | Path) -> List[ToolDef]:
    tools: List[ToolDef] = []
    root = Path(root)
    tools_dir = root / "XXtoolsXX"
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


def x_discover_tools__mutmut_7(root: str | Path) -> List[ToolDef]:
    tools: List[ToolDef] = []
    root = Path(root)
    tools_dir = root / "TOOLS"
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


def x_discover_tools__mutmut_8(root: str | Path) -> List[ToolDef]:
    tools: List[ToolDef] = []
    root = Path(root)
    tools_dir = root / "tools"
    if tools_dir.is_dir():
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


def x_discover_tools__mutmut_9(root: str | Path) -> List[ToolDef]:
    tools: List[ToolDef] = []
    root = Path(root)
    tools_dir = root / "tools"
    if not tools_dir.is_dir():
        return tools
    for entry in sorted(None):
        if entry.is_dir():
            continue
        if entry.suffix.lower() not in SUPPORTED_MODULE_EXTENSIONS:
            continue
        source = _read_text(entry)
        name = _safe_name(entry, tools_dir)
        doc = _extract_function_docstring(source, name)
        tools.append(ToolDef(name=name, path=str(entry), docstring=doc))
    return tools


def x_discover_tools__mutmut_10(root: str | Path) -> List[ToolDef]:
    tools: List[ToolDef] = []
    root = Path(root)
    tools_dir = root / "tools"
    if not tools_dir.is_dir():
        return tools
    for entry in sorted(tools_dir.iterdir()):
        if entry.is_dir():
            break
        if entry.suffix.lower() not in SUPPORTED_MODULE_EXTENSIONS:
            continue
        source = _read_text(entry)
        name = _safe_name(entry, tools_dir)
        doc = _extract_function_docstring(source, name)
        tools.append(ToolDef(name=name, path=str(entry), docstring=doc))
    return tools


def x_discover_tools__mutmut_11(root: str | Path) -> List[ToolDef]:
    tools: List[ToolDef] = []
    root = Path(root)
    tools_dir = root / "tools"
    if not tools_dir.is_dir():
        return tools
    for entry in sorted(tools_dir.iterdir()):
        if entry.is_dir():
            continue
        if entry.suffix.upper() not in SUPPORTED_MODULE_EXTENSIONS:
            continue
        source = _read_text(entry)
        name = _safe_name(entry, tools_dir)
        doc = _extract_function_docstring(source, name)
        tools.append(ToolDef(name=name, path=str(entry), docstring=doc))
    return tools


def x_discover_tools__mutmut_12(root: str | Path) -> List[ToolDef]:
    tools: List[ToolDef] = []
    root = Path(root)
    tools_dir = root / "tools"
    if not tools_dir.is_dir():
        return tools
    for entry in sorted(tools_dir.iterdir()):
        if entry.is_dir():
            continue
        if entry.suffix.lower() in SUPPORTED_MODULE_EXTENSIONS:
            continue
        source = _read_text(entry)
        name = _safe_name(entry, tools_dir)
        doc = _extract_function_docstring(source, name)
        tools.append(ToolDef(name=name, path=str(entry), docstring=doc))
    return tools


def x_discover_tools__mutmut_13(root: str | Path) -> List[ToolDef]:
    tools: List[ToolDef] = []
    root = Path(root)
    tools_dir = root / "tools"
    if not tools_dir.is_dir():
        return tools
    for entry in sorted(tools_dir.iterdir()):
        if entry.is_dir():
            continue
        if entry.suffix.lower() not in SUPPORTED_MODULE_EXTENSIONS:
            break
        source = _read_text(entry)
        name = _safe_name(entry, tools_dir)
        doc = _extract_function_docstring(source, name)
        tools.append(ToolDef(name=name, path=str(entry), docstring=doc))
    return tools


def x_discover_tools__mutmut_14(root: str | Path) -> List[ToolDef]:
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
        source = None
        name = _safe_name(entry, tools_dir)
        doc = _extract_function_docstring(source, name)
        tools.append(ToolDef(name=name, path=str(entry), docstring=doc))
    return tools


def x_discover_tools__mutmut_15(root: str | Path) -> List[ToolDef]:
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
        source = _read_text(None)
        name = _safe_name(entry, tools_dir)
        doc = _extract_function_docstring(source, name)
        tools.append(ToolDef(name=name, path=str(entry), docstring=doc))
    return tools


def x_discover_tools__mutmut_16(root: str | Path) -> List[ToolDef]:
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
        name = None
        doc = _extract_function_docstring(source, name)
        tools.append(ToolDef(name=name, path=str(entry), docstring=doc))
    return tools


def x_discover_tools__mutmut_17(root: str | Path) -> List[ToolDef]:
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
        name = _safe_name(None, tools_dir)
        doc = _extract_function_docstring(source, name)
        tools.append(ToolDef(name=name, path=str(entry), docstring=doc))
    return tools


def x_discover_tools__mutmut_18(root: str | Path) -> List[ToolDef]:
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
        name = _safe_name(entry, None)
        doc = _extract_function_docstring(source, name)
        tools.append(ToolDef(name=name, path=str(entry), docstring=doc))
    return tools


def x_discover_tools__mutmut_19(root: str | Path) -> List[ToolDef]:
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
        name = _safe_name(tools_dir)
        doc = _extract_function_docstring(source, name)
        tools.append(ToolDef(name=name, path=str(entry), docstring=doc))
    return tools


def x_discover_tools__mutmut_20(root: str | Path) -> List[ToolDef]:
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
        name = _safe_name(entry, )
        doc = _extract_function_docstring(source, name)
        tools.append(ToolDef(name=name, path=str(entry), docstring=doc))
    return tools


def x_discover_tools__mutmut_21(root: str | Path) -> List[ToolDef]:
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
        doc = None
        tools.append(ToolDef(name=name, path=str(entry), docstring=doc))
    return tools


def x_discover_tools__mutmut_22(root: str | Path) -> List[ToolDef]:
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
        doc = _extract_function_docstring(None, name)
        tools.append(ToolDef(name=name, path=str(entry), docstring=doc))
    return tools


def x_discover_tools__mutmut_23(root: str | Path) -> List[ToolDef]:
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
        doc = _extract_function_docstring(source, None)
        tools.append(ToolDef(name=name, path=str(entry), docstring=doc))
    return tools


def x_discover_tools__mutmut_24(root: str | Path) -> List[ToolDef]:
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
        doc = _extract_function_docstring(name)
        tools.append(ToolDef(name=name, path=str(entry), docstring=doc))
    return tools


def x_discover_tools__mutmut_25(root: str | Path) -> List[ToolDef]:
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
        doc = _extract_function_docstring(source, )
        tools.append(ToolDef(name=name, path=str(entry), docstring=doc))
    return tools


def x_discover_tools__mutmut_26(root: str | Path) -> List[ToolDef]:
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
        tools.append(None)
    return tools


def x_discover_tools__mutmut_27(root: str | Path) -> List[ToolDef]:
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
        tools.append(ToolDef(name=None, path=str(entry), docstring=doc))
    return tools


def x_discover_tools__mutmut_28(root: str | Path) -> List[ToolDef]:
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
        tools.append(ToolDef(name=name, path=None, docstring=doc))
    return tools


def x_discover_tools__mutmut_29(root: str | Path) -> List[ToolDef]:
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
        tools.append(ToolDef(name=name, path=str(entry), docstring=None))
    return tools


def x_discover_tools__mutmut_30(root: str | Path) -> List[ToolDef]:
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
        tools.append(ToolDef(path=str(entry), docstring=doc))
    return tools


def x_discover_tools__mutmut_31(root: str | Path) -> List[ToolDef]:
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
        tools.append(ToolDef(name=name, docstring=doc))
    return tools


def x_discover_tools__mutmut_32(root: str | Path) -> List[ToolDef]:
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
        tools.append(ToolDef(name=name, path=str(entry), ))
    return tools


def x_discover_tools__mutmut_33(root: str | Path) -> List[ToolDef]:
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
        tools.append(ToolDef(name=name, path=str(None), docstring=doc))
    return tools

mutants_x_discover_tools__mutmut['_mutmut_orig'] = x_discover_tools__mutmut_orig # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_1'] = x_discover_tools__mutmut_1 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_2'] = x_discover_tools__mutmut_2 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_3'] = x_discover_tools__mutmut_3 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_4'] = x_discover_tools__mutmut_4 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_5'] = x_discover_tools__mutmut_5 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_6'] = x_discover_tools__mutmut_6 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_7'] = x_discover_tools__mutmut_7 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_8'] = x_discover_tools__mutmut_8 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_9'] = x_discover_tools__mutmut_9 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_10'] = x_discover_tools__mutmut_10 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_11'] = x_discover_tools__mutmut_11 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_12'] = x_discover_tools__mutmut_12 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_13'] = x_discover_tools__mutmut_13 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_14'] = x_discover_tools__mutmut_14 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_15'] = x_discover_tools__mutmut_15 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_16'] = x_discover_tools__mutmut_16 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_17'] = x_discover_tools__mutmut_17 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_18'] = x_discover_tools__mutmut_18 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_19'] = x_discover_tools__mutmut_19 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_20'] = x_discover_tools__mutmut_20 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_21'] = x_discover_tools__mutmut_21 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_22'] = x_discover_tools__mutmut_22 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_23'] = x_discover_tools__mutmut_23 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_24'] = x_discover_tools__mutmut_24 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_25'] = x_discover_tools__mutmut_25 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_26'] = x_discover_tools__mutmut_26 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_27'] = x_discover_tools__mutmut_27 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_28'] = x_discover_tools__mutmut_28 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_29'] = x_discover_tools__mutmut_29 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_30'] = x_discover_tools__mutmut_30 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_31'] = x_discover_tools__mutmut_31 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_32'] = x_discover_tools__mutmut_32 # type: ignore # mutmut generated
mutants_x_discover_tools__mutmut['x_discover_tools__mutmut_33'] = x_discover_tools__mutmut_33 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_discover_skills__mutmut)
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


def x_discover_skills__mutmut_orig(root: str | Path) -> List[SkillDef]:
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


def x_discover_skills__mutmut_1(root: str | Path) -> List[SkillDef]:
    skills: List[SkillDef] = None
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


def x_discover_skills__mutmut_2(root: str | Path) -> List[SkillDef]:
    skills: List[SkillDef] = []
    root = None
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


def x_discover_skills__mutmut_3(root: str | Path) -> List[SkillDef]:
    skills: List[SkillDef] = []
    root = Path(None)
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


def x_discover_skills__mutmut_4(root: str | Path) -> List[SkillDef]:
    skills: List[SkillDef] = []
    root = Path(root)
    skills_dir = None
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


def x_discover_skills__mutmut_5(root: str | Path) -> List[SkillDef]:
    skills: List[SkillDef] = []
    root = Path(root)
    skills_dir = root * "skills"
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


def x_discover_skills__mutmut_6(root: str | Path) -> List[SkillDef]:
    skills: List[SkillDef] = []
    root = Path(root)
    skills_dir = root / "XXskillsXX"
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


def x_discover_skills__mutmut_7(root: str | Path) -> List[SkillDef]:
    skills: List[SkillDef] = []
    root = Path(root)
    skills_dir = root / "SKILLS"
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


def x_discover_skills__mutmut_8(root: str | Path) -> List[SkillDef]:
    skills: List[SkillDef] = []
    root = Path(root)
    skills_dir = root / "skills"
    if skills_dir.is_dir():
        return skills
    for entry in sorted(skills_dir.iterdir()):
        if entry.is_dir():
            continue
        if entry.suffix.lower() not in SUPPORTED_SKILL_EXTENSIONS:
            continue
        raw = _read_text(entry)
        skills.append(SkillDef(name=entry.stem, path=str(entry), raw=raw))
    return skills


def x_discover_skills__mutmut_9(root: str | Path) -> List[SkillDef]:
    skills: List[SkillDef] = []
    root = Path(root)
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return skills
    for entry in sorted(None):
        if entry.is_dir():
            continue
        if entry.suffix.lower() not in SUPPORTED_SKILL_EXTENSIONS:
            continue
        raw = _read_text(entry)
        skills.append(SkillDef(name=entry.stem, path=str(entry), raw=raw))
    return skills


def x_discover_skills__mutmut_10(root: str | Path) -> List[SkillDef]:
    skills: List[SkillDef] = []
    root = Path(root)
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return skills
    for entry in sorted(skills_dir.iterdir()):
        if entry.is_dir():
            break
        if entry.suffix.lower() not in SUPPORTED_SKILL_EXTENSIONS:
            continue
        raw = _read_text(entry)
        skills.append(SkillDef(name=entry.stem, path=str(entry), raw=raw))
    return skills


def x_discover_skills__mutmut_11(root: str | Path) -> List[SkillDef]:
    skills: List[SkillDef] = []
    root = Path(root)
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return skills
    for entry in sorted(skills_dir.iterdir()):
        if entry.is_dir():
            continue
        if entry.suffix.upper() not in SUPPORTED_SKILL_EXTENSIONS:
            continue
        raw = _read_text(entry)
        skills.append(SkillDef(name=entry.stem, path=str(entry), raw=raw))
    return skills


def x_discover_skills__mutmut_12(root: str | Path) -> List[SkillDef]:
    skills: List[SkillDef] = []
    root = Path(root)
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return skills
    for entry in sorted(skills_dir.iterdir()):
        if entry.is_dir():
            continue
        if entry.suffix.lower() in SUPPORTED_SKILL_EXTENSIONS:
            continue
        raw = _read_text(entry)
        skills.append(SkillDef(name=entry.stem, path=str(entry), raw=raw))
    return skills


def x_discover_skills__mutmut_13(root: str | Path) -> List[SkillDef]:
    skills: List[SkillDef] = []
    root = Path(root)
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return skills
    for entry in sorted(skills_dir.iterdir()):
        if entry.is_dir():
            continue
        if entry.suffix.lower() not in SUPPORTED_SKILL_EXTENSIONS:
            break
        raw = _read_text(entry)
        skills.append(SkillDef(name=entry.stem, path=str(entry), raw=raw))
    return skills


def x_discover_skills__mutmut_14(root: str | Path) -> List[SkillDef]:
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
        raw = None
        skills.append(SkillDef(name=entry.stem, path=str(entry), raw=raw))
    return skills


def x_discover_skills__mutmut_15(root: str | Path) -> List[SkillDef]:
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
        raw = _read_text(None)
        skills.append(SkillDef(name=entry.stem, path=str(entry), raw=raw))
    return skills


def x_discover_skills__mutmut_16(root: str | Path) -> List[SkillDef]:
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
        skills.append(None)
    return skills


def x_discover_skills__mutmut_17(root: str | Path) -> List[SkillDef]:
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
        skills.append(SkillDef(name=None, path=str(entry), raw=raw))
    return skills


def x_discover_skills__mutmut_18(root: str | Path) -> List[SkillDef]:
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
        skills.append(SkillDef(name=entry.stem, path=None, raw=raw))
    return skills


def x_discover_skills__mutmut_19(root: str | Path) -> List[SkillDef]:
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
        skills.append(SkillDef(name=entry.stem, path=str(entry), raw=None))
    return skills


def x_discover_skills__mutmut_20(root: str | Path) -> List[SkillDef]:
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
        skills.append(SkillDef(path=str(entry), raw=raw))
    return skills


def x_discover_skills__mutmut_21(root: str | Path) -> List[SkillDef]:
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
        skills.append(SkillDef(name=entry.stem, raw=raw))
    return skills


def x_discover_skills__mutmut_22(root: str | Path) -> List[SkillDef]:
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
        skills.append(SkillDef(name=entry.stem, path=str(entry), ))
    return skills


def x_discover_skills__mutmut_23(root: str | Path) -> List[SkillDef]:
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
        skills.append(SkillDef(name=entry.stem, path=str(None), raw=raw))
    return skills

mutants_x_discover_skills__mutmut['_mutmut_orig'] = x_discover_skills__mutmut_orig # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_1'] = x_discover_skills__mutmut_1 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_2'] = x_discover_skills__mutmut_2 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_3'] = x_discover_skills__mutmut_3 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_4'] = x_discover_skills__mutmut_4 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_5'] = x_discover_skills__mutmut_5 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_6'] = x_discover_skills__mutmut_6 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_7'] = x_discover_skills__mutmut_7 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_8'] = x_discover_skills__mutmut_8 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_9'] = x_discover_skills__mutmut_9 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_10'] = x_discover_skills__mutmut_10 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_11'] = x_discover_skills__mutmut_11 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_12'] = x_discover_skills__mutmut_12 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_13'] = x_discover_skills__mutmut_13 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_14'] = x_discover_skills__mutmut_14 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_15'] = x_discover_skills__mutmut_15 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_16'] = x_discover_skills__mutmut_16 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_17'] = x_discover_skills__mutmut_17 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_18'] = x_discover_skills__mutmut_18 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_19'] = x_discover_skills__mutmut_19 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_20'] = x_discover_skills__mutmut_20 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_21'] = x_discover_skills__mutmut_21 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_22'] = x_discover_skills__mutmut_22 # type: ignore # mutmut generated
mutants_x_discover_skills__mutmut['x_discover_skills__mutmut_23'] = x_discover_skills__mutmut_23 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_discover_schedules__mutmut)
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


def x_discover_schedules__mutmut_orig(root: str | Path) -> List[ScheduleDef]:
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


def x_discover_schedules__mutmut_1(root: str | Path) -> List[ScheduleDef]:
    schedules: List[ScheduleDef] = None
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


def x_discover_schedules__mutmut_2(root: str | Path) -> List[ScheduleDef]:
    schedules: List[ScheduleDef] = []
    root = None
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


def x_discover_schedules__mutmut_3(root: str | Path) -> List[ScheduleDef]:
    schedules: List[ScheduleDef] = []
    root = Path(None)
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


def x_discover_schedules__mutmut_4(root: str | Path) -> List[ScheduleDef]:
    schedules: List[ScheduleDef] = []
    root = Path(root)
    schedules_dir = None
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


def x_discover_schedules__mutmut_5(root: str | Path) -> List[ScheduleDef]:
    schedules: List[ScheduleDef] = []
    root = Path(root)
    schedules_dir = root * "schedules"
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


def x_discover_schedules__mutmut_6(root: str | Path) -> List[ScheduleDef]:
    schedules: List[ScheduleDef] = []
    root = Path(root)
    schedules_dir = root / "XXschedulesXX"
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


def x_discover_schedules__mutmut_7(root: str | Path) -> List[ScheduleDef]:
    schedules: List[ScheduleDef] = []
    root = Path(root)
    schedules_dir = root / "SCHEDULES"
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


def x_discover_schedules__mutmut_8(root: str | Path) -> List[ScheduleDef]:
    schedules: List[ScheduleDef] = []
    root = Path(root)
    schedules_dir = root / "schedules"
    if schedules_dir.is_dir():
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


def x_discover_schedules__mutmut_9(root: str | Path) -> List[ScheduleDef]:
    schedules: List[ScheduleDef] = []
    root = Path(root)
    schedules_dir = root / "schedules"
    if not schedules_dir.is_dir():
        return schedules
    for entry in sorted(None):
        if entry.is_dir():
            continue
        if entry.suffix.lower() not in {".yaml", ".yml"}:
            continue
        import yaml

        raw = yaml.safe_load(_read_text(entry))
        schedules.append(ScheduleDef(name=entry.stem, path=str(entry), raw=raw))
    return schedules


def x_discover_schedules__mutmut_10(root: str | Path) -> List[ScheduleDef]:
    schedules: List[ScheduleDef] = []
    root = Path(root)
    schedules_dir = root / "schedules"
    if not schedules_dir.is_dir():
        return schedules
    for entry in sorted(schedules_dir.iterdir()):
        if entry.is_dir():
            break
        if entry.suffix.lower() not in {".yaml", ".yml"}:
            continue
        import yaml

        raw = yaml.safe_load(_read_text(entry))
        schedules.append(ScheduleDef(name=entry.stem, path=str(entry), raw=raw))
    return schedules


def x_discover_schedules__mutmut_11(root: str | Path) -> List[ScheduleDef]:
    schedules: List[ScheduleDef] = []
    root = Path(root)
    schedules_dir = root / "schedules"
    if not schedules_dir.is_dir():
        return schedules
    for entry in sorted(schedules_dir.iterdir()):
        if entry.is_dir():
            continue
        if entry.suffix.upper() not in {".yaml", ".yml"}:
            continue
        import yaml

        raw = yaml.safe_load(_read_text(entry))
        schedules.append(ScheduleDef(name=entry.stem, path=str(entry), raw=raw))
    return schedules


def x_discover_schedules__mutmut_12(root: str | Path) -> List[ScheduleDef]:
    schedules: List[ScheduleDef] = []
    root = Path(root)
    schedules_dir = root / "schedules"
    if not schedules_dir.is_dir():
        return schedules
    for entry in sorted(schedules_dir.iterdir()):
        if entry.is_dir():
            continue
        if entry.suffix.lower() in {".yaml", ".yml"}:
            continue
        import yaml

        raw = yaml.safe_load(_read_text(entry))
        schedules.append(ScheduleDef(name=entry.stem, path=str(entry), raw=raw))
    return schedules


def x_discover_schedules__mutmut_13(root: str | Path) -> List[ScheduleDef]:
    schedules: List[ScheduleDef] = []
    root = Path(root)
    schedules_dir = root / "schedules"
    if not schedules_dir.is_dir():
        return schedules
    for entry in sorted(schedules_dir.iterdir()):
        if entry.is_dir():
            continue
        if entry.suffix.lower() not in {"XX.yamlXX", ".yml"}:
            continue
        import yaml

        raw = yaml.safe_load(_read_text(entry))
        schedules.append(ScheduleDef(name=entry.stem, path=str(entry), raw=raw))
    return schedules


def x_discover_schedules__mutmut_14(root: str | Path) -> List[ScheduleDef]:
    schedules: List[ScheduleDef] = []
    root = Path(root)
    schedules_dir = root / "schedules"
    if not schedules_dir.is_dir():
        return schedules
    for entry in sorted(schedules_dir.iterdir()):
        if entry.is_dir():
            continue
        if entry.suffix.lower() not in {".YAML", ".yml"}:
            continue
        import yaml

        raw = yaml.safe_load(_read_text(entry))
        schedules.append(ScheduleDef(name=entry.stem, path=str(entry), raw=raw))
    return schedules


def x_discover_schedules__mutmut_15(root: str | Path) -> List[ScheduleDef]:
    schedules: List[ScheduleDef] = []
    root = Path(root)
    schedules_dir = root / "schedules"
    if not schedules_dir.is_dir():
        return schedules
    for entry in sorted(schedules_dir.iterdir()):
        if entry.is_dir():
            continue
        if entry.suffix.lower() not in {".yaml", "XX.ymlXX"}:
            continue
        import yaml

        raw = yaml.safe_load(_read_text(entry))
        schedules.append(ScheduleDef(name=entry.stem, path=str(entry), raw=raw))
    return schedules


def x_discover_schedules__mutmut_16(root: str | Path) -> List[ScheduleDef]:
    schedules: List[ScheduleDef] = []
    root = Path(root)
    schedules_dir = root / "schedules"
    if not schedules_dir.is_dir():
        return schedules
    for entry in sorted(schedules_dir.iterdir()):
        if entry.is_dir():
            continue
        if entry.suffix.lower() not in {".yaml", ".YML"}:
            continue
        import yaml

        raw = yaml.safe_load(_read_text(entry))
        schedules.append(ScheduleDef(name=entry.stem, path=str(entry), raw=raw))
    return schedules


def x_discover_schedules__mutmut_17(root: str | Path) -> List[ScheduleDef]:
    schedules: List[ScheduleDef] = []
    root = Path(root)
    schedules_dir = root / "schedules"
    if not schedules_dir.is_dir():
        return schedules
    for entry in sorted(schedules_dir.iterdir()):
        if entry.is_dir():
            continue
        if entry.suffix.lower() not in {".yaml", ".yml"}:
            break
        import yaml

        raw = yaml.safe_load(_read_text(entry))
        schedules.append(ScheduleDef(name=entry.stem, path=str(entry), raw=raw))
    return schedules


def x_discover_schedules__mutmut_18(root: str | Path) -> List[ScheduleDef]:
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

        raw = None
        schedules.append(ScheduleDef(name=entry.stem, path=str(entry), raw=raw))
    return schedules


def x_discover_schedules__mutmut_19(root: str | Path) -> List[ScheduleDef]:
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

        raw = yaml.safe_load(None)
        schedules.append(ScheduleDef(name=entry.stem, path=str(entry), raw=raw))
    return schedules


def x_discover_schedules__mutmut_20(root: str | Path) -> List[ScheduleDef]:
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

        raw = yaml.safe_load(_read_text(None))
        schedules.append(ScheduleDef(name=entry.stem, path=str(entry), raw=raw))
    return schedules


def x_discover_schedules__mutmut_21(root: str | Path) -> List[ScheduleDef]:
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
        schedules.append(None)
    return schedules


def x_discover_schedules__mutmut_22(root: str | Path) -> List[ScheduleDef]:
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
        schedules.append(ScheduleDef(name=None, path=str(entry), raw=raw))
    return schedules


def x_discover_schedules__mutmut_23(root: str | Path) -> List[ScheduleDef]:
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
        schedules.append(ScheduleDef(name=entry.stem, path=None, raw=raw))
    return schedules


def x_discover_schedules__mutmut_24(root: str | Path) -> List[ScheduleDef]:
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
        schedules.append(ScheduleDef(name=entry.stem, path=str(entry), raw=None))
    return schedules


def x_discover_schedules__mutmut_25(root: str | Path) -> List[ScheduleDef]:
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
        schedules.append(ScheduleDef(path=str(entry), raw=raw))
    return schedules


def x_discover_schedules__mutmut_26(root: str | Path) -> List[ScheduleDef]:
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
        schedules.append(ScheduleDef(name=entry.stem, raw=raw))
    return schedules


def x_discover_schedules__mutmut_27(root: str | Path) -> List[ScheduleDef]:
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
        schedules.append(ScheduleDef(name=entry.stem, path=str(entry), ))
    return schedules


def x_discover_schedules__mutmut_28(root: str | Path) -> List[ScheduleDef]:
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
        schedules.append(ScheduleDef(name=entry.stem, path=str(None), raw=raw))
    return schedules

mutants_x_discover_schedules__mutmut['_mutmut_orig'] = x_discover_schedules__mutmut_orig # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_1'] = x_discover_schedules__mutmut_1 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_2'] = x_discover_schedules__mutmut_2 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_3'] = x_discover_schedules__mutmut_3 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_4'] = x_discover_schedules__mutmut_4 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_5'] = x_discover_schedules__mutmut_5 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_6'] = x_discover_schedules__mutmut_6 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_7'] = x_discover_schedules__mutmut_7 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_8'] = x_discover_schedules__mutmut_8 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_9'] = x_discover_schedules__mutmut_9 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_10'] = x_discover_schedules__mutmut_10 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_11'] = x_discover_schedules__mutmut_11 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_12'] = x_discover_schedules__mutmut_12 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_13'] = x_discover_schedules__mutmut_13 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_14'] = x_discover_schedules__mutmut_14 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_15'] = x_discover_schedules__mutmut_15 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_16'] = x_discover_schedules__mutmut_16 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_17'] = x_discover_schedules__mutmut_17 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_18'] = x_discover_schedules__mutmut_18 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_19'] = x_discover_schedules__mutmut_19 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_20'] = x_discover_schedules__mutmut_20 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_21'] = x_discover_schedules__mutmut_21 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_22'] = x_discover_schedules__mutmut_22 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_23'] = x_discover_schedules__mutmut_23 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_24'] = x_discover_schedules__mutmut_24 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_25'] = x_discover_schedules__mutmut_25 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_26'] = x_discover_schedules__mutmut_26 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_27'] = x_discover_schedules__mutmut_27 # type: ignore # mutmut generated
mutants_x_discover_schedules__mutmut['x_discover_schedules__mutmut_28'] = x_discover_schedules__mutmut_28 # type: ignore # mutmut generated
mutants_x_discover__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_discover__mutmut)
def discover(root: str | Path) -> DiscoveryResult:
    root = Path(root)
    diagnostics: List[Dict[str, Any]] = []
    tools = discover_tools(root)
    skills = discover_skills(root)
    schedules = discover_schedules(root)
    return DiscoveryResult(tools=tools, skills=skills, schedules=schedules, diagnostics=diagnostics)


def x_discover__mutmut_orig(root: str | Path) -> DiscoveryResult:
    root = Path(root)
    diagnostics: List[Dict[str, Any]] = []
    tools = discover_tools(root)
    skills = discover_skills(root)
    schedules = discover_schedules(root)
    return DiscoveryResult(tools=tools, skills=skills, schedules=schedules, diagnostics=diagnostics)


def x_discover__mutmut_1(root: str | Path) -> DiscoveryResult:
    root = None
    diagnostics: List[Dict[str, Any]] = []
    tools = discover_tools(root)
    skills = discover_skills(root)
    schedules = discover_schedules(root)
    return DiscoveryResult(tools=tools, skills=skills, schedules=schedules, diagnostics=diagnostics)


def x_discover__mutmut_2(root: str | Path) -> DiscoveryResult:
    root = Path(None)
    diagnostics: List[Dict[str, Any]] = []
    tools = discover_tools(root)
    skills = discover_skills(root)
    schedules = discover_schedules(root)
    return DiscoveryResult(tools=tools, skills=skills, schedules=schedules, diagnostics=diagnostics)


def x_discover__mutmut_3(root: str | Path) -> DiscoveryResult:
    root = Path(root)
    diagnostics: List[Dict[str, Any]] = None
    tools = discover_tools(root)
    skills = discover_skills(root)
    schedules = discover_schedules(root)
    return DiscoveryResult(tools=tools, skills=skills, schedules=schedules, diagnostics=diagnostics)


def x_discover__mutmut_4(root: str | Path) -> DiscoveryResult:
    root = Path(root)
    diagnostics: List[Dict[str, Any]] = []
    tools = None
    skills = discover_skills(root)
    schedules = discover_schedules(root)
    return DiscoveryResult(tools=tools, skills=skills, schedules=schedules, diagnostics=diagnostics)


def x_discover__mutmut_5(root: str | Path) -> DiscoveryResult:
    root = Path(root)
    diagnostics: List[Dict[str, Any]] = []
    tools = discover_tools(None)
    skills = discover_skills(root)
    schedules = discover_schedules(root)
    return DiscoveryResult(tools=tools, skills=skills, schedules=schedules, diagnostics=diagnostics)


def x_discover__mutmut_6(root: str | Path) -> DiscoveryResult:
    root = Path(root)
    diagnostics: List[Dict[str, Any]] = []
    tools = discover_tools(root)
    skills = None
    schedules = discover_schedules(root)
    return DiscoveryResult(tools=tools, skills=skills, schedules=schedules, diagnostics=diagnostics)


def x_discover__mutmut_7(root: str | Path) -> DiscoveryResult:
    root = Path(root)
    diagnostics: List[Dict[str, Any]] = []
    tools = discover_tools(root)
    skills = discover_skills(None)
    schedules = discover_schedules(root)
    return DiscoveryResult(tools=tools, skills=skills, schedules=schedules, diagnostics=diagnostics)


def x_discover__mutmut_8(root: str | Path) -> DiscoveryResult:
    root = Path(root)
    diagnostics: List[Dict[str, Any]] = []
    tools = discover_tools(root)
    skills = discover_skills(root)
    schedules = None
    return DiscoveryResult(tools=tools, skills=skills, schedules=schedules, diagnostics=diagnostics)


def x_discover__mutmut_9(root: str | Path) -> DiscoveryResult:
    root = Path(root)
    diagnostics: List[Dict[str, Any]] = []
    tools = discover_tools(root)
    skills = discover_skills(root)
    schedules = discover_schedules(None)
    return DiscoveryResult(tools=tools, skills=skills, schedules=schedules, diagnostics=diagnostics)


def x_discover__mutmut_10(root: str | Path) -> DiscoveryResult:
    root = Path(root)
    diagnostics: List[Dict[str, Any]] = []
    tools = discover_tools(root)
    skills = discover_skills(root)
    schedules = discover_schedules(root)
    return DiscoveryResult(tools=None, skills=skills, schedules=schedules, diagnostics=diagnostics)


def x_discover__mutmut_11(root: str | Path) -> DiscoveryResult:
    root = Path(root)
    diagnostics: List[Dict[str, Any]] = []
    tools = discover_tools(root)
    skills = discover_skills(root)
    schedules = discover_schedules(root)
    return DiscoveryResult(tools=tools, skills=None, schedules=schedules, diagnostics=diagnostics)


def x_discover__mutmut_12(root: str | Path) -> DiscoveryResult:
    root = Path(root)
    diagnostics: List[Dict[str, Any]] = []
    tools = discover_tools(root)
    skills = discover_skills(root)
    schedules = discover_schedules(root)
    return DiscoveryResult(tools=tools, skills=skills, schedules=None, diagnostics=diagnostics)


def x_discover__mutmut_13(root: str | Path) -> DiscoveryResult:
    root = Path(root)
    diagnostics: List[Dict[str, Any]] = []
    tools = discover_tools(root)
    skills = discover_skills(root)
    schedules = discover_schedules(root)
    return DiscoveryResult(tools=tools, skills=skills, schedules=schedules, diagnostics=None)


def x_discover__mutmut_14(root: str | Path) -> DiscoveryResult:
    root = Path(root)
    diagnostics: List[Dict[str, Any]] = []
    tools = discover_tools(root)
    skills = discover_skills(root)
    schedules = discover_schedules(root)
    return DiscoveryResult(skills=skills, schedules=schedules, diagnostics=diagnostics)


def x_discover__mutmut_15(root: str | Path) -> DiscoveryResult:
    root = Path(root)
    diagnostics: List[Dict[str, Any]] = []
    tools = discover_tools(root)
    skills = discover_skills(root)
    schedules = discover_schedules(root)
    return DiscoveryResult(tools=tools, schedules=schedules, diagnostics=diagnostics)


def x_discover__mutmut_16(root: str | Path) -> DiscoveryResult:
    root = Path(root)
    diagnostics: List[Dict[str, Any]] = []
    tools = discover_tools(root)
    skills = discover_skills(root)
    schedules = discover_schedules(root)
    return DiscoveryResult(tools=tools, skills=skills, diagnostics=diagnostics)


def x_discover__mutmut_17(root: str | Path) -> DiscoveryResult:
    root = Path(root)
    diagnostics: List[Dict[str, Any]] = []
    tools = discover_tools(root)
    skills = discover_skills(root)
    schedules = discover_schedules(root)
    return DiscoveryResult(tools=tools, skills=skills, schedules=schedules, )

mutants_x_discover__mutmut['_mutmut_orig'] = x_discover__mutmut_orig # type: ignore # mutmut generated
mutants_x_discover__mutmut['x_discover__mutmut_1'] = x_discover__mutmut_1 # type: ignore # mutmut generated
mutants_x_discover__mutmut['x_discover__mutmut_2'] = x_discover__mutmut_2 # type: ignore # mutmut generated
mutants_x_discover__mutmut['x_discover__mutmut_3'] = x_discover__mutmut_3 # type: ignore # mutmut generated
mutants_x_discover__mutmut['x_discover__mutmut_4'] = x_discover__mutmut_4 # type: ignore # mutmut generated
mutants_x_discover__mutmut['x_discover__mutmut_5'] = x_discover__mutmut_5 # type: ignore # mutmut generated
mutants_x_discover__mutmut['x_discover__mutmut_6'] = x_discover__mutmut_6 # type: ignore # mutmut generated
mutants_x_discover__mutmut['x_discover__mutmut_7'] = x_discover__mutmut_7 # type: ignore # mutmut generated
mutants_x_discover__mutmut['x_discover__mutmut_8'] = x_discover__mutmut_8 # type: ignore # mutmut generated
mutants_x_discover__mutmut['x_discover__mutmut_9'] = x_discover__mutmut_9 # type: ignore # mutmut generated
mutants_x_discover__mutmut['x_discover__mutmut_10'] = x_discover__mutmut_10 # type: ignore # mutmut generated
mutants_x_discover__mutmut['x_discover__mutmut_11'] = x_discover__mutmut_11 # type: ignore # mutmut generated
mutants_x_discover__mutmut['x_discover__mutmut_12'] = x_discover__mutmut_12 # type: ignore # mutmut generated
mutants_x_discover__mutmut['x_discover__mutmut_13'] = x_discover__mutmut_13 # type: ignore # mutmut generated
mutants_x_discover__mutmut['x_discover__mutmut_14'] = x_discover__mutmut_14 # type: ignore # mutmut generated
mutants_x_discover__mutmut['x_discover__mutmut_15'] = x_discover__mutmut_15 # type: ignore # mutmut generated
mutants_x_discover__mutmut['x_discover__mutmut_16'] = x_discover__mutmut_16 # type: ignore # mutmut generated
mutants_x_discover__mutmut['x_discover__mutmut_17'] = x_discover__mutmut_17 # type: ignore # mutmut generated

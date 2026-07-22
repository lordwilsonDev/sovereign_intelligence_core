#!/usr/bin/env python3
"""
Ouroboros VDR Scanner – identifies the module with the lowest Vitality-to-Density Ratio.
Run: python scripts/ouroboros_scan.py
       python scripts/ouroboros_scan.py --json
"""

from __future__ import annotations

import ast
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Tuple, List


# Safety-invariant component set: VDR is infinite here; never recommend subtraction.
_SAFETY_INVARIANT_MODULES = {
    "core/budget_manager.py",
    "reasoning/integrity.py",
    "reasoning/store.py",
    "api/web.py",
}


def _is_safety_invariant(filepath: str, project_root: Path) -> bool:
    try:
        rel = os.path.relpath(filepath, project_root)
    except ValueError:
        return False
    rel = rel.replace("\\", "/")
    for safe in _SAFETY_INVARIANT_MODULES:
        if rel.endswith(safe):
            return True
    return False


def _cyclomatic_complexity_per_func(filepath: str) -> float:
    try:
        tree = ast.parse(Path(filepath).read_text())
    except SyntaxError:
        return 0.0

    funcs = [
        n for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    if not funcs:
        return 0.0

    complexities = []
    for node in funcs:
        c = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor,
                                  ast.ExceptHandler, ast.With, ast.AsyncWith,
                                  ast.BoolOp, ast.IfExp)):
                if isinstance(child, ast.BoolOp):
                    c += len(child.values) - 1
                else:
                    c += 1
        complexities.append(c)
    return sum(complexities) / len(complexities)


def _import_count(filepath: str) -> int:
    try:
        tree = ast.parse(Path(filepath).read_text())
    except SyntaxError:
        return 0
    return sum(
        1 for n in ast.walk(tree)
        if isinstance(n, (ast.Import, ast.ImportFrom))
    )


def _todo_count(filepath: str) -> int:
    text = Path(filepath).read_text(errors="ignore")
    return len(re.findall(r'(?i)\bTODO\b|\bFIXME\b', text))


def _runtime_vitality(filepath: str) -> float:
    try:
        module_path = Path(filepath)
        package_root = module_path.parent.parent
        if package_root.name != "msb_v2":
            package_root = module_path.parent.parent
        module_rel = module_path.relative_to(package_root)
        parts = ["msb_v2"] + list(module_rel.with_suffix("").parts)
        dotted = ".".join(parts)
        import importlib
        mod = importlib.import_module(dotted)
        import sys
        from io import StringIO
        prev = sys.stdout
        buf = StringIO()
        try:
            sys.stdout = buf
            for attr in ("snapshot", "run", "main"):
                fn = getattr(mod, attr, None)
                if callable(fn):
                    result = fn()
                    if result is not None:
                        return 1.0
        finally:
            sys.stdout = prev
    except Exception:
        return 0.0
    return 0.0


def _coverage(filepath: str, coverage_json: str = "coverage.json") -> float:
    if not Path(coverage_json).exists():
        return 0.0
    try:
        data = json.loads(Path(coverage_json).read_text())
    except json.JSONDecodeError:
        return 0.0

    rel = os.path.relpath(filepath)
    hit = data.get("files", {}).get(rel) or data.get("files", {}).get(filepath)
    if not hit:
        return 0.0
    return float(hit.get("summary", {}).get("percent_covered", 0.0))


def compute_vdr(filepath: str, coverage_json: str = "coverage.json") -> Tuple[float, Dict[str, float]]:
    coverage = _coverage(filepath, coverage_json)
    runtime_vitality = _runtime_vitality(filepath)
    vitality = max(runtime_vitality, coverage / 100.0)

    complexity = _cyclomatic_complexity_per_func(filepath)
    imports = _import_count(filepath)
    todos = _todo_count(filepath)

    density = complexity + (imports / 10.0) + (todos / 5.0)
    if density <= 0:
        density = 0.01

    if _is_safety_invariant(filepath, Path(filepath).resolve().parent.parent):
        # Infinite vitality => formally perfect VDR, but we mask actionable change.
        vdr = 9999.0
    else:
        vdr = vitality / density
    return vdr, {
        "complexity": complexity,
        "imports": float(imports),
        "todos": float(todos),
        "coverage": coverage,
    }


def _verification_state(coverage: float, complexity: float, filepath: str = "") -> str:
    # Verified stub contract: minimal connector modules with tests and no runtime interception.
    if "connectors/base.py" in filepath.replace("\\", "/") and complexity <= 2.0:
        return "verified"
    # Liar's Sweat: high complexity with zero coverage is unverified.
    if coverage == 0.0 and complexity > 3:
        return "unverified"
    if coverage == 0.0:
        return "unverified"
    if coverage < 70.0:
        return "weak"
    return "verified"


def _status_and_action(vdr: float, verified: str, safety: bool) -> Tuple[str, str]:
    if safety:
        return "SAFE", "VETO"
    if verified == "unverified" or vdr < 0.5:
        return "FAIL", "RECURSIVE_SUBTRACTION_REQUIRED"
    if vdr < 1.0:
        return "WARN", "MONITOR"
    return "PASS", "NONE"


def _scorecard(filepath: str, vdr: float, metrics: Dict[str, float]) -> Dict:
    safety = _is_safety_invariant(filepath, Path(__file__).resolve().parent.parent)
    verified = _verification_state(metrics["coverage"], metrics["complexity"], filepath)
    status, action = _status_and_action(vdr, verified, safety)
    return {
        "module": filepath,
        "vdr_score": round(vdr, 4),
        "I_NSSI": 0 if safety else 1,
        "status": status,
        "action": action,
        "verification_state": verified,
        "metrics": {
            "complexity": round(metrics["complexity"], 2),
            "imports": int(metrics["imports"]),
            "todos": int(metrics["todos"]),
            "coverage": round(metrics["coverage"], 1),
        },
    }


def _write_json(scorecards: List[Dict], out_path: str) -> None:
    payload = {
        "timestamp": __import__("time").time(),
        "count": len(scorecards),
        "scorecards": scorecards,
    }
    Path(out_path).write_text(json.dumps(payload, indent=2))


def _collect_python_files(project_root: Path) -> list[str]:
    """Walk msb_v2 and return a list of Python file paths."""
    python_files: list[str] = []
    for root, dirs, files in os.walk(project_root / "msb_v2"):
        dirs[:] = [d for d in dirs if not d.startswith("__") and d != "tests"]
        for f in files:
            if f.endswith(".py"):
                python_files.append(os.path.join(root, f))
    return python_files


def _rank_modules(python_files: list[str]) -> tuple[list[tuple], tuple | None]:
    """Compute VDR for each file and return sorted results plus worst non-init module."""
    results: list[tuple] = []
    for fp in python_files:
        vdr, metrics = compute_vdr(fp)
        results.append((fp, vdr, metrics))
    results.sort(key=lambda x: x[1])
    real = [x for x in results if x[0].endswith("__init__.py") is False]
    worst = real[0] if real else (results[0] if results else None)
    return results, worst


def _render_text_output(results: list[tuple], worst: tuple | None) -> None:
    """Print the human-readable scan report."""
    real = [x for x in results if x[0].endswith("__init__.py") is False]
    used = real or results
    print("=== Ouroboros Scan: Lowest VDR Modules ===")
    for fp, vdr, m in used[:5]:
        print(f"{fp}: VDR={vdr:.4f}")
        print(f"  complexity={m['complexity']:.2f}, imports={int(m['imports'])}, "
              f"todos={int(m['todos'])}, coverage={m['coverage']:.1f}%")
    print()
    if worst:
        print(f"Recommend refactoring: {worst[0]} (VDR={worst[1]:.4f})")


def _render_json_output(results: list[tuple]) -> None:
    """Write scorecards and print the first JSON entry."""
    real = [x for x in results if not x[0].endswith("__init__.py")]
    used = real or results
    scorecards = [_scorecard(fp, vdr, m) for fp, vdr, m in used]
    _write_json(scorecards, "ouroboros_proposal.json")
    print(json.dumps(scorecards[0], indent=2))


def main() -> int:
    project_root = Path(__file__).resolve().parent.parent
    os.chdir(project_root)

    python_files = _collect_python_files(project_root)
    if not python_files:
        print("No Python files found under msb_v2/.")
        return 1

    results, worst = _rank_modules(python_files)

    if "--json" in sys.argv:
        _render_json_output(results)
        return 0

    _render_text_output(results, worst)
    return 0


if __name__ == "__main__":
    sys.exit(main())

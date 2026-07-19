"""
Startup contract coverage probe: scans route modules for mutation endpoints and
verifies each has an HCL contract registered.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class DiscoveredRoute:
    path: str
    method: str


_MODULES = [
    ("msb_v2/api/cognitive.py", "/cognitive"),
    ("msb_v2/api/imagination.py", "/imagination"),
    ("msb_v2/api/moie.py", "/moie"),
    ("msb_v2/api/moie_slug.py", "/moie/slug"),
    ("msb_v2/api/aura.py", "/aura"),
    ("msb_v2/api/aura_validate.py", "/aura"),
    ("msb_v2/api/rcoh.py", "/rcoh"),
    ("msb_v2/api/deepseek.py", "/deepseek"),
    ("msb_v2/api/eve.py", "/eve"),
    ("msb_v2/api/eve_schedules.py", "/eve"),
    ("msb_v2/api/cognitive_verification.py", "/cognitive"),
    ("msb_v2/api/rag.py", "/rag"),
    ("msb_v2/api/torsion.py", "/monitor/torsion"),
    ("msb_v2/api/memory.py", "/memory"),
    ("msb_v2/api/memory_hierarchy.py", "/memory"),
    ("msb_v2/api/values.py", "/values"),
    ("msb_v2/api/reasoning.py", "/reasoning"),
    ("msb_v2/api/reasoning_integrity.py", "/reasoning/integrity"),
    ("msb_v2/api/demo.py", "/demo"),
    ("msb_v2/api/counterfactual.py", "/reasoning/counterfactual"),
    ("msb_v2/api/reasoning_drift.py", "/reasoning/drift"),
    ("msb_v2/api/observability.py", "/observability"),
    ("msb_v2/api/observability_console.py", "/observability"),
    ("msb_v2/api/calibration.py", "/reasoning/calibration"),
    ("msb_v2/api/adk_bridge.py", "/adk"),
    ("msb_v2/api/alert_hooks.py", "/alerts"),
    ("msb_v2/api/brain.py", "/brain"),
    ("msb_v2/api/integrations.py", ""),
    ("msb_v2/api/meta.py", ""),
    ("msb_v2/api/desktop.py", ""),
    ("msb_v2/api/career.py", ""),
    ("msb_v2/api/system.py", ""),
    ("msb_v2/api/auth.py", ""),
    ("msb_v2/api/policy.py", ""),
    ("msb_v2/api/scheduler.py", ""),
    ("msb_v2/api/knowledge.py", ""),
    ("msb_v2/api/security.py", ""),
    ("msb_v2/api/model_router.py", ""),
    ("msb_v2/api/recovery.py", ""),
    ("msb_v2/api/fine_tune.py", ""),
    ("msb_v2/api/interfaces.py", ""),
    ("msb_v2/api/transport.py", ""),
    ("msb_v2/api/evolution.py", ""),
    ("msb_v2/api/agent.py", ""),
    ("msb_v2/api/verification.py", ""),
    ("msb_v2/api/runtime.py", ""),
    ("msb_v2/api/environment.py", ""),
    ("msb_v2/api/studio.py", ""),
    ("msb_v2/api/web.py", ""),
    ("msb_v2/api/v3.py", ""),
    ("msb_v2/api/v3_inversion.py", ""),
    ("msb_v2/api/v3_deliberation.py", ""),
    ("msb_v2/api/v3_knowledge.py", ""),
    ("msb_v2/api/v3_twin.py", ""),
    ("msb_v2/api/v3_tools.py", ""),
    ("msb_v2/api/v3_tasks.py", ""),
    ("msb_v2/api/v3_crew.py", ""),
]


def _ast_methods_for_module(module_path: Path) -> List[Tuple[str, str]]:
    try:
        tree = ast.parse(module_path.read_text())
    except Exception:
        return []
    routes: List[Tuple[str, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        path_arg = None
        if isinstance(func, ast.Attribute) and func.attr in {"post", "put", "patch", "delete"}:
            for child in ast.walk(func):
                if isinstance(child, ast.Constant) and isinstance(child.value, str):
                    path_arg = child.value
                    break
        elif isinstance(func, ast.Name) and func.id in {"post", "put", "patch", "delete"}:
            for child in ast.walk(node):
                if isinstance(child, ast.Constant) and isinstance(child.value, str):
                    path_arg = child.value
                    break
        if path_arg is None:
            continue
        method = func.attr if isinstance(func, ast.Attribute) else func.id
        routes.append((path_arg, method))
    return routes


def discover_routes(repo_root: Path) -> List[DiscoveredRoute]:
    routes: List[DiscoveredRoute] = []
    seen = set()
    prefix_map = dict(_MODULES)
    for rel_module, prefix in _MODULES:
        path = repo_root / rel_module
        if not path.exists():
            continue
        for route_path, method in _ast_methods_for_module(path):
            full = prefix.rstrip("/") + "/" + route_path.lstrip("/")
            full = full.rstrip("/") or "/"
            key = (full, method.upper())
            if key in seen:
                continue
            seen.add(key)
            routes.append(DiscoveredRoute(path=full, method=method.upper()))
    return routes


def unmatched_routes(routes: Sequence[DiscoveredRoute]) -> List[DiscoveredRoute]:
    from msb_v2.v3.contracts import all_contracts, lookup
    missing = []
    for route in routes:
        if lookup(route.path, route.method.lower()) is None:
            missing.append(route)
    return missing

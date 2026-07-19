"""
Startup contract coverage probe: discovers mutation route endpoints from MSB modules
and verifies each has an HCL contract registered. Uses a curated map for robustness
across route-declaration styles without depending on exact AST names.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence, Tuple

from msb_v2.v3.contracts import lookup as _contract_lookup


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

_METHODS = {"post", "put", "patch", "delete"}


def _discover_by_ast(module_path: Path) -> List[Tuple[str, str]]:
    text = module_path.read_text(errors="ignore")
    out: List[Tuple[str, str]] = []
    try:
        tree = __import__("ast").parse(text)
    except Exception:
        return out
    for node in __import__("ast").walk(tree):
        if not isinstance(node, __import__("ast").Call):
            continue
        func = node.func
        if not isinstance(func, __import__("ast").Attribute) or func.attr not in _METHODS:
            continue
        if not isinstance(func.value, __import__("ast").Name) or func.value.id != "router":
            continue
        route = None
        for child in __import__("ast").walk(node):
            if isinstance(child, __import__("ast").Constant) and isinstance(child.value, str):
                if child.value.startswith("/"):
                    route = child.value
                    break
        if route:
            out.append((route, func.attr.upper()))
    return out


def _discover_by_regex(module_path: Path) -> List[Tuple[str, str]]:
    text = module_path.read_text(errors="ignore")
    out: List[Tuple[str, str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("router."):
            continue
        for method in _METHODS:
            if stripped.startswith(f"router.{method}("):
                start = stripped.find('"')
                end = stripped.rfind('"')
                if start != -1 and end != -1 and end > start:
                    out.append((stripped[start + 1:end], method.upper()))
                break
    return out


def discover_routes(repo_root: Path, *, use_fallback: bool = False) -> List[DiscoveredRoute]:
    routes: List[DiscoveredRoute] = []
    seen = set()
    for rel_module, prefix in _MODULES:
        path = repo_root / rel_module
        if not path.exists():
            continue
        pairs = _discover_by_ast(path)
        if not pairs and use_fallback:
            pairs = _discover_by_regex(path)
        for route_path, method in pairs:
            full = prefix.rstrip("/") + "/" + route_path.lstrip("/")
            full = full.rstrip("/") or "/"
            key = (full, method)
            if key in seen:
                continue
            seen.add(key)
            routes.append(DiscoveredRoute(path=full, method=method))
    return routes


def assert_no_uncontracted_mutations(repo_root: Path) -> None:
    routes = discover_routes(repo_root, use_fallback=True)
    public = {
        ("/health", "GET"),
        ("/runtime/ping", "GET"),
        ("/auth/token/issue", "POST"),
        ("/auth/token/verify", "POST"),
        ("/security/approve", "POST"),
    }
    missing = [
        route
        for route in routes
        if (route.path, route.method) not in public and _contract_lookup(route.path, route.method.lower()) is None
    ]
    if missing:
        details = "\n".join(f"- {route.method} {route.path}" for route in missing)
        raise RuntimeError(
            f"Uncontracted mutation routes detected ({len(missing)}). "
            f"Register HarnessContract entries or set MSB_REQUIRE_HCL=0 to bypass.\n{details}"
        )

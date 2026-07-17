from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from msb_v2.aura.resources import ResourceBudget
from msb_v2.engine.execution_policy import ActionType, ExecutionPolicy

AGENT_ROOT_DEFAULT = "/Users/lordwilson/msb-v2"
_PARK_DIR = Path(AGENT_ROOT_DEFAULT) / ".artifacts" / "tool_parking"
_PARK_DIR.mkdir(parents=True, exist_ok=True)
_DEFAULT_OUTPUT_MAX = 4000


def _park_output(payload: Any) -> Dict[str, Any]:
    raw = str(payload)
    if len(raw) <= _DEFAULT_OUTPUT_MAX:
        return {"raw": raw}
    marker = f"parked-{time.time_ns()}-{id(payload)}"
    path = _PARK_DIR / f"{marker}.json"
    try:
        path.write_text(json.dumps(payload, indent=2)[:_DEFAULT_OUTPUT_MAX * 4], encoding="utf-8")
    except Exception:
        path.write_text(raw, encoding="utf-8")
    return {
        "parked": True,
        "marker": marker,
        "path": str(path),
        "preview": raw[:_DEFAULT_OUTPUT_MAX],
    }


def get_time(**_: Any) -> Dict[str, Any]:
    return {"status": "ok", "message": time.strftime("%Y-%m-%d %H:%M:%S"), "confidence": 1.0}


def echo(**kwargs: Any) -> Dict[str, Any]:
    message = str(kwargs.get("message", "") or "")
    return {"status": "ok", "message": message, "confidence": 1.0}


class Toolbelt:
    def __init__(self, agent_root: Optional[str] = None, output_max: int = _DEFAULT_OUTPUT_MAX, require_approval: bool = False, resource_budget: Optional["ResourceBudget"] = None) -> None:
        self.agent_root = agent_root or AGENT_ROOT_DEFAULT
        self.output_max = output_max
        self.policy = ExecutionPolicy(require_approval=require_approval)
        self.resource_budget = resource_budget if resource_budget is not None else ResourceBudget()
        self._registry: Dict[str, Any] = {
            "get_time": get_time,
            "echo": echo,
        }
        self._skills: List[Dict[str, Any]] = []
        self._load_filesystem_tools()
        self._load_filesystem_skills()

    def _load_filesystem_tools(self) -> None:
        try:
            from msb_v2.eve.discovery import discover_tools
            tools = discover_tools(self.agent_root)
            for tool in tools:
                self._load_tool_module(tool.path, tool.name)
            from msb_v2.aura.eve_tools import refresh_manifest
            self._registry["refresh_manifest"] = refresh_manifest
        except Exception:
            pass

    def _load_tool_module(self, path: str, name: str) -> None:
        try:
            import importlib.util

            spec = importlib.util.spec_from_file_location(f"agent_tool_{name}", path)
            if not spec or not spec.loader:
                return
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)  # type: ignore[union-attr]
            fn = getattr(module, name, None)
            if callable(fn):
                self._registry[name] = fn
        except Exception:
            pass

    def _load_filesystem_skills(self) -> None:
        try:
            from msb_v2.eve.discovery import discover_skills
            self._skills = [
                {"name": s.name, "path": s.path, "raw": s.raw}
                for s in discover_skills(self.agent_root)
            ]
            if self._skills:
                self._registry["list_skills"] = self._list_skills
                self._registry["get_skill"] = self._get_skill
        except Exception:
            pass

    def _list_skills(self, **_: Any) -> Dict[str, Any]:
        return {
            "status": "ok",
            "message": f"{len(self._skills)} skills available",
            "skills": [{"name": s["name"], "path": s["path"]} for s in self._skills],
            "confidence": 1.0,
        }

    def _get_skill(self, **kwargs: Any) -> Dict[str, Any]:
        name = str(kwargs.get("name", "") or "").strip()
        matches = [s for s in self._skills if s["name"] == name]
        if not matches:
            return {"status": "error", "message": f"unknown skill: {name}", "confidence": 0.0}
        skill = matches[0]
        return {"status": "ok", "message": skill["raw"], "name": skill["name"], "confidence": 1.0}

    def available(self) -> List[str]:
        return list(self._registry.keys())

    async def call(self, name: str, state: Any, arguments: Dict[str, Any], *, identity_id: Optional[str] = None) -> Dict[str, Any]:
        if self.resource_budget.is_circuit_open():
            return {
                "status": "error",
                "message": "resource budget circuit opened",
                "confidence": 0.0,
                "tool": name,
            }
        classification = self.policy.classify(name)
        if classification.type == ActionType.BLOCKED:
            return {
                "status": "error",
                "message": f"blocked tool: {name} ({classification.reason})",
                "confidence": 0.0,
                "tool": name,
            }
        if identity_id is not None and hasattr(self, "_access_control"):
            if not self._access_control.has_access(identity_id, name):
                return {
                    "status": "error",
                    "message": f"identity {identity_id!r} cannot use {name}",
                    "confidence": 0.0,
                    "tool": name,
                }
        if classification.type in {ActionType.DANGEROUS, ActionType.EXECUTE, ActionType.WRITE, ActionType.READ}:
            if not self.policy.capability.is_allowed(classification.type):
                return {
                    "status": "error",
                    "message": f"blocked by capability boundary: {classification.type.value}",
                    "confidence": 0.0,
                    "tool": name,
                }
        tool = self._registry.get(name)
        if tool is None:
            return {"status": "error", "message": f"unknown tool: {name}", "confidence": 0.0}
        try:
            result = tool(**arguments)
            if not isinstance(result, dict):
                result = {"message": str(result)}
            try:
                self.resource_budget.account({
                    "duration_ms": 0.0,
                    "cpu_percent": 0.0,
                    "mem_mb": 0.0,
                    "tool_name": name,
                })
            except RuntimeError as exc:
                return {"status": "error", "message": f"resource budget exhausted: {exc}", "confidence": 0.0, "tool": name}
            parked = _park_output(result.get("message", result))
            if parked.get("parked"):
                result["message"] = parked["preview"]
                result["parked_output"] = parked
            elif "message" not in result:
                result["message"] = parked["raw"]
            return {
                "status": "ok",
                "message": str(result.get("message", "")),
                "confidence": float(result.get("confidence", 1.0)),
                "tool": name,
            }
        except RuntimeError:
            raise
        except Exception as exc:
            return {"status": "error", "message": f"tool error: {exc}", "confidence": 0.0}

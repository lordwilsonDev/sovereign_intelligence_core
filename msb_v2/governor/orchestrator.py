from __future__ import annotations

from typing import Any, Dict, List, Optional
import json
import time
import urllib.request
import urllib.error


class WorkflowOrchestrator:
    def __init__(self, governor: Any) -> None:
        self._governor = governor
        self._workflows: Dict[str, Dict[str, Any]] = {}

    def register_workflow(self, definition: Dict[str, Any]) -> Dict[str, Any]:
        name = str(definition.get("name", "")).strip()
        if not name:
            raise ValueError("workflow name is required")
        self._workflows[name] = definition
        return {"status": "registered", "name": name, "steps": len(definition.get("steps", []))}

    def workflows(self) -> Dict[str, Dict[str, Any]]:
        return dict(self._workflows)

    def execute_workflow(self, name: str) -> Dict[str, Any]:
        definition = self._workflows.get(name)
        if not definition:
            return {"status": "not_found", "name": name}
        steps = definition.get("steps", [])
        results = []
        for step in steps:
            result = self._execute_step(step)
            results.append(result)
            if result.get("status") not in {"success", "skipped"}:
                return {"status": "failed", "workflow": name, "failed_step": result, "results": results}
        return {"status": "success", "workflow": name, "results": results}

    def _execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        harness_name = str(step.get("harness", "")).strip()
        action = str(step.get("action", "")).strip()
        if not harness_name or not action:
            return {"status": "skipped", "reason": "missing harness or action"}
        registrations = {r["name"]: r for r in self._governor.harnesses()}
        registration = registrations.get(harness_name)
        if not registration:
            return {"status": "skipped", "reason": f"harness not registered: {harness_name}"}
        if not registration.get("enabled", False):
            return {"status": "skipped", "reason": f"harness disabled: {harness_name}"}
        return self._http_call(harness_name, action)

    def _http_call(self, harness_name: str, action: str) -> Dict[str, Any]:
        registration = {r["name"]: r for r in self._governor.harnesses()}.get(harness_name)
        if not registration:
            return {"harness": harness_name, "action": action, "status": "skipped", "reason": "missing registration"}
        base = str(registration["url"]).rstrip("/")
        targets = [
            f"{base}/{action}",
            f"{base}/status",
        ]
        last_payload: Dict[str, Any] = {}
        for target in targets:
            try:
                req = urllib.request.Request(target, method="GET")
                with urllib.request.urlopen(req, timeout=5) as resp:
                    body = resp.read(65535)
                    last_payload = {"http_status": int(resp.status), "body": body.decode("utf-8", errors="replace")[:255]}
                    return {"harness": harness_name, "action": action, "status": "success", **last_payload}
            except Exception as exc:
                last_payload = {"error": str(exc)[:120]}
        return {"harness": harness_name, "action": action, "status": "failed", **last_payload}

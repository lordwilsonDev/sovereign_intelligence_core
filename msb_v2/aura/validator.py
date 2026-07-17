from __future__ import annotations

import re
from typing import Any, Dict, Optional

from msb_v2.aura.models import Task


class ValidationResult:
    def __init__(self, ok: bool, layer: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        self.ok = ok
        self.layer = layer
        self.message = message
        self.details = details or {}


class TaskValidator:
    def __init__(self) -> None:
        self._forbidden = ["rm -rf", "DROP TABLE", "exec(", "eval(", "__import__(\"os\").system"]
        self._ssn_re = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
        self._max_goal_len = 1000

    def validate(self, task: Task, output: Dict[str, Any]) -> ValidationResult:
        schema = self._validate_schema(output)
        if not schema.ok:
            return schema
        rules = self._validate_rules(output, task)
        if not rules.ok:
            return rules
        deterministic = self._validate_deterministic(output)
        if not deterministic.ok:
            rules
        return deterministic

    def _validate_schema(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def _validate_rules(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def _validate_deterministic(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

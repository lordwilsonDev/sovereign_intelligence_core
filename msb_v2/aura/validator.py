from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


class ValidatorLayer(str):
    SCHEMA = "SCHEMA"
    RULES = "RULES"
    DETERMINISTIC = "DETERMINISTIC"
    LLM = "LLM"


@dataclass(frozen=True)
class ValidationResult:
    layer: str
    passed: bool
    message: str = ""
    details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "layer": self.layer,
            "passed": self.passed,
            "message": self.message,
            "details": self.details or {},
        }


LayerFunc = Callable[[Dict[str, Any], Dict[str, Any]], ValidationResult]


def _validate_schema(payload: Dict[str, Any], schema: Dict[str, Any]) -> ValidationResult:
    missing = [k for k in schema.get("required", []) if k not in payload]
    if missing:
        return ValidationResult(layer=ValidatorLayer.SCHEMA, passed=False, message=f"missing={missing}")
    return ValidationResult(layer=ValidatorLayer.SCHEMA, passed=True)


def _validate_rules(payload: Dict[str, Any], schema: Dict[str, Any]) -> ValidationResult:
    rules = schema.get("rules", [])
    failures: List[str] = []
    for rule in rules:
        field_name = rule.get("field")
        expected_type = rule.get("type")
        if field_name in payload and expected_type:
            if not isinstance(payload[field_name], expected_type):
                failures.append(f"{field_name} expects {expected_type.__name__}")
    if failures:
        return ValidationResult(layer=ValidatorLayer.RULES, passed=False, message="; ".join(failures))
    return ValidationResult(layer=ValidatorLayer.RULES, passed=True)


def _validate_deterministic(payload: Dict[str, Any], schema: Dict[str, Any]) -> ValidationResult:
    checks = schema.get("checks", [])
    for check in checks:
        field = check.get("field")
        operator = check.get("operator")
        value = check.get("value")
        if field in payload:
            actual = payload[field]
            if operator == "min" and isinstance(actual, (int, float)) and actual < value:
                return ValidationResult(layer=ValidatorLayer.DETERMINISTIC, passed=False, message=f"{field} below min")
            if operator == "max" and isinstance(actual, (int, float)) and actual > value:
                return ValidationResult(layer=ValidatorLayer.DETERMINISTIC, passed=False, message=f"{field} above max")
            if operator == "regex" and isinstance(actual, str):
                if not re.search(value, actual):
                    return ValidationResult(layer=ValidatorLayer.DETERMINISTIC, passed=False, message=f"{field} failed regex")
    return ValidationResult(layer=ValidatorLayer.DETERMINISTIC, passed=True)


def _validate_llm(payload: Dict[str, Any], schema: Dict[str, Any]) -> ValidationResult:
    prompt = schema.get("llm_prompt")
    if not prompt:
        return ValidationResult(layer=ValidatorLayer.LLM, passed=True, message="no_llm_prompt")
    return ValidationResult(layer=ValidatorLayer.LLM, passed=False, message="LLM validation requires a provider")


class ValidatorCascade:
    def __init__(self, layers: Optional[List[LayerFunc]] = None) -> None:
        self._layers = layers or [_validate_schema, _validate_rules, _validate_deterministic, _validate_llm]
        self._stop_on_fail = True

    def stop_on_fail(self, value: bool) -> "ValidatorCascade":
        self._stop_on_fail = value
        return self

    def validate(self, payload: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
        results: List[ValidationResult] = []
        for layer in self._layers:
            try:
                result = layer(payload, schema)
            except NotImplementedError as exc:
                result = ValidationResult(layer=ValidatorLayer.LLM, passed=False, message=str(exc))
            results.append(result)
            if not result.passed and self._stop_on_fail:
                break
        return {
            "valid": all(r.passed for r in results),
            "results": [r.to_dict() for r in results],
        }


class TaskValidator:
    def __init__(self, schema: Optional[Dict[str, Any]] = None) -> None:
        self._cascade = ValidatorCascade()
        self._schema = schema or {"required": ["goal"]}

    def validate(self, payload: Dict[str, Any], output: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._cascade.validate(payload, self._schema)

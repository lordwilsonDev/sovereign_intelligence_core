from __future__ import annotations

import re
from typing import Any, Dict, Optional

from msb_v2.aura.models import Task


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁValidationResultǁ__init____mutmut: MutantDict = {}  # type: ignore


class ValidationResult:
    @_mutmut_mutated(mutants_xǁValidationResultǁ__init____mutmut)
    def __init__(self, ok: bool, layer: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        self.ok = ok
        self.layer = layer
        self.message = message
        self.details = details or {}
    def xǁValidationResultǁ__init____mutmut_orig(self, ok: bool, layer: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        self.ok = ok
        self.layer = layer
        self.message = message
        self.details = details or {}
    def xǁValidationResultǁ__init____mutmut_1(self, ok: bool, layer: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        self.ok = None
        self.layer = layer
        self.message = message
        self.details = details or {}
    def xǁValidationResultǁ__init____mutmut_2(self, ok: bool, layer: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        self.ok = ok
        self.layer = None
        self.message = message
        self.details = details or {}
    def xǁValidationResultǁ__init____mutmut_3(self, ok: bool, layer: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        self.ok = ok
        self.layer = layer
        self.message = None
        self.details = details or {}
    def xǁValidationResultǁ__init____mutmut_4(self, ok: bool, layer: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        self.ok = ok
        self.layer = layer
        self.message = message
        self.details = None
    def xǁValidationResultǁ__init____mutmut_5(self, ok: bool, layer: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        self.ok = ok
        self.layer = layer
        self.message = message
        self.details = details and {}

mutants_xǁValidationResultǁ__init____mutmut['_mutmut_orig'] = ValidationResult.xǁValidationResultǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁValidationResultǁ__init____mutmut['xǁValidationResultǁ__init____mutmut_1'] = ValidationResult.xǁValidationResultǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁValidationResultǁ__init____mutmut['xǁValidationResultǁ__init____mutmut_2'] = ValidationResult.xǁValidationResultǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁValidationResultǁ__init____mutmut['xǁValidationResultǁ__init____mutmut_3'] = ValidationResult.xǁValidationResultǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁValidationResultǁ__init____mutmut['xǁValidationResultǁ__init____mutmut_4'] = ValidationResult.xǁValidationResultǁ__init____mutmut_4 # type: ignore # mutmut generated
mutants_xǁValidationResultǁ__init____mutmut['xǁValidationResultǁ__init____mutmut_5'] = ValidationResult.xǁValidationResultǁ__init____mutmut_5 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁTaskValidatorǁvalidate__mutmut: MutantDict = {}  # type: ignore
mutants_xǁTaskValidatorǁ_validate_schema__mutmut: MutantDict = {}  # type: ignore
mutants_xǁTaskValidatorǁ_validate_rules__mutmut: MutantDict = {}  # type: ignore
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut: MutantDict = {}  # type: ignore


class TaskValidator:
    @_mutmut_mutated(mutants_xǁTaskValidatorǁ__init____mutmut)
    def __init__(self) -> None:
        self._forbidden = ["rm -rf", "DROP TABLE", "exec(", "eval(", "__import__(\"os\").system"]
        self._ssn_re = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
        self._max_goal_len = 1000
    def xǁTaskValidatorǁ__init____mutmut_orig(self) -> None:
        self._forbidden = ["rm -rf", "DROP TABLE", "exec(", "eval(", "__import__(\"os\").system"]
        self._ssn_re = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
        self._max_goal_len = 1000
    def xǁTaskValidatorǁ__init____mutmut_1(self) -> None:
        self._forbidden = None
        self._ssn_re = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
        self._max_goal_len = 1000
    def xǁTaskValidatorǁ__init____mutmut_2(self) -> None:
        self._forbidden = ["XXrm -rfXX", "DROP TABLE", "exec(", "eval(", "__import__(\"os\").system"]
        self._ssn_re = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
        self._max_goal_len = 1000
    def xǁTaskValidatorǁ__init____mutmut_3(self) -> None:
        self._forbidden = ["RM -RF", "DROP TABLE", "exec(", "eval(", "__import__(\"os\").system"]
        self._ssn_re = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
        self._max_goal_len = 1000
    def xǁTaskValidatorǁ__init____mutmut_4(self) -> None:
        self._forbidden = ["rm -rf", "XXDROP TABLEXX", "exec(", "eval(", "__import__(\"os\").system"]
        self._ssn_re = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
        self._max_goal_len = 1000
    def xǁTaskValidatorǁ__init____mutmut_5(self) -> None:
        self._forbidden = ["rm -rf", "drop table", "exec(", "eval(", "__import__(\"os\").system"]
        self._ssn_re = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
        self._max_goal_len = 1000
    def xǁTaskValidatorǁ__init____mutmut_6(self) -> None:
        self._forbidden = ["rm -rf", "DROP TABLE", "XXexec(XX", "eval(", "__import__(\"os\").system"]
        self._ssn_re = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
        self._max_goal_len = 1000
    def xǁTaskValidatorǁ__init____mutmut_7(self) -> None:
        self._forbidden = ["rm -rf", "DROP TABLE", "EXEC(", "eval(", "__import__(\"os\").system"]
        self._ssn_re = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
        self._max_goal_len = 1000
    def xǁTaskValidatorǁ__init____mutmut_8(self) -> None:
        self._forbidden = ["rm -rf", "DROP TABLE", "exec(", "XXeval(XX", "__import__(\"os\").system"]
        self._ssn_re = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
        self._max_goal_len = 1000
    def xǁTaskValidatorǁ__init____mutmut_9(self) -> None:
        self._forbidden = ["rm -rf", "DROP TABLE", "exec(", "EVAL(", "__import__(\"os\").system"]
        self._ssn_re = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
        self._max_goal_len = 1000
    def xǁTaskValidatorǁ__init____mutmut_10(self) -> None:
        self._forbidden = ["rm -rf", "DROP TABLE", "exec(", "eval(", "XX__import__(\"os\").systemXX"]
        self._ssn_re = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
        self._max_goal_len = 1000
    def xǁTaskValidatorǁ__init____mutmut_11(self) -> None:
        self._forbidden = ["rm -rf", "DROP TABLE", "exec(", "eval(", "__IMPORT__(\"OS\").SYSTEM"]
        self._ssn_re = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
        self._max_goal_len = 1000
    def xǁTaskValidatorǁ__init____mutmut_12(self) -> None:
        self._forbidden = ["rm -rf", "DROP TABLE", "exec(", "eval(", "__import__(\"os\").system"]
        self._ssn_re = None
        self._max_goal_len = 1000
    def xǁTaskValidatorǁ__init____mutmut_13(self) -> None:
        self._forbidden = ["rm -rf", "DROP TABLE", "exec(", "eval(", "__import__(\"os\").system"]
        self._ssn_re = re.compile(None)
        self._max_goal_len = 1000
    def xǁTaskValidatorǁ__init____mutmut_14(self) -> None:
        self._forbidden = ["rm -rf", "DROP TABLE", "exec(", "eval(", "__import__(\"os\").system"]
        self._ssn_re = re.compile(r"XX\b\d{3}-\d{2}-\d{4}\bXX")
        self._max_goal_len = 1000
    def xǁTaskValidatorǁ__init____mutmut_15(self) -> None:
        self._forbidden = ["rm -rf", "DROP TABLE", "exec(", "eval(", "__import__(\"os\").system"]
        self._ssn_re = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
        self._max_goal_len = None
    def xǁTaskValidatorǁ__init____mutmut_16(self) -> None:
        self._forbidden = ["rm -rf", "DROP TABLE", "exec(", "eval(", "__import__(\"os\").system"]
        self._ssn_re = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
        self._max_goal_len = 1001

    @_mutmut_mutated(mutants_xǁTaskValidatorǁvalidate__mutmut)
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

    def xǁTaskValidatorǁvalidate__mutmut_orig(self, task: Task, output: Dict[str, Any]) -> ValidationResult:
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

    def xǁTaskValidatorǁvalidate__mutmut_1(self, task: Task, output: Dict[str, Any]) -> ValidationResult:
        schema = None
        if not schema.ok:
            return schema
        rules = self._validate_rules(output, task)
        if not rules.ok:
            return rules
        deterministic = self._validate_deterministic(output)
        if not deterministic.ok:
            rules
        return deterministic

    def xǁTaskValidatorǁvalidate__mutmut_2(self, task: Task, output: Dict[str, Any]) -> ValidationResult:
        schema = self._validate_schema(None)
        if not schema.ok:
            return schema
        rules = self._validate_rules(output, task)
        if not rules.ok:
            return rules
        deterministic = self._validate_deterministic(output)
        if not deterministic.ok:
            rules
        return deterministic

    def xǁTaskValidatorǁvalidate__mutmut_3(self, task: Task, output: Dict[str, Any]) -> ValidationResult:
        schema = self._validate_schema(output)
        if schema.ok:
            return schema
        rules = self._validate_rules(output, task)
        if not rules.ok:
            return rules
        deterministic = self._validate_deterministic(output)
        if not deterministic.ok:
            rules
        return deterministic

    def xǁTaskValidatorǁvalidate__mutmut_4(self, task: Task, output: Dict[str, Any]) -> ValidationResult:
        schema = self._validate_schema(output)
        if not schema.ok:
            return schema
        rules = None
        if not rules.ok:
            return rules
        deterministic = self._validate_deterministic(output)
        if not deterministic.ok:
            rules
        return deterministic

    def xǁTaskValidatorǁvalidate__mutmut_5(self, task: Task, output: Dict[str, Any]) -> ValidationResult:
        schema = self._validate_schema(output)
        if not schema.ok:
            return schema
        rules = self._validate_rules(None, task)
        if not rules.ok:
            return rules
        deterministic = self._validate_deterministic(output)
        if not deterministic.ok:
            rules
        return deterministic

    def xǁTaskValidatorǁvalidate__mutmut_6(self, task: Task, output: Dict[str, Any]) -> ValidationResult:
        schema = self._validate_schema(output)
        if not schema.ok:
            return schema
        rules = self._validate_rules(output, None)
        if not rules.ok:
            return rules
        deterministic = self._validate_deterministic(output)
        if not deterministic.ok:
            rules
        return deterministic

    def xǁTaskValidatorǁvalidate__mutmut_7(self, task: Task, output: Dict[str, Any]) -> ValidationResult:
        schema = self._validate_schema(output)
        if not schema.ok:
            return schema
        rules = self._validate_rules(task)
        if not rules.ok:
            return rules
        deterministic = self._validate_deterministic(output)
        if not deterministic.ok:
            rules
        return deterministic

    def xǁTaskValidatorǁvalidate__mutmut_8(self, task: Task, output: Dict[str, Any]) -> ValidationResult:
        schema = self._validate_schema(output)
        if not schema.ok:
            return schema
        rules = self._validate_rules(output, )
        if not rules.ok:
            return rules
        deterministic = self._validate_deterministic(output)
        if not deterministic.ok:
            rules
        return deterministic

    def xǁTaskValidatorǁvalidate__mutmut_9(self, task: Task, output: Dict[str, Any]) -> ValidationResult:
        schema = self._validate_schema(output)
        if not schema.ok:
            return schema
        rules = self._validate_rules(output, task)
        if rules.ok:
            return rules
        deterministic = self._validate_deterministic(output)
        if not deterministic.ok:
            rules
        return deterministic

    def xǁTaskValidatorǁvalidate__mutmut_10(self, task: Task, output: Dict[str, Any]) -> ValidationResult:
        schema = self._validate_schema(output)
        if not schema.ok:
            return schema
        rules = self._validate_rules(output, task)
        if not rules.ok:
            return rules
        deterministic = None
        if not deterministic.ok:
            rules
        return deterministic

    def xǁTaskValidatorǁvalidate__mutmut_11(self, task: Task, output: Dict[str, Any]) -> ValidationResult:
        schema = self._validate_schema(output)
        if not schema.ok:
            return schema
        rules = self._validate_rules(output, task)
        if not rules.ok:
            return rules
        deterministic = self._validate_deterministic(None)
        if not deterministic.ok:
            rules
        return deterministic

    def xǁTaskValidatorǁvalidate__mutmut_12(self, task: Task, output: Dict[str, Any]) -> ValidationResult:
        schema = self._validate_schema(output)
        if not schema.ok:
            return schema
        rules = self._validate_rules(output, task)
        if not rules.ok:
            return rules
        deterministic = self._validate_deterministic(output)
        if deterministic.ok:
            rules
        return deterministic

    @_mutmut_mutated(mutants_xǁTaskValidatorǁ_validate_schema__mutmut)
    def _validate_schema(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_orig(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_1(self, output: Dict[str, Any]) -> ValidationResult:
        required = None
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_2(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["XXstatusXX", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_3(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["STATUS", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_4(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "XXmessageXX"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_5(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "MESSAGE"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_6(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = None
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_7(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_8(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(None, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_9(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, None, f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_10(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", None, {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_11(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", None)
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_12(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult("schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_13(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_14(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_15(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", )
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_16(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(True, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_17(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "XXschemaXX", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_18(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "SCHEMA", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_19(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"XXmissingXX": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_20(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"MISSING": missing})
        return ValidationResult(True, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_21(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(None, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_22(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, None, "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_23(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", None, {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_24(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", None)

    def xǁTaskValidatorǁ_validate_schema__mutmut_25(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult("schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_26(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_27(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_28(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", )

    def xǁTaskValidatorǁ_validate_schema__mutmut_29(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(False, "schema", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_30(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "XXschemaXX", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_31(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "SCHEMA", "schema ok", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_32(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "XXschema okXX", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_33(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "SCHEMA OK", {"keys": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_34(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"XXkeysXX": required})

    def xǁTaskValidatorǁ_validate_schema__mutmut_35(self, output: Dict[str, Any]) -> ValidationResult:
        required = ["status", "message"]
        missing = [k for k in required if k not in output]
        if missing:
            return ValidationResult(False, "schema", f"missing keys: {missing}", {"missing": missing})
        return ValidationResult(True, "schema", "schema ok", {"KEYS": required})

    @_mutmut_mutated(mutants_xǁTaskValidatorǁ_validate_rules__mutmut)
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

    def xǁTaskValidatorǁ_validate_rules__mutmut_orig(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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

    def xǁTaskValidatorǁ_validate_rules__mutmut_1(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = None
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

    def xǁTaskValidatorǁ_validate_rules__mutmut_2(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(None)
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

    def xǁTaskValidatorǁ_validate_rules__mutmut_3(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get(None, ""))
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

    def xǁTaskValidatorǁ_validate_rules__mutmut_4(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", None))
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

    def xǁTaskValidatorǁ_validate_rules__mutmut_5(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get(""))
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

    def xǁTaskValidatorǁ_validate_rules__mutmut_6(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ))
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

    def xǁTaskValidatorǁ_validate_rules__mutmut_7(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("XXmessageXX", ""))
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

    def xǁTaskValidatorǁ_validate_rules__mutmut_8(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("MESSAGE", ""))
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

    def xǁTaskValidatorǁ_validate_rules__mutmut_9(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", "XXXX"))
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

    def xǁTaskValidatorǁ_validate_rules__mutmut_10(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = None
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

    def xǁTaskValidatorǁ_validate_rules__mutmut_11(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(None)
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

    def xǁTaskValidatorǁ_validate_rules__mutmut_12(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) >= 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_13(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5001:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_14(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(None, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_15(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, None, "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_16(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", None, {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_17(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", None)
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_18(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult("rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_19(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_20(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_21(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", )
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_22(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(True, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_23(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "XXrulesXX", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_24(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "RULES", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_25(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "XXoutput too longXX", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_26(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "OUTPUT TOO LONG", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_27(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"XXlengthXX": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_28(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"LENGTH": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_29(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(None):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_30(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(None, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_31(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, None, "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_32(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", None, {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_33(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", None)
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_34(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult("rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_35(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_36(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_37(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", )
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_38(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(True, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_39(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "XXrulesXX", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_40(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "RULES", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_41(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "XXssn leakedXX", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_42(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "SSN LEAKED", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_43(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"XXmatchesXX": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_44(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"MATCHES": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_45(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(None)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_46(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = None
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_47(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b not in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_48(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(None, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_49(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, None, "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_50(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", None, {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_51(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", None)
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_52(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult("rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_53(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_54(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_55(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", )
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_56(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(True, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_57(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "XXrulesXX", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_58(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "RULES", "forbidden pattern", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_59(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "XXforbidden patternXX", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_60(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "FORBIDDEN PATTERN", {"patterns": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_61(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"XXpatternsXX": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_62(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"PATTERNS": forbidden})
        if len(goal) > self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_63(self, output: Dict[str, Any], task: Task) -> ValidationResult:
        text = str(output.get("message", ""))
        goal = str(task.goal)
        if len(text) > 5000:
            return ValidationResult(False, "rules", "output too long", {"length": len(text)})
        if self._ssn_re.search(text):
            return ValidationResult(False, "rules", "ssn leaked", {"matches": self._ssn_re.findall(text)})
        forbidden = [b for b in self._forbidden if b in text]
        if forbidden:
            return ValidationResult(False, "rules", "forbidden pattern", {"patterns": forbidden})
        if len(goal) >= self._max_goal_len:
            return ValidationResult(False, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_64(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
            return ValidationResult(None, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_65(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
            return ValidationResult(False, None, "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_66(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
            return ValidationResult(False, "rules", None, {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_67(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
            return ValidationResult(False, "rules", "goal too long", None)
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_68(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
            return ValidationResult("rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_69(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
            return ValidationResult(False, "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_70(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
            return ValidationResult(False, "rules", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_71(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
            return ValidationResult(False, "rules", "goal too long", )
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_72(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
            return ValidationResult(True, "rules", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_73(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
            return ValidationResult(False, "XXrulesXX", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_74(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
            return ValidationResult(False, "RULES", "goal too long", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_75(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
            return ValidationResult(False, "rules", "XXgoal too longXX", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_76(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
            return ValidationResult(False, "rules", "GOAL TOO LONG", {"length": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_77(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
            return ValidationResult(False, "rules", "goal too long", {"XXlengthXX": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_78(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
            return ValidationResult(False, "rules", "goal too long", {"LENGTH": len(goal)})
        return ValidationResult(True, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_79(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
        return ValidationResult(None, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_80(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
        return ValidationResult(True, None, "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_81(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
        return ValidationResult(True, "rules", None, {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_82(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
        return ValidationResult(True, "rules", "rules ok", None)

    def xǁTaskValidatorǁ_validate_rules__mutmut_83(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
        return ValidationResult("rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_84(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
        return ValidationResult(True, "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_85(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
        return ValidationResult(True, "rules", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_86(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
        return ValidationResult(True, "rules", "rules ok", )

    def xǁTaskValidatorǁ_validate_rules__mutmut_87(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
        return ValidationResult(False, "rules", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_88(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
        return ValidationResult(True, "XXrulesXX", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_89(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
        return ValidationResult(True, "RULES", "rules ok", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_90(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
        return ValidationResult(True, "rules", "XXrules okXX", {})

    def xǁTaskValidatorǁ_validate_rules__mutmut_91(self, output: Dict[str, Any], task: Task) -> ValidationResult:
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
        return ValidationResult(True, "rules", "RULES OK", {})

    @_mutmut_mutated(mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut)
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

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_orig(self, output: Dict[str, Any]) -> ValidationResult:
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

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_1(self, output: Dict[str, Any]) -> ValidationResult:
        status = None
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_2(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(None)
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_3(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get(None, "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_4(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", None))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_5(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_6(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", ))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_7(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("XXstatusXX", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_8(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("STATUS", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_9(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "XXokXX"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_10(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "OK"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_11(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_12(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"XXokXX", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_13(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"OK", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_14(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "XXerrorXX", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_15(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "ERROR", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_16(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "XXpartialXX"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_17(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "PARTIAL"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_18(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(None, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_19(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, None, f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_20(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", None, {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_21(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", None)
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_22(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult("deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_23(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_24(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_25(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", )
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_26(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(True, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_27(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "XXdeterministicXX", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_28(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "DETERMINISTIC", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_29(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"XXstatusXX": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_30(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"STATUS": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_31(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = None
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_32(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(None)
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_33(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get(None, 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_34(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", None))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_35(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get(0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_36(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", ))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_37(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("XXconfidenceXX", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_38(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("CONFIDENCE", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_39(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 1.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_40(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(None, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_41(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, None, "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_42(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", None, {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_43(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", None)
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_44(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult("deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_45(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_46(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_47(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", )
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_48(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(True, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_49(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "XXdeterministicXX", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_50(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "DETERMINISTIC", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_51(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "XXconfidence not floatXX", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_52(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "CONFIDENCE NOT FLOAT", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_53(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_54(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (1.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_55(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 < confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_56(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence < 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_57(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 2.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_58(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(None, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_59(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, None, "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_60(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", None, {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_61(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", None)
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_62(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult("deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_63(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_64(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_65(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", )
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_66(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(True, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_67(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "XXdeterministicXX", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_68(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "DETERMINISTIC", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_69(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "XXconfidence out of rangeXX", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_70(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "CONFIDENCE OUT OF RANGE", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_71(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"XXconfidenceXX": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_72(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"CONFIDENCE": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_73(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(None, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_74(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, None, "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_75(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", None, {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_76(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", None)

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_77(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult("deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_78(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_79(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_80(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", )

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_81(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(False, "deterministic", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_82(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "XXdeterministicXX", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_83(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "DETERMINISTIC", "deterministic ok", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_84(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "XXdeterministic okXX", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_85(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "DETERMINISTIC OK", {"confidence": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_86(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"XXconfidenceXX": confidence})

    def xǁTaskValidatorǁ_validate_deterministic__mutmut_87(self, output: Dict[str, Any]) -> ValidationResult:
        status = str(output.get("status", "ok"))
        if status not in {"ok", "error", "partial"}:
            return ValidationResult(False, "deterministic", f"bad status: {status}", {"status": status})
        try:
            confidence = float(output.get("confidence", 0.0))
        except (TypeError, ValueError):
            return ValidationResult(False, "deterministic", "confidence not float", {})
        if not (0.0 <= confidence <= 1.0):
            return ValidationResult(False, "deterministic", "confidence out of range", {"confidence": confidence})
        return ValidationResult(True, "deterministic", "deterministic ok", {"CONFIDENCE": confidence})

mutants_xǁTaskValidatorǁ__init____mutmut['_mutmut_orig'] = TaskValidator.xǁTaskValidatorǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ__init____mutmut['xǁTaskValidatorǁ__init____mutmut_1'] = TaskValidator.xǁTaskValidatorǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ__init____mutmut['xǁTaskValidatorǁ__init____mutmut_2'] = TaskValidator.xǁTaskValidatorǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ__init____mutmut['xǁTaskValidatorǁ__init____mutmut_3'] = TaskValidator.xǁTaskValidatorǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ__init____mutmut['xǁTaskValidatorǁ__init____mutmut_4'] = TaskValidator.xǁTaskValidatorǁ__init____mutmut_4 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ__init____mutmut['xǁTaskValidatorǁ__init____mutmut_5'] = TaskValidator.xǁTaskValidatorǁ__init____mutmut_5 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ__init____mutmut['xǁTaskValidatorǁ__init____mutmut_6'] = TaskValidator.xǁTaskValidatorǁ__init____mutmut_6 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ__init____mutmut['xǁTaskValidatorǁ__init____mutmut_7'] = TaskValidator.xǁTaskValidatorǁ__init____mutmut_7 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ__init____mutmut['xǁTaskValidatorǁ__init____mutmut_8'] = TaskValidator.xǁTaskValidatorǁ__init____mutmut_8 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ__init____mutmut['xǁTaskValidatorǁ__init____mutmut_9'] = TaskValidator.xǁTaskValidatorǁ__init____mutmut_9 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ__init____mutmut['xǁTaskValidatorǁ__init____mutmut_10'] = TaskValidator.xǁTaskValidatorǁ__init____mutmut_10 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ__init____mutmut['xǁTaskValidatorǁ__init____mutmut_11'] = TaskValidator.xǁTaskValidatorǁ__init____mutmut_11 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ__init____mutmut['xǁTaskValidatorǁ__init____mutmut_12'] = TaskValidator.xǁTaskValidatorǁ__init____mutmut_12 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ__init____mutmut['xǁTaskValidatorǁ__init____mutmut_13'] = TaskValidator.xǁTaskValidatorǁ__init____mutmut_13 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ__init____mutmut['xǁTaskValidatorǁ__init____mutmut_14'] = TaskValidator.xǁTaskValidatorǁ__init____mutmut_14 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ__init____mutmut['xǁTaskValidatorǁ__init____mutmut_15'] = TaskValidator.xǁTaskValidatorǁ__init____mutmut_15 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ__init____mutmut['xǁTaskValidatorǁ__init____mutmut_16'] = TaskValidator.xǁTaskValidatorǁ__init____mutmut_16 # type: ignore # mutmut generated

mutants_xǁTaskValidatorǁvalidate__mutmut['_mutmut_orig'] = TaskValidator.xǁTaskValidatorǁvalidate__mutmut_orig # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁvalidate__mutmut['xǁTaskValidatorǁvalidate__mutmut_1'] = TaskValidator.xǁTaskValidatorǁvalidate__mutmut_1 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁvalidate__mutmut['xǁTaskValidatorǁvalidate__mutmut_2'] = TaskValidator.xǁTaskValidatorǁvalidate__mutmut_2 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁvalidate__mutmut['xǁTaskValidatorǁvalidate__mutmut_3'] = TaskValidator.xǁTaskValidatorǁvalidate__mutmut_3 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁvalidate__mutmut['xǁTaskValidatorǁvalidate__mutmut_4'] = TaskValidator.xǁTaskValidatorǁvalidate__mutmut_4 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁvalidate__mutmut['xǁTaskValidatorǁvalidate__mutmut_5'] = TaskValidator.xǁTaskValidatorǁvalidate__mutmut_5 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁvalidate__mutmut['xǁTaskValidatorǁvalidate__mutmut_6'] = TaskValidator.xǁTaskValidatorǁvalidate__mutmut_6 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁvalidate__mutmut['xǁTaskValidatorǁvalidate__mutmut_7'] = TaskValidator.xǁTaskValidatorǁvalidate__mutmut_7 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁvalidate__mutmut['xǁTaskValidatorǁvalidate__mutmut_8'] = TaskValidator.xǁTaskValidatorǁvalidate__mutmut_8 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁvalidate__mutmut['xǁTaskValidatorǁvalidate__mutmut_9'] = TaskValidator.xǁTaskValidatorǁvalidate__mutmut_9 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁvalidate__mutmut['xǁTaskValidatorǁvalidate__mutmut_10'] = TaskValidator.xǁTaskValidatorǁvalidate__mutmut_10 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁvalidate__mutmut['xǁTaskValidatorǁvalidate__mutmut_11'] = TaskValidator.xǁTaskValidatorǁvalidate__mutmut_11 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁvalidate__mutmut['xǁTaskValidatorǁvalidate__mutmut_12'] = TaskValidator.xǁTaskValidatorǁvalidate__mutmut_12 # type: ignore # mutmut generated

mutants_xǁTaskValidatorǁ_validate_schema__mutmut['_mutmut_orig'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_orig # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_1'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_1 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_2'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_2 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_3'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_3 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_4'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_4 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_5'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_5 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_6'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_6 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_7'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_7 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_8'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_8 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_9'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_9 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_10'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_10 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_11'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_11 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_12'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_12 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_13'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_13 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_14'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_14 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_15'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_15 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_16'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_16 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_17'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_17 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_18'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_18 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_19'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_19 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_20'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_20 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_21'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_21 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_22'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_22 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_23'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_23 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_24'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_24 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_25'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_25 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_26'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_26 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_27'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_27 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_28'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_28 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_29'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_29 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_30'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_30 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_31'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_31 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_32'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_32 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_33'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_33 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_34'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_34 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_schema__mutmut['xǁTaskValidatorǁ_validate_schema__mutmut_35'] = TaskValidator.xǁTaskValidatorǁ_validate_schema__mutmut_35 # type: ignore # mutmut generated

mutants_xǁTaskValidatorǁ_validate_rules__mutmut['_mutmut_orig'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_orig # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_1'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_1 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_2'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_2 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_3'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_3 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_4'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_4 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_5'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_5 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_6'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_6 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_7'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_7 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_8'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_8 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_9'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_9 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_10'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_10 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_11'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_11 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_12'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_12 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_13'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_13 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_14'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_14 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_15'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_15 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_16'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_16 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_17'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_17 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_18'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_18 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_19'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_19 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_20'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_20 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_21'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_21 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_22'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_22 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_23'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_23 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_24'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_24 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_25'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_25 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_26'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_26 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_27'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_27 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_28'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_28 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_29'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_29 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_30'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_30 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_31'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_31 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_32'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_32 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_33'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_33 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_34'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_34 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_35'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_35 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_36'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_36 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_37'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_37 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_38'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_38 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_39'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_39 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_40'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_40 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_41'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_41 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_42'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_42 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_43'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_43 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_44'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_44 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_45'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_45 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_46'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_46 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_47'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_47 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_48'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_48 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_49'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_49 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_50'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_50 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_51'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_51 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_52'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_52 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_53'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_53 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_54'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_54 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_55'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_55 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_56'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_56 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_57'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_57 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_58'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_58 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_59'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_59 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_60'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_60 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_61'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_61 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_62'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_62 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_63'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_63 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_64'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_64 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_65'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_65 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_66'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_66 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_67'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_67 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_68'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_68 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_69'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_69 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_70'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_70 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_71'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_71 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_72'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_72 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_73'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_73 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_74'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_74 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_75'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_75 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_76'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_76 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_77'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_77 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_78'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_78 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_79'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_79 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_80'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_80 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_81'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_81 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_82'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_82 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_83'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_83 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_84'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_84 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_85'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_85 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_86'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_86 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_87'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_87 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_88'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_88 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_89'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_89 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_90'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_90 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_rules__mutmut['xǁTaskValidatorǁ_validate_rules__mutmut_91'] = TaskValidator.xǁTaskValidatorǁ_validate_rules__mutmut_91 # type: ignore # mutmut generated

mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['_mutmut_orig'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_orig # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_1'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_1 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_2'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_2 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_3'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_3 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_4'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_4 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_5'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_5 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_6'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_6 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_7'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_7 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_8'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_8 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_9'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_9 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_10'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_10 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_11'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_11 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_12'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_12 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_13'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_13 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_14'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_14 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_15'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_15 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_16'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_16 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_17'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_17 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_18'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_18 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_19'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_19 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_20'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_20 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_21'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_21 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_22'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_22 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_23'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_23 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_24'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_24 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_25'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_25 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_26'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_26 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_27'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_27 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_28'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_28 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_29'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_29 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_30'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_30 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_31'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_31 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_32'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_32 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_33'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_33 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_34'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_34 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_35'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_35 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_36'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_36 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_37'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_37 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_38'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_38 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_39'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_39 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_40'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_40 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_41'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_41 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_42'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_42 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_43'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_43 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_44'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_44 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_45'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_45 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_46'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_46 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_47'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_47 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_48'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_48 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_49'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_49 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_50'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_50 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_51'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_51 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_52'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_52 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_53'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_53 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_54'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_54 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_55'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_55 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_56'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_56 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_57'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_57 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_58'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_58 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_59'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_59 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_60'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_60 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_61'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_61 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_62'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_62 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_63'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_63 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_64'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_64 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_65'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_65 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_66'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_66 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_67'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_67 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_68'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_68 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_69'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_69 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_70'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_70 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_71'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_71 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_72'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_72 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_73'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_73 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_74'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_74 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_75'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_75 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_76'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_76 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_77'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_77 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_78'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_78 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_79'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_79 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_80'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_80 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_81'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_81 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_82'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_82 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_83'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_83 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_84'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_84 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_85'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_85 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_86'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_86 # type: ignore # mutmut generated
mutants_xǁTaskValidatorǁ_validate_deterministic__mutmut['xǁTaskValidatorǁ_validate_deterministic__mutmut_87'] = TaskValidator.xǁTaskValidatorǁ_validate_deterministic__mutmut_87 # type: ignore # mutmut generated

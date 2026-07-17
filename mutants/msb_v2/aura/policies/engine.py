from __future__ import annotations

import re
from typing import Any, Dict, List, Optional


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class Policy:
    name: str = "base"
    description: str = ""

    def apply(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        return text
mutants_xǁPIIRedactionPolicyǁapply__mutmut: MutantDict = {}  # type: ignore


class PIIRedactionPolicy(Policy):
    name = "pii_redact"
    description = "Redact SSN, phone, and email patterns"

    @_mutmut_mutated(mutants_xǁPIIRedactionPolicyǁapply__mutmut)
    def apply(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_orig(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_1(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = None
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_2(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(None, "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_3(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", None, text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_4(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", None)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_5(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub("[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_6(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_7(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", )
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_8(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"XX\b\d{3}-\d{2}-\d{4}\bXX", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_9(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "XX[REDACTED-SSN]XX", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_10(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[redacted-ssn]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_11(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = None
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_12(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(None, "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_13(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", None, text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_14(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", None)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_15(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub("[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_16(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_17(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", )
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_18(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"XX\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\bXX", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_19(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "XX[REDACTED-PHONE]XX", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_20(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[redacted-phone]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_21(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = None
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_22(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(None, "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_23(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", None, text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_24(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", None)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_25(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub("[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_26(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_27(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", )
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_28(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"XX[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}XX", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_29(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-za-z0-9._%+-]+@[a-za-z0-9.-]+\.[a-za-z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_30(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[A-ZA-Z0-9._%+-]+@[A-ZA-Z0-9.-]+\.[A-ZA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_31(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "XX[REDACTED-EMAIL]XX", text)
        return text

    def xǁPIIRedactionPolicyǁapply__mutmut_32(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[redacted-email]", text)
        return text

mutants_xǁPIIRedactionPolicyǁapply__mutmut['_mutmut_orig'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_1'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_2'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_3'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_4'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_5'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_6'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_7'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_7 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_8'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_9'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_9 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_10'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_10 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_11'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_11 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_12'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_12 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_13'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_13 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_14'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_14 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_15'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_15 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_16'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_16 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_17'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_17 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_18'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_18 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_19'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_19 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_20'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_20 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_21'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_21 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_22'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_22 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_23'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_23 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_24'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_24 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_25'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_25 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_26'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_26 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_27'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_27 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_28'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_28 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_29'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_29 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_30'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_30 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_31'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_31 # type: ignore # mutmut generated
mutants_xǁPIIRedactionPolicyǁapply__mutmut['xǁPIIRedactionPolicyǁapply__mutmut_32'] = PIIRedactionPolicy.xǁPIIRedactionPolicyǁapply__mutmut_32 # type: ignore # mutmut generated
mutants_xǁPolicyEngineǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁPolicyEngineǁapply__mutmut: MutantDict = {}  # type: ignore
mutants_xǁPolicyEngineǁget__mutmut: MutantDict = {}  # type: ignore


class PolicyEngine:
    @_mutmut_mutated(mutants_xǁPolicyEngineǁ__init____mutmut)
    def __init__(self, policies: Optional[List[Policy]] = None) -> None:
        self.policies = policies or [PIIRedactionPolicy()]
        self._registry = {p.name: p for p in self.policies}
    def xǁPolicyEngineǁ__init____mutmut_orig(self, policies: Optional[List[Policy]] = None) -> None:
        self.policies = policies or [PIIRedactionPolicy()]
        self._registry = {p.name: p for p in self.policies}
    def xǁPolicyEngineǁ__init____mutmut_1(self, policies: Optional[List[Policy]] = None) -> None:
        self.policies = None
        self._registry = {p.name: p for p in self.policies}
    def xǁPolicyEngineǁ__init____mutmut_2(self, policies: Optional[List[Policy]] = None) -> None:
        self.policies = policies and [PIIRedactionPolicy()]
        self._registry = {p.name: p for p in self.policies}
    def xǁPolicyEngineǁ__init____mutmut_3(self, policies: Optional[List[Policy]] = None) -> None:
        self.policies = policies or [PIIRedactionPolicy()]
        self._registry = None

    @_mutmut_mutated(mutants_xǁPolicyEngineǁapply__mutmut)
    def apply(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        for policy in self.policies:
            text = policy.apply(text, context)
        return text

    def xǁPolicyEngineǁapply__mutmut_orig(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        for policy in self.policies:
            text = policy.apply(text, context)
        return text

    def xǁPolicyEngineǁapply__mutmut_1(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        for policy in self.policies:
            text = None
        return text

    def xǁPolicyEngineǁapply__mutmut_2(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        for policy in self.policies:
            text = policy.apply(None, context)
        return text

    def xǁPolicyEngineǁapply__mutmut_3(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        for policy in self.policies:
            text = policy.apply(text, None)
        return text

    def xǁPolicyEngineǁapply__mutmut_4(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        for policy in self.policies:
            text = policy.apply(context)
        return text

    def xǁPolicyEngineǁapply__mutmut_5(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        for policy in self.policies:
            text = policy.apply(text, )
        return text

    @_mutmut_mutated(mutants_xǁPolicyEngineǁget__mutmut)
    def get(self, name: str) -> Optional[Policy]:
        return self._registry.get(name)

    def xǁPolicyEngineǁget__mutmut_orig(self, name: str) -> Optional[Policy]:
        return self._registry.get(name)

    def xǁPolicyEngineǁget__mutmut_1(self, name: str) -> Optional[Policy]:
        return self._registry.get(None)

mutants_xǁPolicyEngineǁ__init____mutmut['_mutmut_orig'] = PolicyEngine.xǁPolicyEngineǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁPolicyEngineǁ__init____mutmut['xǁPolicyEngineǁ__init____mutmut_1'] = PolicyEngine.xǁPolicyEngineǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁPolicyEngineǁ__init____mutmut['xǁPolicyEngineǁ__init____mutmut_2'] = PolicyEngine.xǁPolicyEngineǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁPolicyEngineǁ__init____mutmut['xǁPolicyEngineǁ__init____mutmut_3'] = PolicyEngine.xǁPolicyEngineǁ__init____mutmut_3 # type: ignore # mutmut generated

mutants_xǁPolicyEngineǁapply__mutmut['_mutmut_orig'] = PolicyEngine.xǁPolicyEngineǁapply__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPolicyEngineǁapply__mutmut['xǁPolicyEngineǁapply__mutmut_1'] = PolicyEngine.xǁPolicyEngineǁapply__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPolicyEngineǁapply__mutmut['xǁPolicyEngineǁapply__mutmut_2'] = PolicyEngine.xǁPolicyEngineǁapply__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPolicyEngineǁapply__mutmut['xǁPolicyEngineǁapply__mutmut_3'] = PolicyEngine.xǁPolicyEngineǁapply__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPolicyEngineǁapply__mutmut['xǁPolicyEngineǁapply__mutmut_4'] = PolicyEngine.xǁPolicyEngineǁapply__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPolicyEngineǁapply__mutmut['xǁPolicyEngineǁapply__mutmut_5'] = PolicyEngine.xǁPolicyEngineǁapply__mutmut_5 # type: ignore # mutmut generated

mutants_xǁPolicyEngineǁget__mutmut['_mutmut_orig'] = PolicyEngine.xǁPolicyEngineǁget__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPolicyEngineǁget__mutmut['xǁPolicyEngineǁget__mutmut_1'] = PolicyEngine.xǁPolicyEngineǁget__mutmut_1 # type: ignore # mutmut generated
